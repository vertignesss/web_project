from django.shortcuts import render
from rest_framework import viewsets

from .models import Card, User, UserCard, Offer, Keyword
from .serializers import CardSerializer, UserSerializer, UserCardSerializer, OfferSerializer, KeywordSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCardViewSet(viewsets.ModelViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
