from django import template
from shop.models import Category, Gallery, Like

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_filters():
    filters = [
        {
            "title": "Price",
            "filters": [
                ['-price', 'high to low'],
                ['price', 'low to high']
            ]
        },

        {
            "title": "Size",
            "filters": [
                ['-size', 'high to low'],
                ['size', 'low to high']
            ]
        },

        {
            "title": "Color",
            "filters": [
                ['color', 'A - Z'],
                ['-color', 'Z - A']
            ]
        },

        {
            "title": "Name",
            "filters": [
                ['title', 'A - Z'],
                ['-title', 'Z - A']
            ]
        }
    ]
    return filters


@register.simple_tag()
def get_like(user):
    likes = Like.objects.filter(user=user)
    products = [i.product for i in likes ]
    return products
