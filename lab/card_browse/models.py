from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from django.utils.html import format_html

RARITY_CHOICES = (
    ("COMMON", "Common"),
    ("UNCOMMON", "Uncommon"),
    ("RARE", "Rare"),
    ("MYTHIC_RARE", "Mythic Rare"),
    )

class Keyword(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    oracle_text = models.CharField(max_length = 500)
    def __str__(self):
        return self.name

class Card(models.Model):
    id = models.IntegerField(primary_key = True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    name = models.CharField(max_length = 50)
    oracle_text = models.CharField(max_length = 500)
    power = models.IntegerField(blank = True, null = True)
    toughness = models.IntegerField(blank = True, null = True)
    mana_cost = models.CharField(max_length = 20, blank = True, null = True)
    color_identity = models.IntegerField()
    converted_mana_cost = models.IntegerField()
    rarity = models.CharField(max_length = 30, choices = RARITY_CHOICES, default = "COMMON")
    keywords = models.ManyToManyField(Keyword, related_name="cards", through="Keywords_On_Cards")
    def image_tag(self): 
        if self.image: 
            return format_html('<img src="{}" width="200" height="270" />'.format(self.image.url)) 
        return "No Image"
    def __str__(self):
        return self.name

    


class Keywords_On_Cards(models.Model):
    card = models.ForeignKey(Card, on_delete = models.CASCADE)
    Keyword = models.ForeignKey(Keyword, on_delete = models.CASCADE)


class User(models.Model):
    id = models.IntegerField(primary_key = True)
    login = models.CharField(max_length = 32, unique = True)
    password = models.CharField(max_length = 32)
    cards = models.ManyToManyField(Card, related_name="users")
    def __str__(self):
        return self.login


class UserCard(models.Model):
    id = models.IntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    card = models.ForeignKey(Card, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.user.__str__() + " has " + self.card.__str__() + "(s)"





class NewOfferManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published__gte=datetime.now()-timedelta(weeks=1))







class Offer(models.Model):
    id = models.AutoField(primary_key = True)
    user_card = models.ForeignKey(UserCard, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    history = HistoricalRecords()
    published = models.DateTimeField(default = timezone.now)

    objects = models.Manager()
    new = NewOfferManager()

    def whole_price(self):
        return self.quantity * self.price


    whole_price.short_description = "Price for All"

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"




def export_model_to_pdf(request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="offers_data.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    data = [["User and Card", "Quantity", "Price"]]  # Заголовки столбцов
    new_queryset = queryset.values("user_card", "quantity", "price")
    print(new_queryset)
    for q in new_queryset:
        data.append([UserCard.objects.get(id = q['user_card']).__str__(), q['quantity'], q['price']])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response
