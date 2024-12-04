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
		if color_identity < 0 or color_identity > 31
			raise serializers.ValidationError("Color identity должна быть в диапазоне от 0 до 31")
		if power < 0 or toughness < 0
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


class OfferSerializer(serializers.ModelSerializer):
	class Meta:
		model = Offer
		fields = "__all__"
	def validate(self, attrs):
		quantity = attrs.get("quantity")
		price = attrs.get("price")
		if price < 1
			raise serializers.ValidationError("Цена должна быть положительной")
		if quantity < 1
			raise serializers.ValidationError("Кол-во карт должно быть положительным")
		return attrs


class UserCardSerialezer(serializers.ModelSerializer):
	class Meta:
		model = UserCard
		fields = "__all__"
	def validate_quantity(self, value):
		if value < 1:
			raise serializers.ValidationError("Кол-во карт должно быть положительным")
		return value
