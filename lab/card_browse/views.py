from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Card, User, UserCard, Offer, Keyword
from .serializers import CardSerializer, UserSerializer, UserCardSerializer, OfferSerializer, KeywordSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
import django_filters
from rest_framework.response import Response
from .forms import OfferForm, SearchForm



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


    @action(methods = ["GET"], detail = False)
    def cards_with_cost(self, request):
        selected_cards = Card.objects.exclude(converted_mana_cost=0)
        serial = CardSerializer(selected_cards, many = True)
        return Response({
            "Карты за хотя бы 1 ману" : serial.data
            })

    @action(methods = ["GET"], detail = False)
    def card_in_descending_cost_order(self, request):
        selected_cards = Card.objects.order_by("-converted_mana_cost")
        serial = CardSerializer(selected_cards, many = True)
        return Response({
            "Карты по убыв. стоимости" : serial.data
            })
    

    @action(methods=["POST", "GET"], detail=True)
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
    @action(methods = ["GET"], detail = False)
    def new_offers(self, request):
        selected_offers = Offer.new.all()
        serial = OfferSerializer(selected_offers, many = True)
        return Response({
            "Новые предложения" : serial.data
            })

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = [SearchFilter]

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class CardList(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'oracle_text']

def offer_list(request, card_id = None):
    if card_id:
        offers = Offer.objects.filter(user_card__card_id = card_id)
    else:
        offers = Offer.new.all()
    return render(request, 'card_browse/offer/list.html', {'offers' : offers})

def offer_detail(request, id):
    offer = get_object_or_404(Offer,
    id=id,
    )
    return render(request,
    'card_browse/offer/detail.html',
    {'offer': offer})

def offer_form(request, pk = None):
    if pk:
        obj = get_object_or_404(Offer, pk=pk)
    else:
        obj = None
    if request.method == 'POST':
        form = OfferForm(request.POST, instance = obj)
        if 'save' in request.POST and form.is_valid:
            form.save(commit = True)
            return redirect('../../form/success')
        elif 'delete' in request.POST and obj:
            obj.delete()
            return redirect('../../form/success')
    else:
        form = OfferForm(instance = obj)
    return render(request, 'card_browse/form/main.html', {'form': form, 'object':obj})



def success(request):
    return render(request, 'card_browse/form/success.html')


def card_list(request):
    query = None
    cards = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            cards = Card.objects.filter(name__icontains=query)
    else:
        form = SearchForm()
        cards = Card.objects.all()
    return render(request, 'card_browse/card/list.html', {'form':form, 'query':query, 'cards' : cards})