from django.db.models import Avg
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import NetworkObject, Product, Contact
from .permissions import IsActiveEmployeePermission, IsOwnerNetworkObject
from .serializers import NetworkObjectSerializer, ProductSerializer, ContactSerializer
from .tasks import send_qr_code_email


class NetworkObjectViewSet(viewsets.ModelViewSet):
    queryset = NetworkObject.objects.all()
    serializer_class = NetworkObjectSerializer
    permission_classes = [IsActiveEmployeePermission, IsOwnerNetworkObject]

    # Пользователь может получить информацию только о своём объекте сети.
    # если надо чтобы не мог смотреть чужие
    # def get_queryset(self):
    #     try:
    #         employee = self.request.user.employee
    #         return NetworkObject.objects.filter(id=employee.network_object.id)
    #     except Employee.DoesNotExist:
    #         return NetworkObject.objects.none()


    @action(detail=False, methods=['get'])
    def by_country(self, request):
        country = request.query_params.get('country')
        if not country:
            return Response({"error": "Параметр 'country' обязателен."}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(contacts__address__country__iexact=country)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def above_average_debt(self, request):
        avg_debt = self.get_queryset().aggregate(avg=Avg('debt'))['avg'] or 0
        qs = self.get_queryset().filter(debt__gt=avg_debt)
        serializer = self.get_serializer(qs, many=True)
        return Response({
            "average_debt": avg_debt,
            "objects": serializer.data
        })

    @action(detail=False, methods=['get'])
    def by_product(self, request):
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


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsActiveEmployeePermission]

    @action(detail=True, methods=['post'])
    def send_qr(self, request, pk=None):
        contact = self.get_object()
        user_email = request.user.email

        if not user_email:
            return Response({"error": "Не указан e-mail"}, status=status.HTTP_400_BAD_REQUEST)

        send_qr_code_email.delay(contact.id, user_email)
        return Response({"message": f"Задача по отправке QR-кода на {user_email} запущена."},
                        status=status.HTTP_202_ACCEPTED)
