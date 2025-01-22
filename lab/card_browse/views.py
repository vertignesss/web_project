from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from .models import Card, User, UserCard, Offer, Keyword, CardFilter, OfferFilter, UserFilter
from .serializers import CardSerializer, UserSerializer, UserCardSerializer, OfferSerializer, KeywordSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
import django_filters
from rest_framework.response import Response
from .forms import OfferForm, SearchForm
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import render_to_string

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    search_fields = ["name", "oracle_text"]
    filter_backends = [DjangoFilterBackend] 
    filterset_class = CardFilter

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
    filter_backends = [DjangoFilterBackend] 
    filterset_class = UserFilter

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
    filter_backends = [SearchFilter, DjangoFilterBackend] 
    filterset_class = OfferFilter

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
        name = Card.objects.filter(id=card_id)[0].name
    else:
        offers = Offer.objects.all()
        name = None
    return render(request, 'card_browse/offer/list.html', {'offers' : offers, 'card_id':name})

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
            return redirect('offer_list')
        elif 'delete' in request.POST and obj:
            obj.delete()
            return redirect('offer_list')
    else:
        form = OfferForm(instance = obj)
    return render(request, 'card_browse/form/main.html', {'form': form, 'object':obj})



def success(request):
    return render(request, 'card_browse/form/success.html')

def get_cards_context(request, widget=False):
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
    if widget:
        cards = cards[:4]
    return {'form':form, 'query':query, 'cards' : cards}

def card_list(request):
    
    return render(request, 'card_browse/card/list.html', get_cards_context(request))

def card_by_oracle(request, oracle): 
    cards = Card.objects.filter(oracle_text__icontains=oracle) 
    return render(request, 'card_browse/card/list.html', {'form': SearchForm(), 'query':None, 'cards':cards})

def get_latest_offers_context(count = None):
    if count:
        latest_offers = Offer.objects.order_by('-published')[:3]
    else:
        latest_offers = Offer.objects.order_by('-published') 
    avg = latest_offers.aggregate(Avg('price'))['price__avg']
    return {'latest_offers':latest_offers, 'avg_price':avg}



def latest_offers(request): 
    return render(request, 'card_browse/offer/latest_offer.html', get_latest_offers_context())

def main_page(request):
    latest_widget = render_to_string('card_browse/offer/latest_offer_widget.html', context=get_latest_offers_context(3))
    card_widget = render_to_string('card_browse/card/list_widget.html', context={**request.GET, **get_cards_context(request, True)})
    offer_widget = render_to_string('card_browse/offer/list_widget.html', context={'offers' : Offer.objects.all()[:3], 'card_id':None})
    return render(request, 'card_browse/index.html', {'latest_widget' : latest_widget, 'card_widget':card_widget, 'offer_widget':offer_widget})