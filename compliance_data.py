"""
EU AI Act compliance requirements organised by risk level.
Each requirement maps to a specific article of the EU AI Act (2024/1689).
"""

USE_CASE_CATEGORIES = [
    # Prohibited systems (Article 5)
    ('social_scoring',        'Social Scoring by Public Authorities',                    'prohibited'),
    ('rtb_biometrics',        'Real-time Remote Biometric ID in Public Spaces',          'prohibited'),
    ('subliminal',            'Subliminal or Manipulative AI Techniques',                'prohibited'),
    ('vulnerability_exploit', 'Exploitation of Psychological/Physical Vulnerabilities',  'prohibited'),

    # High-risk systems (Annex III)
    ('biometric_identity',    'Biometric Identification & Categorisation',               'high'),
    ('critical_infra',        'Critical Infrastructure (Water / Energy / Transport)',    'high'),
    ('education_assess',      'Education & Vocational Training (Admission / Assessment)','high'),
    ('employment_hr',         'Employment, Recruitment & Worker Management',             'high'),
    ('essential_services',    'Access to Essential Services (Credit / Insurance / Benefits)', 'high'),
    ('law_enforcement',       'Law Enforcement & Criminal Justice',                      'high'),
    ('migration_border',      'Migration, Asylum & Border Control',                      'high'),
    ('justice_democracy',     'Administration of Justice & Democratic Processes',        'high'),
    ('safety_components',     'Safety Components in Regulated Products',                 'high'),

    # Limited-risk systems (Article 50)
    ('chatbot',               'Chatbot / Conversational AI',                             'limited'),
    ('deepfake_synthetic',    'Deepfake / Synthetic Content Generation',                 'limited'),
    ('emotion_recognition',   'Emotion Recognition System',                              'limited'),

    # Minimal / no-risk systems
    ('content_recommendation','Content Recommendation',                                  'minimal'),
    ('spam_filter',           'Spam / Content Filter',                                   'minimal'),
    ('process_automation',    'Business Process Automation (RPA)',                       'minimal'),
    ('analytics',             'Analytics, Reporting & Business Intelligence',            'minimal'),
    ('document_processing',   'Document Processing & Data Extraction',                  'minimal'),
    ('translation',           'Language Translation',                                    'minimal'),
    ('search',                'Search & Information Retrieval',                          'minimal'),
    ('other_minimal',         'Other – Minimal or No Risk',                              'minimal'),
]

RISK_LEVEL_MAP = {cat[0]: cat[2] for cat in USE_CASE_CATEGORIES}

RISK_LABELS = {
    'prohibited': 'Prohibited',
    'high':       'High Risk',
    'limited':    'Limited Risk',
    'minimal':    'Minimal / No Risk',
}

RISK_DESCRIPTIONS = {
    'prohibited': (
        'This use case is <strong>prohibited</strong> under Article 5 of the EU AI Act. '
        'Procuring or deploying this type of AI system in the EU is unlawful. '
        'Proceed no further with this procurement.'
    ),
    'high': (
        'High-risk AI systems (Annex III) are subject to the full set of mandatory '
        'requirements under Articles 9–15 and must undergo conformity assessment '
        'before being placed on the market or put into service.'
    ),
    'limited': (
        'Limited-risk AI systems trigger specific <strong>transparency obligations</strong> '
        'under Article 50. Users must be informed that they are interacting with AI, '
        'and synthetic content must be appropriately labelled.'
    ),
    'minimal': (
        'Minimal-risk AI systems are <strong>largely unregulated</strong> under the EU AI Act. '
        'Basic due diligence and voluntary adherence to a code of conduct are recommended.'
    ),
}

