from django.db import models
from django.urls import reverse

class Card(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    oracle_text = models.CharField(max_length = 500)
    power = models.IntegerField(blank = True, null = True)
    toughness = models.IntegerField(blank = True, null = True)
    mana_cost = models.CharField(max_length = 20, blank = True, null = True)
    color_identity = models.IntegerField()
    converted_mana_cost = models.IntegerField()
    def __str__(self):
        return self.name

    
class Keyword(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    oracle_text = models.CharField(max_length = 500)
    cards = models.ManyToManyField(Card)
    def __str__(self):
        return self.name


class User(models.Model):
    id = models.IntegerField(primary_key = True)
    login = models.CharField(max_length = 32, unique = True)
    password = models.CharField(max_length = 32)
    def __str__(self):
        return self.login


class UserCard(models.Model):
    id = models.IntegerField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    card = models.ForeignKey(Card, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.user.__str__() + " has " + self.card.__str__() + "(s)"







class Offer(models.Model):
    id = models.IntegerField(primary_key = True)
    user_card = models.ForeignKey(UserCard, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()




