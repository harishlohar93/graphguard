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
from api.neo4j_service import Neo4jService


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



"This api endpoint will be used by the frontend to fetch graph data for visualization. It queries Neo4j for accounts and their follow relationships, and returns them in a format suitable for rendering with libraries like D3.js or Vis.js."
@api_view(["GET"])
def graph_data(request):
    nodes_result = Neo4jService.run_query("""
        MATCH (a:Account)
        RETURN a.id AS id,
               a.username AS username,
               a.account_type AS account_type,
               a.follower_count AS follower_count
        LIMIT 500
    """
        
        )

    edges_result = Neo4jService.run_query("""
        MATCH (a:Account)-[:FOLLOWS]->(b:Account)
        RETURN a.id AS source, b.id AS target
        LIMIT 2000
    """)

    return Response({
        "nodes": nodes_result,
        "edges": edges_result
    })