HIGH_RISK_REQUIREMENTS = [
    # ── Article 9 – Risk Management ──────────────────────────────────────────
    {
        'key': 'rm_1', 'article': 'Art. 9', 'category': 'Risk Management System',
        'question': 'Does the vendor maintain a documented risk management system specific to this AI system?',
        'guidance': (
            'Request the risk management policy and evidence of regular risk assessments. '
            'The system must identify, analyse, estimate, and evaluate risks throughout the lifecycle.'
        ),
        'weight': 2,
    },
    {
        'key': 'rm_2', 'article': 'Art. 9', 'category': 'Risk Management System',
        'question': 'Is the risk management process iterative and updated throughout the system\'s entire lifecycle?',
        'guidance': (
            'Verify that risk reviews occur after updates, incidents, or significant changes '
            'in deployment context — not only at initial release.'
        ),
        'weight': 2,
    },
    {
        'key': 'rm_3', 'article': 'Art. 9', 'category': 'Risk Management System',
        'question': 'Has the vendor identified and implemented appropriate risk mitigation measures?',
        'guidance': (
            'Review documented mitigation measures and confirm they are embedded in the system, '
            'not just listed in a policy document.'
        ),
        'weight': 2,
    },

    # ── Article 10 – Data Governance ─────────────────────────────────────────
    {
        'key': 'dg_1', 'article': 'Art. 10', 'category': 'Data & Data Governance',
        'question': 'Are training, validation, and testing datasets fully documented (origin, scope, collection methods)?',
        'guidance': (
            'Request dataset documentation (datasheets / data cards). '
            'Check data sources, collection period, demographic coverage, and known limitations.'
        ),
        'weight': 2,
    },
    {
        'key': 'dg_2', 'article': 'Art. 10', 'category': 'Data & Data Governance',
        'question': 'Has the vendor implemented bias detection and data quality assurance measures?',
        'guidance': (
            'Ask for bias testing results across relevant demographic groups and the processes '
            'used to identify and correct data quality issues before training.'
        ),
        'weight': 2,
    },
    {
        'key': 'dg_3', 'article': 'Art. 10', 'category': 'Data & Data Governance',
        'question': 'If personal data is used in training or operation, is a Data Protection Impact Assessment (DPIA) available?',
        'guidance': (
            'Under GDPR, high-risk processing of personal data requires a DPIA. '
            'For public-sector AI this is especially important — request the DPIA and confirm it covers the specific deployment.'
        ),
        'weight': 2,
    },

    # ── Article 11 – Technical Documentation ─────────────────────────────────
    {
        'key': 'td_1', 'article': 'Art. 11', 'category': 'Technical Documentation',
        'question': 'Is comprehensive technical documentation (Annex IV format) available before deployment?',
        'guidance': (
            'Documentation must be provided before the system is put into service. '
            'Request the technical file as required by Annex IV of the EU AI Act.'
        ),
        'weight': 2,
    },
    {
        'key': 'td_2', 'article': 'Art. 11', 'category': 'Technical Documentation',
        'question': 'Does the documentation cover the system\'s intended purpose, performance metrics, and known limitations?',
        'guidance': (
            'The documentation must explicitly state what the system can and cannot do, '
            'including accuracy rates, error rates, and edge cases.'
        ),
        'weight': 2,
    },
    {
        'key': 'td_3', 'article': 'Art. 11', 'category': 'Technical Documentation',
        'question': 'Is technical documentation kept up to date with all system changes and updates?',
        'guidance': (
            'There should be a version history and a defined change management procedure. '
            'Ask how documentation is updated when the model is retrained or the system changes.'
        ),
        'weight': 1,
    },

    # ── Article 12 – Record-Keeping ───────────────────────────────────────────
    {
        'key': 'rk_1', 'article': 'Art. 12', 'category': 'Record-Keeping & Logging',
        'question': 'Does the system automatically generate logs that enable traceability of its operation?',
        'guidance': (
            'Logs should capture inputs, outputs, and decision-relevant information. '
            'Verify that audit logging is enabled by default, not optional.'
        ),
        'weight': 2,
    },
    {
        'key': 'rk_2', 'article': 'Art. 12', 'category': 'Record-Keeping & Logging',
        'question': 'Are logs retained for appropriate periods and accessible for auditing purposes?',
        'guidance': (
            'Ask about log retention policies, storage security, and access controls. '
            'For public-sector use, retention may need to align with freedom-of-information requirements.'
        ),
        'weight': 2,
    },
    {
        'key': 'rk_3', 'article': 'Art. 12', 'category': 'Record-Keeping & Logging',
        'question': 'Do logs capture sufficient detail to reconstruct individual decisions made by the system?',
        'guidance': (
            'For high-stakes decisions (benefits, enforcement, etc.), it must be possible to explain '
            'why a specific outcome was produced. Test this with sample log entries.'
        ),
        'weight': 2,
    },

    # ── Article 13 – Transparency ─────────────────────────────────────────────
    {
        'key': 'tr_1', 'article': 'Art. 13', 'category': 'Transparency & Information',
        'question': 'Is plain-language information provided to operators about the system\'s capabilities and limitations?',
        'guidance': (
            'Request the instructions for use (operator guide). '
            'It must be comprehensible to non-technical staff who will operate the system day-to-day.'
        ),
        'weight': 2,
    },
    {
        'key': 'tr_2', 'article': 'Art. 13', 'category': 'Transparency & Information',
        'question': 'Are individuals affected by AI-assisted decisions informed that AI is being used?',
        'guidance': (
            'Check the notification procedure. In most public-sector contexts, '
            'individuals must be informed when AI influences decisions affecting them.'
        ),
        'weight': 2,
    },
    {
        'key': 'tr_3', 'article': 'Art. 13', 'category': 'Transparency & Information',
        'question': 'Does the instructions-for-use document cover intended purpose, performance levels, and known risks?',
        'guidance': (
            'The instructions must explicitly cover circumstances where the system should not be used '
            'and known sources of error — not just how to operate it.'
        ),
        'weight': 1,
    },

    # ── Article 14 – Human Oversight ──────────────────────────────────────────
    {
        'key': 'ho_1', 'article': 'Art. 14', 'category': 'Human Oversight',
        'question': 'Can human operators monitor the AI system\'s operation meaningfully in real time?',
        'guidance': (
            'Verify that operators have monitoring tools that provide insight into system behaviour, '
            'not just final outputs. Ask for a demonstration.'
        ),
        'weight': 2,
    },
    {
        'key': 'ho_2', 'article': 'Art. 14', 'category': 'Human Oversight',
        'question': 'Are there practical mechanisms to pause, override, or immediately shut down the system?',
        'guidance': (
            'There must be an effective "stop button" accessible to operators. '
            'Request a demonstration of the override procedure and confirm it is documented.'
        ),
        'weight': 2,
    },
    {
        'key': 'ho_3', 'article': 'Art. 14', 'category': 'Human Oversight',
        'question': 'Is there a defined, accessible process for contesting AI decisions and escalating to human review?',
        'guidance': (
            'Appeals and review procedures must be documented and realistically usable by affected persons. '
            'This is critical for decisions affecting fundamental rights.'
        ),
        'weight': 2,
    },
    {
        'key': 'ho_4', 'article': 'Art. 14', 'category': 'Human Oversight',
        'question': 'Have operators received, or will they receive, adequate training to use oversight features effectively?',
        'guidance': (
            'Ask for the operator training plan and materials. '
            'Training must cover exception handling and escalation, not just standard operation.'
        ),
        'weight': 1,
    },

    # ── Article 15 – Accuracy, Robustness & Cybersecurity ────────────────────
    {
        'key': 'ar_1', 'article': 'Art. 15', 'category': 'Accuracy, Robustness & Cybersecurity',
        'question': 'Has the system\'s accuracy been validated across diverse demographic groups and use-case scenarios?',
        'guidance': (
            'Request disaggregated accuracy metrics. The system must not perform significantly worse '
            'for any demographic group relevant to its intended use.'
        ),
        'weight': 2,
    },
    {
        'key': 'ar_2', 'article': 'Art. 15', 'category': 'Accuracy, Robustness & Cybersecurity',
        'question': 'Are measures in place to prevent, detect, and respond to adversarial inputs or data poisoning?',
        'guidance': (
            'Ask about adversarial robustness testing and input validation. '
            'This is critical for systems that may face deliberate manipulation attempts.'
        ),
        'weight': 2,
    },
    {
        'key': 'ar_3', 'article': 'Art. 15', 'category': 'Accuracy, Robustness & Cybersecurity',
        'question': 'Is there a vulnerability management and AI-specific security incident response plan?',
        'guidance': (
            'The plan should cover AI-specific threats (model theft, data poisoning, output manipulation) '
            'in addition to standard cybersecurity incidents.'
        ),
        'weight': 2,
    },
    {
        'key': 'ar_4', 'article': 'Art. 15', 'category': 'Accuracy, Robustness & Cybersecurity',
        'question': 'Is system performance continuously monitored post-deployment with alerts for degradation?',
        'guidance': (
            'AI performance can degrade over time (model drift). '
            'Ask about automated monitoring and what triggers a review or retraining.'
        ),
        'weight': 2,
    },

    # ── Articles 43 / 49 / 51 – Conformity & Registration ────────────────────
    {
        'key': 'cf_1', 'article': 'Art. 43', 'category': 'Conformity Assessment & Registration',
        'question': 'Has the system undergone a conformity assessment (third-party or self-assessment as applicable)?',
        'guidance': (
            'Most high-risk systems permit self-assessment; biometrics and law enforcement require '
            'third-party assessment. Request the conformity assessment report.'
        ),
        'weight': 2,
    },
    {
        'key': 'cf_2', 'article': 'Art. 49', 'category': 'Conformity Assessment & Registration',
        'question': 'Is the CE marking affixed to the system and its accompanying documentation?',
        'guidance': (
            'High-risk AI systems must bear CE marking, indicating the provider\'s '
            'declaration of conformity. Check the physical product and documentation.'
        ),
        'weight': 1,
    },
    {
        'key': 'cf_3', 'article': 'Art. 51', 'category': 'Conformity Assessment & Registration',
        'question': 'Is the system registered in the EU database for high-risk AI systems?',
        'guidance': (
            'Providers must register before placing the system on the market. '
            'Request the EU database registration number and verify it.'
        ),
        'weight': 2,
    },
]

