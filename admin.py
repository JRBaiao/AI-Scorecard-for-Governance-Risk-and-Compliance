from django.contrib import admin
from .models import Evaluation, ComplianceAnswer


class ComplianceAnswerInline(admin.TabularInline):
    model = ComplianceAnswer
    extra = 0
    readonly_fields = ('requirement_key', 'category', 'article', 'answer', 'notes')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'system_name', 'risk_level', 'compliance_score', 'compliance_status', 'completed', 'created_at')
    list_filter = ('risk_level', 'compliance_status', 'completed')
    search_fields = ('vendor_name', 'system_name', 'contact_email')
    inlines = [ComplianceAnswerInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ComplianceAnswer)
class ComplianceAnswerAdmin(admin.ModelAdmin):
    list_display = ('evaluation', 'requirement_key', 'category', 'answer')
    list_filter = ('answer', 'category')
