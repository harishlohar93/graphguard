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
from api.scoring_service import ScoringService


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
    try:
        nodes_result = Neo4jService.run_query("""
            MATCH (a:Account)
            RETURN a.id AS id,
                   a.username AS username,
                   a.account_type AS account_type,
                   a.follower_count AS follower_count
        """)

        edges_result = Neo4jService.run_query("""
            MATCH (a:Account)-[:FOLLOWS]->(b:Account)
            RETURN a.id AS source, b.id AS target
            LIMIT 1500
        """)
        alert_map = {}
        alerts = Alert.objects.select_related("account").all()
        for alert in alerts:
            alert_map[alert.account.account_id] = alert.label

        for node in nodes_result:
            node["label"] = alert_map.get(node["id"], "normal")

        return Response({
            "nodes": nodes_result,
            "edges": edges_result
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(["POST"])
def score_account(request, account_id):
    try:
        result = ScoringService.score_single_account(account_id)

        try:
            account = Account.objects.get(account_id=result["account_id"])
            Alert.objects.update_or_create(
                account=account,
                defaults={
                    "score": result["anomaly_score"],
                    "label": result["label"],
                    "status": "pending",
                }
            )
        except Account.DoesNotExist:
            pass

        return Response(result)

    except RuntimeError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=500)
    
@api_view(["POST"])
def run_setup(request):
    secret = request.data.get("secret")
    if secret != "graphguard-setup-2024":
        return Response({"error": "unauthorized"}, status=401)
    
    try:
        from django.core.management import call_command
        import io
        results = {}

        out = io.StringIO()
        call_command("sync_accounts", stdout=out)
        results["sync_accounts"] = "done"

        call_command("train_model", stdout=out)
        results["train_model"] = "done"

        call_command("score_all", stdout=out)
        results["score_all"] = "done"

        return Response({"status": "setup complete", "results": results})
    except Exception as e:
        return Response({"error": str(e)}, status=500)    
    