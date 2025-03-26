from rest_framework.routers import DefaultRouter
from .views import NetworkObjectViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'network-objects', NetworkObjectViewSet, basename='networkobject')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls
