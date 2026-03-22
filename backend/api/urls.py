from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, AlertViewSet, ClusterViewSet, AuditLogViewSet

router = DefaultRouter()
router.register("accounts", AccountViewSet)
router.register("alerts", AlertViewSet)
router.register("clusters", ClusterViewSet)
router.register("auditlogs", AuditLogViewSet)

urlpatterns = router.urls