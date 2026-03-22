from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Alert, Cluster, AuditLog
from .serializers import (
    AccountSerializer,
    AlertSerializer,
    ClusterSerializer,
    AuditLogSerializer,
)


@api_view(["GET"])
def health_check(request):
    return Response({
        "status": "ok",
        "day": 1,
        "project": "GraphGuard",
        "message": "Day 1 complete — Django is running!"
    })


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["label", "status"]
    search_fields = ["account__username"]
    ordering_fields = ["score", "created_at"]


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
