from django.shortcuts import render
from rest_framework import viewsets, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Card, User, UserCard, Offer, Keyword
from .serializers import CardSerializer, UserSerializer, UserCardSerializer, OfferSerializer, KeywordSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
import django_filters
from rest_framework.response import Response




class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    search_fields = ["name", "oracle_text"]


    @action(methods = ["GET"], detail = False)
    def w_or_u_not_hasty_cards(self, request):
        selected_cards = Card.objects.filter(
            (Q(color_identity__gte=16) |
            Q(color_identity__gte=8) ) & 
            ~Q(oracle_text__contains='haste')
            )
        serial = CardSerializer(selected_cards, many = True)

        return Response({
            "Красные или синие карты без haste" : serial.data,
            })

    @action(methods = ["GET"], detail = False)
    def paid_cards_with_tough_or_pw(self, request):
        selected_cards = Card.objects.filter(
            (~Q(power=None) |
            ~Q(toughness=None)) &
            ~Q(converted_mana_cost=0)
            )
        serial = CardSerializer(selected_cards, many = True)

        return Response({
            "Карты со стоимостью, у которых есть сила или здоровье" : serial.data
            })

    @action(methods=["POST"], detail=True)
    def change_card(self, request, pk=None):

        card = self.get_object()
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Карта изменена."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """
        Возвращает сериализатор, который нужно использовать для действия "change_price".
        """
        if self.action == "change_oracle":
            return CardSerializer
        return super().get_serializer_class()



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


class CardList(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'oracle_text']