from django.contrib import admin

from .models import Card, User, UserCard, Offer, Keyword
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from django.contrib import admin
from .models import export_model_to_pdf



class CardResource(resources.ModelResource):

	class Meta:
		model = Card
	def get_export_queryset(self, request=None):
		return super().get_export_queryset(request)

class CardAdmin(ImportExportModelAdmin):
	resource_class = CardResource
	list_display = ('name', 'get_image', 'oracle_text', 'power', 'toughness', "rarity")
	search_fields = ('name', 'oracle_text')
	list_filter = ('rarity',)
	@admin.display(description="image")
	def get_image(self,obj):
		return obj.image_tag()

class UserResource(resources.ModelResource):

	class Meta:
		model = User
	def get_export_queryset(self, request=None):
		return super().get_export_queryset(request)

class UserAdmin(ImportExportModelAdmin):
	resource_class = UserResource
	list_display = ('login', 'password')
	filter_horizontal = ('cards',)

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

def download_pdf(modeladmin, request, queryset):
    return export_model_to_pdf(request, queryset)

class OfferAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
	resource_class = OfferResource
	list_display = ['user_card', 'quantity', 'price', 'whole_price', "published", "user_card__card__rarity"]
	list_filter = ('price',)
	fields = ["user_card", "quantity", "price", "published"]
	list_display_links = ('user_card',)
	readonly_fields = ('published',)
	list_editable = ('quantity', 'price')
	actions = [download_pdf]
	date_hierarchy='published'


admin.site.register(User, UserAdmin)
admin.site.register(UserCard, UserCardAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Keyword)
admin.site.register(Card, CardAdmin)

