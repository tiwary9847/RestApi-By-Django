from django.shortcuts import render
from .models import Customer,Profession,Document,DataSheet
from .serializers import CustomerSerializer,ProfessionSerializer,DataSheetSerializer,DocumentSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

class CustomerViewSet(viewsets.ModelViewSet):
    #queryset = Customer.objects.filter(active=True)
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name','address','data_sheet__description']
    ordering_fields = '__all__'#ordeing by all the field
    ordering=('-id')#-id means ordeering by descending order
    lookup_field='doc_num'#look up field is always unique
    authentication_classes=[TokenAuthentication,]
    def get_queryset(self):
        #import pdb; pdb.set_trace()#for break point
        address=self.request.query_params.get('address', None)
        
        if self.request.query_params.get('active')=='False':

            status=False
        else:

            status=True

        if address:

            customer=Customer.objects.filter(address__icontains=address,active=status)
        else:
            customer=Customer.objects.filter(active=status)

        
        return customer

#    def list(self, request, *args, **kwargs):
#        #import pdb; pdb.set_trace()
#       customer=self.get_queryset()
#       serializer=CustomerSerializer(customer,many=True)
#       return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj=self.get_object()
        serializer=CustomerSerializer(obj)
        return Response(serializer.data)


    """def create(self, request, *args, **kwargs):
        data=request.data
        customer=Customer.objects.create(
            name=data['name'],address=data['address'],data_sheet_id=data['data_sheet']

        )
        profession=Profession.objects.get(id=data['profession'])
        customer.professions.add(profession)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    """
    def update(self, request, *args, **kwargs):
        customer=self.get_object()
        data=request.data
        customer.name=data['name']
        customer.address=data['address']
        customer.data_sheet_id=data['data_sheet']

        profession=Profession.objects.get(id=data['profession'])
        for p in customer.professions.all():
            customer.professions.remove(p)
        customer.professions.add(profession)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.name=request.data.get('name',customer.name)
        customer.address=request.data.get('address',customer.address)
        customer.data_sheet_id=request.data.get('data_sheet',customer.data_sheet_id)
        customer.save()
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer=self.get_object()
        customer.delete()
        return Response("object removed")
    @action(detail=True)
    def deactivate(self,request,**kwargs):
        customer=self.get_object()
        customer.active=False

        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    @action(detail=False)
    def deactivate_all(self,request,**kwargs):
        customers=self.get_queryset()
        customers.update(active=False)

        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self,request,**kwargs):
        customers=self.get_queryset()
        customers.update(active=True)

        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    @action(detail=False,methods=['POST'])
    def change_status(self,request,**kwargs):
        #import pdb; pdb.set_trace()
        status=True if request.data['active']=='True' else False
        
        customers=self.get_queryset()
        customers.update(active=status)

        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)



    




class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes=[TokenAuthentication,]
    permission_classes=[IsAdminUser,]

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes=[AllowAny,]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes=[DjangoModelPermissionsOrAnonReadOnly]

