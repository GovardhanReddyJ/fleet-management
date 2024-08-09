from .models import Vehicle_category,Vehicle, Trip,Order
from .serializers import VehicleCategorySerializer,VehicleSerializer, TripSerializer,OrderSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.authentication import BasicAuthentication
from django.http import Http404
from django.utils import timezone
import json
import environ
import razorpay
from rest_framework.decorators import api_view


class AvailableVehiclesViewSet(viewsets.ViewSet):
    def list(self, request):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        num_of_people = request.data.get('num_of_people')
        # vehicle_id = request.data.get('vehicle_id')

        if start_date and end_date and num_of_people:
            vehicles = Vehicle.objects.all()
            # if vehicle_id:
            #     vehicles = vehicles.filter(id=vehicle_id)

            available_vehicles = vehicles.exclude(
                Q(trip__start_date__lte=start_date, trip__end_date__gte=end_date) |
                Q(trip__start_date__gte=start_date, trip__end_date__lte=end_date) |
                Q(trip__start_date__lte=start_date, trip__end_date__gte=start_date) |
                Q(trip__start_date__lte=end_date, trip__end_date__gte=end_date)
            ).filter(type_of_vehicle__no_of_seats__gte=num_of_people).distinct()

            serializer = VehicleSerializer(available_vehicles, many=True)
            return Response(serializer.data)
        else:
            return Response("Missing required fields", status=status.HTTP_400_BAD_REQUEST)
# class AvailableVehiclesAPIView(APIView):
#     def get(self, request):
#         start_date = request.data.get('start_date')
#         end_date = request.data.get('end_date')
#         num_of_people = request.data.get('num_of_people')
#
#         if start_date and end_date and num_of_people:
#             available_vehicles = Vehicle.objects.exclude(
#                 Q(trip__start_date__lte=start_date, trip__end_date__gte=end_date) |
#                 Q(trip__start_date__gte=start_date, trip__end_date__lte=end_date) |
#                 Q(trip__start_date__lte=start_date, trip__end_date__gte=start_date) |
#                 Q(trip__start_date__lte=end_date, trip__end_date__gte=end_date)
#             ).filter(type_of_vehicle__no_of_seats__gte=num_of_people).distinct()
#             serializer = VehicleSerializer(available_vehicles, many=True)
#             return Response(serializer.data)
#         else:
#             return Response("Missing required fields", status=status.HTTP_400_BAD_REQUEST)

# class AllocateVehicleAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         data['created_by'] = str(request.user.get('username'))
#         serializer = TripSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get_object(self, pk):
#         try:
#             return Trip.objects.get(pk=pk)
#         except Trip.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         trip = self.get_object(pk)
#         serializer = TripSerializer(trip)
#         return Response(serializer.data)
#     def get(self):
#         trip = Trip.objects.all()
#         serializer = TripSerializer(trip)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         trip = self.get_object(pk)
#         data = request.data
#         data['updated_by'] = str(request.user.get('username'))
#         data['updated_at'] = timezone.now()
#         serializer = TripSerializer(trip, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, pk):
#         trip = self.get_object(pk)
#         trip.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
class AllocateVehicleViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        data['created_by'] = str(request.user.get('id'))
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data['updated_by'] = str(request.user.get('id'))
        data['updated_at'] = timezone.now()
        serializer = self.get_serializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterVehicleAPIView(APIView):
    def post(self, request):
        data=request.data
        data['created_by']=str(request.user.get('id'))
        print(request.user)
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404
    # def get(self, request, pk):
    #     vehicle = self.get_object(pk)
    #     serializer = VehicleSerializer(vehicle)
    #     return Response(serializer.data)
    def get(self):
        vehicle = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)

    def put(self, request, pk):
        vehicle = self.get_object(pk)
        data = request.data
        data['updated_by'] = str(request.user.get('id'))
        data['updated_at'] = timezone.now()
        serializer = VehicleSerializer(vehicle, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        vehicle = self.get_object(pk)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class VehicleCategoryViewSet(viewsets.ModelViewSet):
    queryset = Vehicle_category.objects.all()
    serializer_class = VehicleCategorySerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get('created_by', None):
            request.data['created_by'] = request.user.get('id')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.data.get('updated_by', None):
            request.data['updated_by'] = request.user.get('id')
            request.data['updated_at'] = timezone.now()
        return super().update(request, *args, **kwargs)




# # payments/views.py
# import razorpay
# from django.conf import settings
# from rest_framework import status, views
# from rest_framework.response import Response
# from .serializers import PaymentSerializer
# from .models import Payment

# client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

# class PaymentView(views.APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PaymentSerializer(data=request.data)
#         if serializer.is_valid():
#             amount = serializer.validated_data['amount']
#             currency = serializer.validated_data['currency']
#             razorpay_payment_id = serializer.validated_data['razorpay_payment_id']

#             try:
#                 # Verify the payment
#                 payment = client.payment.fetch(razorpay_payment_id)
#                 if payment['status'] == 'captured':
#                     Payment.objects.create(
#                         amount=amount,
#                         currency=currency,
#                         razorpay_payment_id=razorpay_payment_id
#                     )
#                     return Response({"success": "Payment processed successfully"}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"error": "Payment not captured"}, status=status.HTTP_400_BAD_REQUEST)
#             except razorpay.errors.RazorpayError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

env = environ.Env()
environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    amount = request.data['amount']
    name = request.data['name']

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)
