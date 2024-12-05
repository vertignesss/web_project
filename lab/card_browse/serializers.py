from rest_framework import serializers
from .models import Card, User, UserCard, Offer, Keyword

class CardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Card
		fields = "__all__"
	def validate(self, attrs):
		power = attrs.get("power")
		toughness = attrs.get("toughness")
		color_identity = attrs.get("color_identity")
		if color_identity < 0 or color_identity > 31:
			raise serializers.ValidationError("Color identity должна быть в диапазоне от 0 до 31")
		if (power is not None and power < 0) or (toughness is not None and toughness < 0):
			raise serializers.ValidationError("Здоровье и сила должны быть неотрицательными")
		return attrs


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User 
		fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
	class Meta:
		model = Keyword
		fields = "__all__"


def quantity_validator(quantity):
	if quantity < 1:
		raise serializers.ValidationError("Кол-во карт должно быть положительным")
	return quantity

class OfferSerializer(serializers.ModelSerializer):
	class Meta:
		quantity = serializers.IntegerField(validators = [quantity_validator])
		model = Offer
		fields = "__all__"
	def validate(self, attrs):
		quantity = attrs.get("quantity")
		price = attrs.get("price")
		if price < 1:
			raise serializers.ValidationError("Цена должна быть положительной")
		
		return attrs


class UserCardSerializer(serializers.ModelSerializer):
	class Meta:
		quantity = serializers.IntegerField(validators = [quantity_validator])
		model = UserCard
		fields = "__all__"