LIMITED_RISK_REQUIREMENTS = [
    {
        'key': 'lt_1', 'article': 'Art. 50', 'category': 'Transparency Obligations',
        'question': 'If this is a chatbot or conversational AI, are users explicitly told they are interacting with AI?',
        'guidance': (
            'The disclosure must be clear and given at the start of the interaction. '
            '"Powered by AI" in small print is insufficient — users must be explicitly informed.'
        ),
        'weight': 2,
    },
    {
        'key': 'lt_2', 'article': 'Art. 50', 'category': 'Transparency Obligations',
        'question': 'If the system generates synthetic content (images, audio, video, text), is that content clearly labelled?',
        'guidance': (
            'Deepfakes and synthetic media must carry machine-readable and human-visible labels. '
            'Ask for a demonstration of the labelling mechanism.'
        ),
        'weight': 2,
    },
    {
        'key': 'lt_3', 'article': 'Art. 50', 'category': 'Transparency Obligations',
        'question': 'Does the vendor provide documentation showing how transparency measures are technically implemented?',
        'guidance': (
            'Transparency obligations must be technically enforced, not just stated in policy. '
            'Request technical documentation showing how disclosure is triggered in the system.'
        ),
        'weight': 1,
    },
]

MINIMAL_RISK_REQUIREMENTS = [
    {
        'key': 'mr_1', 'article': 'Recital 47', 'category': 'Voluntary Commitments',
        'question': 'Has the vendor voluntarily committed to the EU AI Act voluntary code of conduct?',
        'guidance': (
            'While not legally required, voluntary commitment to the code of conduct '
            'demonstrates responsible AI practices and should be encouraged.'
        ),
        'weight': 1,
    },
    {
        'key': 'mr_2', 'article': 'Best Practice', 'category': 'Documentation & Support',
        'question': 'Does the vendor provide adequate documentation, support, and an incident reporting process?',
        'guidance': (
            'Even minimal-risk systems should have basic documentation, '
            'clear support channels, and a process for users to report issues.'
        ),
        'weight': 1,
    },
]

