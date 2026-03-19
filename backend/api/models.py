from django.db import models


class Account(models.Model):

    ACCOUNT_TYPE_CHOICES = [
        ("normal", "Normal"),
        ("bot", "Bot"),
        ("suspect", "Suspect"),
    ]

    account_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=150)
    created_days_ago = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default="normal"
    )
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.account_id})"

    class Meta:
        ordering = ["-created_at"]


class Cluster(models.Model):

    RISK_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    name = models.CharField(max_length=100)
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_CHOICES,
        default="low"
    )
    member_count = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0.0)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.risk_level} risk"

    class Meta:
        ordering = ["-detected_at"]


class Alert(models.Model):

    LABEL_CHOICES = [
        ("normal", "Normal"),
        ("suspect", "Suspect"),
        ("bot", "Bot"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("suspended", "Suspended"),
        ("safe", "Marked Safe"),
        ("escalated", "Escalated"),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="alerts"
    )
    cluster = models.ForeignKey(
        Cluster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts"
    )
    score = models.FloatField()
    label = models.CharField(
        max_length=20,
        choices=LABEL_CHOICES,
        default="normal"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alert: {self.account.username} — score {self.score} ({self.label})"

    class Meta:
        ordering = ["-created_at"]


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("suspended", "Suspended"),
        ("marked_safe", "Marked Safe"),
        ("escalated", "Escalated"),
        ("reviewed", "Reviewed"),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs"
    )
    note = models.TextField(blank=True, default="")
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.account.username}"

    class Meta:
        ordering = ["-performed_at"]