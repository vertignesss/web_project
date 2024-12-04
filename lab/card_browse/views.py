from django.shortcuts import render
from rest_framework import viewsets
from .models import User, UserAddress, Courier, Restaurant, RestaurantGroup, RestaurantDish, RestaurantAttribute, Order, OrderDish, OrderAttribute, Ticket
from .serializers import UserSerializer, UserAddressSerializer, CourierSerializer, RestaurantSerializer, RestaurantGroupSerializer, RestaurantDishSerializer, RestaurantAttributeSerializer, OrderSerializer, OrderDishSerializer, OrderAttributeSerializer, TicketSerializer


from .models import Card, User, UserCard, Offer, Keyword


class CardView(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCardView(viewsets.ModelViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer


class OfferView(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class KeywordView(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
