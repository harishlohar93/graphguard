from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AccountViewSet, AlertViewSet, ClusterViewSet, AuditLogViewSet, graph_data

router = DefaultRouter()
router.register("accounts", AccountViewSet)
router.register("alerts", AlertViewSet)
router.register("clusters", ClusterViewSet)
router.register("auditlogs", AuditLogViewSet)

urlpatterns = router.urls+ [
    path("graph/", graph_data),
]