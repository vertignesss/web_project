"""
URL configuration for lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from card_browse import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.SimpleRouter()
router.register('users', views.UserViewSet)
router.register('users_cards', views.UserCardViewSet)
router.register('cards', views.CardViewSet)
router.register('keywords', views.KeywordViewSet)
router.register('offers', views.OfferViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('offer/<int:card_id>', views.offer_list, name="offer_list"),
    path('card/<str:oracle>', views.card_by_oracle, name="card_list"),
    path('offer/', views.offer_list, name="offer_list"),
    path('offer/detail/<int:id>', views.offer_detail, name="offer_detail"),
    path('offer/create', views.offer_form, name="offer_form"),
    path('offer/create/<int:pk>', views.offer_form, name="offer_form_edit"),
    path('form/success', views.success, name="success"),
    path('__debug__/', include('debug_toolbar.urls')),
    path("card/", views.card_list, name="card_list"),
    path('offer/latest_offer', views.latest_offers, name='latest_offers'),
    path("", views.main_page, name="main_page")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)