REQUIREMENTS_BY_RISK = {
    'high':    HIGH_RISK_REQUIREMENTS,
    'limited': LIMITED_RISK_REQUIREMENTS,
    'minimal': MINIMAL_RISK_REQUIREMENTS,
    'prohibited': [],
}

CATEGORY_ICONS = {
    'Risk Management System':              'bi-shield-check',
    'Data & Data Governance':              'bi-database-check',
    'Technical Documentation':             'bi-file-earmark-text',
    'Record-Keeping & Logging':            'bi-journal-text',
    'Transparency & Information':          'bi-eye',
    'Human Oversight':                     'bi-person-check',
    'Accuracy, Robustness & Cybersecurity':'bi-cpu',
    'Conformity Assessment & Registration':'bi-patch-check',
    'Transparency Obligations':            'bi-megaphone',
    'Voluntary Commitments':               'bi-hand-thumbs-up',
    'Documentation & Support':             'bi-question-circle',
}

ANSWER_WEIGHTS = {'yes': 2, 'partial': 1, 'no': 0, 'na': None}

SCORE_THRESHOLDS = [
    (80, 'Compliant',          'success', 'The vendor demonstrates strong EU AI Act compliance.'),
    (60, 'Partially Compliant','warning', 'Significant gaps exist. Remediation required before procurement.'),
    (0,  'Non-Compliant',      'danger',  'Critical compliance failures identified. Do not proceed without major remediation.'),
]


def get_risk_level(use_case_key: str) -> str:
    return RISK_LEVEL_MAP.get(use_case_key, 'minimal')


def get_requirements(risk_level: str) -> list:
    return REQUIREMENTS_BY_RISK.get(risk_level, [])


def calculate_score(answers: dict) -> tuple[float | None, str, str, str]:
    """
    answers: {requirement_key: answer_value}
    Returns (score_pct, status_label, bootstrap_class, description)
    """
    total_weight = 0
    earned_weight = 0

    for req_key, answer in answers.items():
        weight = next(
            (r['weight'] for reqs in REQUIREMENTS_BY_RISK.values() for r in reqs if r['key'] == req_key),
            1
        )
        if answer == 'na':
            continue
        total_weight += weight * 2
        earned_weight += ANSWER_WEIGHTS.get(answer, 0) * weight

    if total_weight == 0:
        return None, 'No Score', 'secondary', 'No applicable questions answered.'

    pct = round((earned_weight / total_weight) * 100, 1)

    for threshold, label, cls, desc in SCORE_THRESHOLDS:
        if pct >= threshold:
            return pct, label, cls, desc

    return pct, 'Non-Compliant', 'danger', SCORE_THRESHOLDS[-1][3]
