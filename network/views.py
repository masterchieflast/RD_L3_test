from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import NetworkObject, Product
from .serializers import NetworkObjectSerializer, ProductSerializer
from .permissions import IsActiveEmployeePermission


class NetworkObjectViewSet(viewsets.ModelViewSet):
    """
    API для объектов сети.
    """
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    permission_classes = [IsActiveEmployeePermission]  # Только активные сотрудники имеют доступ

    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """
        4.2 Информацию об объектах определённой страны (фильтр по названию);
        request?country=НазваниеСтраны
        """
        country = request.query_params.get('country')
        if not country:
            return Response({"error": "Параметр 'country' обязателен."}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(contacts__address__country__iexact=country)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def above_average_debt(self, request):
        """
        4.3 Статистику об объектах, задолженность которых превышает среднюю задолженность
        всех объектов
        """
        avg_debt = self.get_queryset().aggregate(avg=Avg('debt'))['avg'] or 0
        qs = self.get_queryset().filter(debt__gt=avg_debt)
        serializer = self.get_serializer(qs, many=True)
        return Response({
            "average_debt": avg_debt,
            "objects": serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_product(self, request):
        """
        4.4 Все объекты сети, где встречается определённый продукт.
        Фильтр по id продукта: ?product_id=ID_продукта
        """
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({"error": "Параметр 'product_id' обязателен."}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(products__id=product_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployeePermission]
