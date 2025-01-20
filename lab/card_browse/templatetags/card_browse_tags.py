from django import template
from ..models import Offer
register = template.Library()
@register.simple_tag
def total_new_offers():
	return Offer.new.count()