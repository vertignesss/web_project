from django.contrib import admin
from django.db import models
from .models import Card, User, UserCard, Offer, Keyword
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from django.contrib import admin
from .models import export_model_to_pdf
from django import forms


class CardResource(resources.ModelResource):

	class Meta:
		model = Card
	def get_export_queryset(self, request=None):
		return super().get_export_queryset(request)

class KeywordsInline(admin.TabularInline):
	model = Card.keywords.through
	extra = 1

class CardAdmin(ImportExportModelAdmin):
	resource_class = CardResource
	formfield_overrides = { 
		models.TextField: {
		'widget': forms.Textarea(attrs={'cols': 40, 'rows': 10,  'style': 'resize: none;'})
		}, 
		models.AutoField: {'widget': forms.HiddenInput},
	}
	list_display = ('name', 'get_image', 'oracle_text', 'power', 'toughness', "rarity")
	search_fields = ('name', 'oracle_text')
	exclude = ('id',)
	list_filter = ('rarity',)
	inlines = [KeywordsInline]
	list_editable = ('power', 'toughness', 'oracle_text', 'rarity')
	list_per_page = 3
	fieldsets = ( 
		(None, {
		 'fields': ('name', 'image', 'oracle_text', 'rarity') 
		 }), 
		('Creature-specific', { 
			'fields': ('power', 'toughness'),
			'classes':('collapse',)
			}), 
		)
	@admin.display(description="image")
	def get_image(self,obj):
		return obj.image_tag()

class KeywordResource(resources.ModelResource):

	class Meta:
		model = Keyword

class KeywordAdmin(ImportExportModelAdmin):
	resource_class = KeywordResource
	list_display=('name', 'oracle_text')
	search_fields=('name', 'oracle_text')
	formfield_overrides = { 
		models.TextField: {
		'widget': forms.Textarea(attrs={'cols': 30, 'rows': 5, 'style': 'resize: none;'})
		}, 
	}
	exclude = ('id',)
	list_per_page = 15

class UserResource(resources.ModelResource):
	class Meta:
		model = User
	def get_export_queryset(self, request=None):
		return super().get_export_queryset(request)

class UserAdmin(ImportExportModelAdmin):
	search_fields=('login',)
	resource_class = UserResource
	list_display = ('login', 'password')
	list_editable = ('password',)
	exclude = ('id',)
	list_per_page = 15

class OfferResource(resources.ModelResource):
	def dehydrate_user_card(self, offer):
		name = getattr(offer.user_card.user, "login", "unknown")
		card = getattr(offer.user_card.card, "name", "unknown")
		return '%s has %s(s)' % (name, card)
	class Meta:
		model = Offer
		ordering = ("user_card",)



class UserCardResource(resources.ModelResource):
	class Meta:
		model = UserCard

	def get_user(self, usercard):
		return f"Пользователь: {user_card.user.login}"

class OfferInline(admin.TabularInline):
	model = Offer
	extra = 1

class UserCardAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
	resource_class = UserCardResource
	list_display = ('user', 'card')
	raw_id_fields = ('user', 'card')
	inlines = [OfferInline]
	exclude = ('id',)
	list_filter = ('user', 'card')

def download_pdf(modeladmin, request, queryset):
    return export_model_to_pdf(request, queryset)

class CardNameFilter(admin.SimpleListFilter):
    title = ('card name')
    parameter_name = 'card_name'

    
    def lookups(self, request, model_admin): 
    	cards = set([offer.user_card.card for offer in Offer.objects.all()]) 
    	return sorted([(card.id, card.name,) for card in cards], key = lambda card:card[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_card__card__id__exact=self.value())
        return queryset



class OfferAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
	resource_class = OfferResource
	list_display = ['user_card__card', 'user_card__user', 'quantity', 'price', 'whole_price', "published", "user_card__card__rarity"]
	list_filter = (CardNameFilter,)
	fields = ["user_card", "quantity", "price", "published"]
	list_display_links = ('user_card__card', 'user_card__user')
	readonly_fields = ('published',)
	actions = [download_pdf]
	date_hierarchy='published'
	exclude = ('id',)
	list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Card, CardAdmin)

