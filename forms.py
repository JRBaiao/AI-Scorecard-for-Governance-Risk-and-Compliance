from django import forms
from .compliance_data import USE_CASE_CATEGORIES, REQUIREMENTS_BY_RISK


COUNTRY_CHOICES = [
    ('', '— Select country —'),
    ('Austria', 'Austria'), ('Belgium', 'Belgium'), ('Bulgaria', 'Bulgaria'),
    ('Croatia', 'Croatia'), ('Cyprus', 'Cyprus'), ('Czech Republic', 'Czech Republic'),
    ('Denmark', 'Denmark'), ('Estonia', 'Estonia'), ('Finland', 'Finland'),
    ('France', 'France'), ('Germany', 'Germany'), ('Greece', 'Greece'),
    ('Hungary', 'Hungary'), ('Ireland', 'Ireland'), ('Italy', 'Italy'),
    ('Latvia', 'Latvia'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'),
    ('Malta', 'Malta'), ('Netherlands', 'Netherlands'), ('Poland', 'Poland'),
    ('Portugal', 'Portugal'), ('Romania', 'Romania'), ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'), ('Spain', 'Spain'), ('Sweden', 'Sweden'),
    # Non-EU but common
    ('United Kingdom', 'United Kingdom'), ('United States', 'United States'),
    ('Canada', 'Canada'), ('Australia', 'Australia'), ('India', 'India'),
    ('China', 'China'), ('Israel', 'Israel'), ('Switzerland', 'Switzerland'),
    ('Other', 'Other'),
]

SECTOR_CHOICES = [
    ('', '— Select sector —'),
    ('Central Government', 'Central Government'),
    ('Regional / Local Government', 'Regional / Local Government'),
    ('Law Enforcement / Police', 'Law Enforcement / Police'),
    ('Justice / Courts', 'Justice / Courts'),
    ('Healthcare', 'Healthcare'),
    ('Education', 'Education'),
    ('Social Services', 'Social Services'),
    ('Tax & Revenue', 'Tax & Revenue'),
    ('Border & Immigration', 'Border & Immigration'),
    ('Defence', 'Defence'),
    ('Transport & Infrastructure', 'Transport & Infrastructure'),
    ('Financial Regulation', 'Financial Regulation'),
    ('Other Public Sector', 'Other Public Sector'),
]


class Step1VendorForm(forms.Form):
    # Vendor details
    vendor_name = forms.CharField(
        max_length=200, label='Vendor / Provider Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Acme AI Solutions GmbH'}),
    )
    vendor_country = forms.ChoiceField(
        choices=COUNTRY_CHOICES, label='Vendor Headquarters Country',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    vendor_website = forms.URLField(
        required=False, label='Vendor Website (optional)',
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
    )
    contact_person = forms.CharField(
        max_length=200, label='Primary Contact Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
    )
    contact_email = forms.EmailField(
        label='Primary Contact Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@vendor.com'}),
    )

    # System details
    system_name = forms.CharField(
        max_length=200, label='AI System Name / Product Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RiskScore Pro 3'}),
    )
    system_version = forms.CharField(
        required=False, max_length=50, label='Version / Release (optional)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. v3.1.2'}),
    )
    system_description = forms.CharField(
        label='System Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 4,
            'placeholder': 'Briefly describe what the AI system does and how it will be used.',
        }),
    )
    procurement_sector = forms.ChoiceField(
        choices=SECTOR_CHOICES, label='Procuring Organisation Sector',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class Step2RiskForm(forms.Form):
    USE_CASE_CHOICES_GROUPED = [('', '— Select a use case —')] + [
        (cat[0], cat[1]) for cat in USE_CASE_CATEGORIES
    ]

    use_case_category = forms.ChoiceField(
        choices=USE_CASE_CHOICES_GROUPED,
        label='Primary Use Case Category',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        help_text=(
            'Select the option that best describes what this AI system will be used for. '
            'The EU AI Act risk level will be determined automatically.'
        ),
    )
    processes_personal_data = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unknown', 'Unknown')],
        label='Does the system process personal data?',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='unknown',
    )
    affects_fundamental_rights = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No'), ('unknown', 'Unknown')],
        label='Could the system\'s outputs significantly affect individuals\' fundamental rights?',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='unknown',
    )
    risk_notes = forms.CharField(
        required=False, label='Risk Classification Notes (optional)',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3,
            'placeholder': 'Any additional context about the risk classification or planned deployment.',
        }),
    )


ANSWER_CHOICES = [
    ('yes',     'Yes'),
    ('partial', 'Partial'),
    ('no',      'No'),
    ('na',      'N/A'),
]


class Step3ComplianceForm(forms.Form):
    """Dynamically built from REQUIREMENTS_BY_RISK for the given risk level."""

    def __init__(self, risk_level, *args, **kwargs):
        super().__init__(*args, **kwargs)
        requirements = REQUIREMENTS_BY_RISK.get(risk_level, [])
        for req in requirements:
            key = req['key']
            self.fields[f'answer_{key}'] = forms.ChoiceField(
                choices=ANSWER_CHOICES,
                label=req['question'],
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                initial='na',
            )
            self.fields[f'notes_{key}'] = forms.CharField(
                required=False,
                label='Evidence / Notes',
                widget=forms.Textarea(attrs={
                    'class': 'form-control form-control-sm',
                    'rows': 2,
                    'placeholder': 'Optional: document evidence, observations, or follow-up actions.',
                }),
            )


class Step4EvaluatorForm(forms.Form):
    evaluated_by = forms.CharField(
        max_length=200, label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
    )
    evaluator_organisation = forms.CharField(
        max_length=200, label='Your Organisation',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ministry of Finance – IT Procurement'}),
    )
    evaluation_date = forms.DateField(
        label='Evaluation Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
