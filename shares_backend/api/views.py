from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView, status
from rest_framework import viewsets

from api.models import Category, Share, Company, Order, Broker, SubCategory
from api.serializers import CategorySerializer, ShareSerializer, OrderSerializer, BrokerSerializer, SubCategorySerializer
from django.core.files.storage import FileSystemStorage

@api_view(['GET'])
def categories(request):
    try:
        return Response(CategorySerializer(Category.objects.all(), many=True).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def category(request, id):
    try:
        return Response(CategorySerializer(Category.objects.get(id=id)).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def shares_by_category(request, id):
    try:
        category = Category.objects.get(id=id)
        return Response(ShareSerializer(category.share_set.all(), many=True).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def shares_by_company(request, id):
    try:
        company = Company.objects.get(id=id)
        return Response(ShareSerializer(company.share_set.all(), many=True).data, status=status.HTTP_200_OK)
    except:
        return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShareView(APIView):
    def get(self, request):
        try:
            return Response(ShareSerializer(Share.objects.all(), many=True).data, status=status.HTTP_200_OK)
        except:
            return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        category = Category.objects.get(name=request.data.get('category'))
        subcategory = SubCategory.objects.get(name=request.data.get('subcategory'))
        company = Company.objects.get(name=request.data.get('company'))
        
        Share.objects.create(
            name = request.data.get('name'),
            category = category,
            subcategory = subcategory,
            company = company,
            description = request.data.get('description'),
            image = request.data.get('image'),
            price = request.data.get('price')
        )
        return Response({"message":"Entity created successfully"}, status=status.HTTP_201_CREATED)

class ShareDetailedView(APIView):
    def get(self, request, id):
        try:
            return Response(ShareSerializer(Share.objects.get(id=id)).data, status=status.HTTP_200_OK)
        except:
            return Response({"exception":"happened"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST', 'GET'])
def order_share(request):
    if request.method == 'POST':
        share = Share.objects.get(id=request.data.get('share'))
        broker = Broker.objects.get(id=request.data.get('broker'))
        Order.objects.create(
            name = request.data.get('name'),
            phone = request.data.get('phone'),
            status = 'awaits_call',
            attached_broker = broker,
            share = share
        )
        return Response({"message":"Order created successfully"}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        return Response(OrderSerializer(Order.objects.all(), many=True).data, status=status.HTTP_200_OK)


class OrderInfo(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request, id):
        return Response(OrderSerializer(Order.objects.get(id=id)).data, status=status.HTTP_200_OK)

    def put(self,request, id):
        order = Order.objects.get(id=id)
        order.status = request.data.get('status')
        order.save()
        return Response({"message":"Order has been updated."}, status=status.HTTP_200_OK)

    def delete(self,request,id):
        order = Order.objects.get(id=id)
        order.delete()
        return Response({"message":"Order has been deleted."}, status=status.HTTP_200_OK)


class SubCategoryVS(viewsets.ViewSet):
    def list(self, request):
        queryset = SubCategory.objects.all()
        serializer = SubCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = SubCategory.objects.all()
        subcat = get_object_or_404(queryset, pk=id)
        serializer = SubCategorySerializer(subcat)
        return Response(serializer.data)

class BrokerVS(viewsets.ViewSet):
    def list(self, request):
        queryset = Broker.objects.all()
        serializer = BrokerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Broker.objects.all()
        subcat = get_object_or_404(queryset, pk=id)
        serializer = BrokerSerializer(subcat)
        return Response(serializer.data)

class BrokerToFireVS(viewsets.ViewSet):
    def list(self, request):
        queryset = Broker.need_to_fire.all()
        serializer = BrokerSerializer(queryset, many=True)
        return Response(serializer.data)

class OrdersCompletedVS(viewsets.ViewSet):
    def list(self, request):
        queryset = Order.completed.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

class OrdersDeclinedVS(viewsets.ViewSet):
    def list(self, request):
        queryset = Order.declined.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

class OrdersInProgressVS(viewsets.ViewSet):
    def list(self, request):
        queryset = Order.in_progress.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return Response({'message': 'lol'})


subcat_list = SubCategoryVS.as_view({'get':'list'})
subcat_detailed = SubCategoryVS.as_view({'get':'retrieve'})
broker_list = BrokerVS.as_view({'get':'list'})
broker_detailed = BrokerVS.as_view({'get':'retrieve'})
broker_to_fire_list = BrokerVS.as_view({'get':'list'})
orders_completed = OrdersCompletedVS.as_view({'get':'list'})
orders_declined = OrdersDeclinedVS.as_view({'get':'list'})
orders_in_progress = OrdersInProgressVS.as_view({'get':'list'})


