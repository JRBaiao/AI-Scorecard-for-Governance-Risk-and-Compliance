from django.db import models
from .compliance_data import RISK_LABELS, USE_CASE_CATEGORIES


class Evaluation(models.Model):
    RISK_CHOICES = [(k, v) for k, v in RISK_LABELS.items()]
    USE_CASE_CHOICES = [(cat[0], cat[1]) for cat in USE_CASE_CATEGORIES]

    # Vendor information (Step 1)
    vendor_name = models.CharField(max_length=200)
    vendor_country = models.CharField(max_length=100)
    vendor_website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField()

    # AI system information (Step 1)
    system_name = models.CharField(max_length=200)
    system_description = models.TextField()
    system_version = models.CharField(max_length=50, blank=True)

    # Risk classification (Step 2)
    use_case_category = models.CharField(max_length=60, choices=USE_CASE_CHOICES)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)

    # Evaluator (Step 3 / Results)
    evaluated_by = models.CharField(max_length=200, blank=True)
    evaluator_organisation = models.CharField(max_length=200, blank=True)
    evaluation_date = models.DateField(null=True, blank=True)

    # Results (Step 4)
    compliance_score = models.FloatField(null=True, blank=True)
    compliance_status = models.CharField(max_length=30, blank=True)
    status_class = models.CharField(max_length=20, blank=True)

    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor_name} – {self.system_name} ({self.risk_level})"

    def get_use_case_label(self):
        return dict(self.USE_CASE_CHOICES).get(self.use_case_category, self.use_case_category)

    def get_risk_label(self):
        return RISK_LABELS.get(self.risk_level, self.risk_level)


class ComplianceAnswer(models.Model):
    ANSWER_CHOICES = [
        ('yes',     'Yes – Fully Compliant'),
        ('partial', 'Partial – Work in Progress'),
        ('no',      'No – Not Compliant'),
        ('na',      'Not Applicable'),
    ]

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='answers')
    requirement_key = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    article = models.CharField(max_length=20)
    answer = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['evaluation', 'requirement_key']
        ordering = ['requirement_key']

    def __str__(self):
        return f"{self.evaluation} | {self.requirement_key}: {self.answer}"

    @property
    def answer_label(self):
        return dict(self.ANSWER_CHOICES).get(self.answer, self.answer)

    @property
    def answer_class(self):
        return {
            'yes': 'success',
            'partial': 'warning',
            'no': 'danger',
            'na': 'secondary',
        }.get(self.answer, 'secondary')
