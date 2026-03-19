from django.contrib import admin
from .models import Account, Alert, Cluster, AuditLog


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["username", "account_id", "account_type", "is_flagged", "follower_count", "created_days_ago"]
    list_filter = ["account_type", "is_flagged"]
    search_fields = ["username", "account_id"]


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["account", "score", "label", "status", "created_at"]
    list_filter = ["label", "status"]
    search_fields = ["account__username"]


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ["name", "risk_level", "member_count", "avg_score", "detected_at"]
    list_filter = ["risk_level"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["account", "action", "performed_by", "performed_at"]
    list_filter = ["action"]
    search_fields = ["account__username"]