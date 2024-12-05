from django.contrib import admin

from .models import Card, User, UserCard, Offer, Keyword
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Card)
admin.site.register(User)
admin.site.register(UserCard)
admin.site.register(Offer, SimpleHistoryAdmin)
admin.site.register(Keyword)
