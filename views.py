import json
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Evaluation, ComplianceAnswer
from .forms import Step1VendorForm, Step2RiskForm, Step3ComplianceForm, Step4EvaluatorForm
from .compliance_data import (
    get_risk_level, get_requirements, calculate_score,
    RISK_LABELS, RISK_DESCRIPTIONS, CATEGORY_ICONS, USE_CASE_CATEGORIES,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _wizard_context(step: int) -> dict:
    steps = [
        (1, 'Vendor Info'),
        (2, 'Risk Classification'),
        (3, 'Compliance Assessment'),
        (4, 'Results'),
    ]
    return {'current_step': step, 'steps': steps, 'total_steps': len(steps)}


def _get_evaluation(request) -> Evaluation | None:
    eval_id = request.session.get('evaluation_id')
    if eval_id:
        try:
            return Evaluation.objects.get(pk=eval_id)
        except Evaluation.DoesNotExist:
            del request.session['evaluation_id']
    return None


def _group_answers_by_category(evaluation: Evaluation, requirements: list) -> list:
    answers_dict = {a.requirement_key: a for a in evaluation.answers.all()}
    categories = {}
    for req in requirements:
        cat = req['category']
        if cat not in categories:
            categories[cat] = {
                'name': cat,
                'icon': CATEGORY_ICONS.get(cat, 'bi-check-circle'),
                'article': req['article'],
                'items': [],
                'yes': 0, 'partial': 0, 'no': 0, 'na': 0,
            }
        answer_obj = answers_dict.get(req['key'])
        categories[cat]['items'].append({
            'req': req,
            'answer': answer_obj,
        })
        if answer_obj:
            categories[cat][answer_obj.answer] += 1
    return list(categories.values())


# ── Home ──────────────────────────────────────────────────────────────────────

def home(request):
    evaluations = Evaluation.objects.filter(completed=True)
    in_progress = _get_evaluation(request)
    return render(request, 'scorecard/home.html', {
        'evaluations': evaluations,
        'in_progress': in_progress,
    })


# ── Step 1: Vendor Information ────────────────────────────────────────────────

def step1(request):
    evaluation = _get_evaluation(request)
    initial = {}
    if evaluation:
        initial = {
            'vendor_name': evaluation.vendor_name,
            'vendor_country': evaluation.vendor_country,
            'vendor_website': evaluation.vendor_website,
            'contact_person': evaluation.contact_person,
            'contact_email': evaluation.contact_email,
            'system_name': evaluation.system_name,
            'system_version': evaluation.system_version,
            'system_description': evaluation.system_description,
        }

    if request.method == 'POST':
        form = Step1VendorForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            if evaluation:
                for field, value in d.items():
                    if hasattr(evaluation, field):
                        setattr(evaluation, field, value)
                evaluation.save()
            else:
                evaluation = Evaluation.objects.create(
                    vendor_name=d['vendor_name'],
                    vendor_country=d['vendor_country'],
                    vendor_website=d.get('vendor_website', ''),
                    contact_person=d['contact_person'],
                    contact_email=d['contact_email'],
                    system_name=d['system_name'],
                    system_version=d.get('system_version', ''),
                    system_description=d['system_description'],
                    risk_level='minimal',  # placeholder until Step 2
                )
                request.session['evaluation_id'] = evaluation.pk
            return redirect('step2')
    else:
        form = Step1VendorForm(initial=initial)

    return render(request, 'scorecard/step1_vendor.html', {
        'form': form,
        **_wizard_context(1),
    })


# ── Step 2: Risk Classification ───────────────────────────────────────────────

def step2(request):
    evaluation = _get_evaluation(request)
    if not evaluation:
        messages.warning(request, 'Please start a new evaluation.')
        return redirect('step1')

    initial = {}
    if evaluation.use_case_category:
        initial['use_case_category'] = evaluation.use_case_category

    if request.method == 'POST':
        form = Step2RiskForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            use_case = d['use_case_category']
            risk_level = get_risk_level(use_case)
            evaluation.use_case_category = use_case
            evaluation.risk_level = risk_level
            evaluation.save()
            return redirect('step3')
    else:
        form = Step2RiskForm(initial=initial)

    return render(request, 'scorecard/step2_risk.html', {
        'form': form,
        'evaluation': evaluation,
        'use_case_categories': USE_CASE_CATEGORIES,
        **_wizard_context(2),
    })


# ── Step 3: Compliance Checklist ──────────────────────────────────────────────

def step3(request):
    evaluation = _get_evaluation(request)
    if not evaluation:
        messages.warning(request, 'Please start a new evaluation.')
        return redirect('step1')
    if not evaluation.use_case_category:
        messages.warning(request, 'Please complete risk classification first.')
        return redirect('step2')

    risk_level = evaluation.risk_level
    requirements = get_requirements(risk_level)

    # Prohibited systems skip the checklist entirely
    if risk_level == 'prohibited':
        return redirect('step4')

    # Pre-populate with existing answers
    initial = {}
    existing = {a.requirement_key: a for a in evaluation.answers.all()}
    for req in requirements:
        key = req['key']
        if key in existing:
            initial[f'answer_{key}'] = existing[key].answer
            initial[f'notes_{key}'] = existing[key].notes

    if request.method == 'POST':
        form = Step3ComplianceForm(risk_level, request.POST)
        if form.is_valid():
            d = form.cleaned_data
            for req in requirements:
                key = req['key']
                answer_val = d.get(f'answer_{key}', 'na')
                notes_val = d.get(f'notes_{key}', '')
                ComplianceAnswer.objects.update_or_create(
                    evaluation=evaluation,
                    requirement_key=key,
                    defaults={
                        'category': req['category'],
                        'article': req['article'],
                        'answer': answer_val,
                        'notes': notes_val,
                    },
                )
            return redirect('step4')
    else:
        form = Step3ComplianceForm(risk_level, initial=initial)

    # Group requirements by category for template rendering
    categories = {}
    for req in requirements:
        cat = req['category']
        if cat not in categories:
            categories[cat] = {
                'name': cat,
                'icon': CATEGORY_ICONS.get(cat, 'bi-check-circle'),
                'article': req['article'],
                'items': [],
            }
        categories[cat]['items'].append({
            'req': req,
            'answer_field': form[f'answer_{req["key"]}'],
            'notes_field':  form[f'notes_{req["key"]}'],
        })

    return render(request, 'scorecard/step3_compliance.html', {
        'form': form,
        'evaluation': evaluation,
        'categories': list(categories.values()),
        'risk_label': RISK_LABELS.get(risk_level, risk_level),
        'risk_description': RISK_DESCRIPTIONS.get(risk_level, ''),
        **_wizard_context(3),
    })


# ── Step 4: Results ───────────────────────────────────────────────────────────

def step4(request):
    evaluation = _get_evaluation(request)
    if not evaluation:
        messages.warning(request, 'Please start a new evaluation.')
        return redirect('step1')

    risk_level = evaluation.risk_level
    requirements = get_requirements(risk_level)

    # Handle evaluator info form
    if request.method == 'POST':
        evaluator_form = Step4EvaluatorForm(request.POST)
        if evaluator_form.is_valid():
            d = evaluator_form.cleaned_data
            evaluation.evaluated_by = d['evaluated_by']
            evaluation.evaluator_organisation = d['evaluator_organisation']
            evaluation.evaluation_date = d['evaluation_date']

            # Calculate score
            answers = {a.requirement_key: a.answer for a in evaluation.answers.all()}
            score_pct, status_label, status_class, status_desc = calculate_score(answers)

            evaluation.compliance_score = score_pct
            evaluation.compliance_status = status_label
            evaluation.status_class = status_class
            evaluation.completed = True
            evaluation.save()

            # Clear wizard session
            if 'evaluation_id' in request.session:
                del request.session['evaluation_id']

            return redirect('results', pk=evaluation.pk)
    else:
        evaluator_form = Step4EvaluatorForm(initial={
            'evaluation_date': timezone.now().date(),
            'evaluated_by': evaluation.evaluated_by,
            'evaluator_organisation': evaluation.evaluator_organisation,
        })

    # Compute live preview score
    answers_dict = {a.requirement_key: a.answer for a in evaluation.answers.all()}
    score_pct, status_label, status_class, _ = calculate_score(answers_dict)
    grouped = _group_answers_by_category(evaluation, requirements)

    # Add per-category scores for preview
    for cat in grouped:
        cat_answers = {item['req']['key']: item['answer'].answer if item['answer'] else 'na'
                       for item in cat['items']}
        pct, _, cls, _ = calculate_score(cat_answers)
        cat['score_pct'] = pct
        cat['score_class'] = cls

    return render(request, 'scorecard/step4_preview.html', {
        'evaluation': evaluation,
        'evaluator_form': evaluator_form,
        'grouped_categories': grouped,
        'score_pct': score_pct,
        'status_label': status_label,
        'status_class': status_class,
        'risk_label': RISK_LABELS.get(risk_level, risk_level),
        'risk_description': RISK_DESCRIPTIONS.get(risk_level, ''),
        **_wizard_context(4),
    })


# ── Results (completed evaluation) ───────────────────────────────────────────

def results(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    requirements = get_requirements(evaluation.risk_level)
    grouped = _group_answers_by_category(evaluation, requirements)

    answers_dict = {a.requirement_key: a.answer for a in evaluation.answers.all()}
    _, _, _, status_desc = calculate_score(answers_dict)

    # Build per-category mini-scores
    for cat in grouped:
        cat_answers = {item['req']['key']: item['answer'].answer if item['answer'] else 'na'
                       for item in cat['items']}
        pct, _, cls, _ = calculate_score(cat_answers)
        cat['score_pct'] = pct
        cat['score_class'] = cls

    critical_gaps = [
        item for cat in grouped
        for item in cat['items']
        if item['answer'] and item['answer'].answer == 'no'
    ]

    return render(request, 'scorecard/results.html', {
        'evaluation': evaluation,
        'grouped_categories': grouped,
        'status_desc': status_desc,
        'critical_gaps': critical_gaps,
        'risk_label': RISK_LABELS.get(evaluation.risk_level, evaluation.risk_level),
        'risk_description': RISK_DESCRIPTIONS.get(evaluation.risk_level, ''),
    })


# ── History ───────────────────────────────────────────────────────────────────

def history(request):
    evaluations = Evaluation.objects.filter(completed=True)
    return render(request, 'scorecard/history.html', {'evaluations': evaluations})


# ── Delete / restart ──────────────────────────────────────────────────────────

def delete_evaluation(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    if request.method == 'POST':
        evaluation.delete()
        messages.success(request, 'Evaluation deleted.')
    return redirect('home')


def restart(request):
    if 'evaluation_id' in request.session:
        try:
            Evaluation.objects.get(pk=request.session['evaluation_id'], completed=False).delete()
        except Evaluation.DoesNotExist:
            pass
        del request.session['evaluation_id']
    return redirect('step1')


# ── AI Chat Assistant ─────────────────────────────────────────────────────────

_CHAT_SYSTEM_PROMPT = """You are a helpful EU AI Act compliance assistant embedded in the AI Procurement Scorecard tool.
You guide public sector procurement officers through evaluating AI vendors against EU AI Act (2024/1689) requirements.

You can help with:
- Explaining EU AI Act risk categories: Prohibited, High Risk, Limited Risk, Minimal Risk
- Clarifying compliance requirements mapped to specific articles (Art. 9–15, 43, 49, 50, 51)
- Guiding users through the 4-step evaluation wizard (Vendor Info → Risk Classification → Compliance Assessment → Results)
- Interpreting scores and procurement recommendations
- Answering questions about specific use cases and their risk classification

Keep answers concise and practical. This is a demo tool."""


@csrf_exempt
@require_POST
def chat_api(request):
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return JsonResponse({
            'reply': (
                "The AI assistant isn't configured yet. "
                "Please set the ANTHROPIC_API_KEY environment variable and restart the server."
            )
        })

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'Empty message.'}, status=400)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model='claude-haiku-4-5',
            max_tokens=512,
            system=_CHAT_SYSTEM_PROMPT,
            messages=[{'role': 'user', 'content': user_message}],
        )
        return JsonResponse({'reply': response.content[0].text})
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)
