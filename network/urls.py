from rest_framework.routers import DefaultRouter

from .views import NetworkObjectViewSet, ProductViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'network-objects', NetworkObjectViewSet, basename='networkobject')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'contact', ContactViewSet, basename='contact')

urlpatterns = router.urls
