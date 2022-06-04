# MODELOS

from django.db import models
from dataclasses import fields
#from users.models import User
from accounts.models import Account

# Create your models here.

# Éste es el modelo de Conceptos.
class Concept(models.Model):
   concept = models.CharField(max_length=200, verbose_name='Concepto')
   type_mov = [
       ('gasto','Gasto'),
       ('ingreso','Ingreso')
    ]
   type_movement = models.CharField(choices=type_mov, max_length=10, verbose_name='Tipo de movimiento')
   type_clasif = [
       ('fijo','Fijo'),
       ('variable','Variable')
   ]
   type_clasification = models.CharField(choices=type_clasif, max_length=10, verbose_name='Tipo de clasificación')
   #user = models.ForeignKey(User, on_delete=models.CASCADE)
   status_delete = models.BooleanField(default=False)


class Meta:
    db_table = 'concepts'

# Éste es elmodelo de Movimientos.
class Move(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre del movimiento')
    description = models.CharField(max_length=200, blank=True, verbose_name= 'Descripcion del movimiento')
    day = models.DateField(verbose_name='Dia del movimiento')
    amount = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Importe del movimiento')
    #imagen pendiente
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    status_delete = models.BooleanField(default=False)


class Meta:
    db_table= 'moves'

# Éste es el modelo de Recursos.
class Style(models.Model):
    color = models.CharField(max_length=50, verbose_name='Color')
    icon = models.CharField(max_length=50, verbose_name='Icono')
    status_delete = models.BooleanField(default=False)

class Meta:
    db_table= 'styles'

# Éste es el modelo Movimietntos_Recursos.
class Move_Style(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)

class Meta:
    db_table= 'move_styles'


# Éste es el modelo Conceptos_Recursos
class Concept_Style(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)

class Meta:
    db_table= 'concept_styles'

# SERIALIZERS

from importlib.resources import Resource
from django.forms import DateInput, ValidationError
from rest_framework import serializers
from api.move.models import Concept_Style, Move_Style, Style

from move.models import Concept, Move


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        exclude = ('status_delete',)
    
 
class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model= Move
        exclude = ('status_delete',)

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model= Style
        exclude = ('status_delete',)

class Move_StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model= Move_Style

class Concept_StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model= Concept_Style

        
# VIEWS

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from move.models import Concept, Move, Style, Concept_Style, Move_Style
from move.serializers import ConceptSerializer, MoveSerializer

# Create your views here.

# Esta clase es para crear un nuevo concepto
class RegisterConceptView(APIView):
    permission_classes=(AllowAny,)

    def post(self, request):
        data = request.data
        serializer = ConceptSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Esta clase es para registrar un movimiento (ingreso o gasto)
class RegisterMoveView(APIView):
    permission_classes=(AllowAny,)

    def post(self, request):
        data = request.data
        serializer = MoveSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Esta clase es para listar los movimientos
class ListMoveView(APIView):
    permission_classes= (AllowAny,)

    def get(self, request):
        move_list = Move.objects.all()
        serializer = MoveSerializer(move_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# URLS

from django.urls import path
from move import views

urlpatterns = [
   path('registerConcept/', views.RegisterConceptView.as_view(),),
   path('registerMove/', views.RegisterMoveView.as_view(),),
   path('listMove/', views.ListMoveView.as_view(),),
  
]
