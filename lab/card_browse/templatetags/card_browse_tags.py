from django import template
from ..models import Offer
register = template.Library()
@register.simple_tag
def total_offers():
	return Offer.objects.count()