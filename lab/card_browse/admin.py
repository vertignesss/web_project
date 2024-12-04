from django.contrib import admin

from .models import Card, User, UserCard, Offer, Keyword

admin.site.register(Card)
admin.site.register(User)
admin.site.register(UserCard)
admin.site.register(Offer)
admin.site.register(Keyword)
