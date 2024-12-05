from django.contrib import admin

from .models import Card, User, UserCard, Offer, Keyword
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field

class CardResource(resources.ModelResource):

	class Meta:
		model = Card
	def get_export_queryset(self, request=None):
		return super().get_export_queryset(request)

class CardAdmin(ImportExportModelAdmin):
	resource_class = CardResource
	list_display = ('name', 'oracle_text', 'power', 'toughness')
	search_fields = ('name', 'oracle_text', 'power', 'toughness')

class OfferResource(resources.ModelResource):
	def dehydrate_user_card(self, offer):
		name = getattr(offer.user_card.user, "login", "unknown")
		card = getattr(offer.user_card.card, "name", "unknown")
		return '%s has %s(s)' % (name, card)
	class Meta:
		model = Offer


class OfferAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
	resource_class = OfferResource
	list_display = ('user_card', 'quantity', 'price')
	list_filter = ('price',)
	fields = ["user_card", "quantity", "price"]
	list_display_links = ('user_card',)
	list_editable = ('quantity', 'price')

class UserCardResource(resources.ModelResource):
	class Meta:
		model = UserCard

	def get_user(self, usercard):
		return f"Пользователь: {user_card.user.login}"

class UserCardAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
	resource_class = UserCardResource
	list_display = ('user', 'card')
admin.site.register(User)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Keyword)
admin.site.register(Card, CardAdmin)