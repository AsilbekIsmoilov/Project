from django.contrib import admin

from shop.models import Category, Product, Gallery, Like, Customer, Order, ShippingAddress, OrderProduct, Comment


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    prepopulated_fields = {'slug':('title',)}

class GalleryAdmin(admin.TabularInline):
    model = Gallery
    fk_name = 'product'
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','quantity','size','color','category']
    list_editable = ['price','quantity','size','color']
    list_display_links = ['title']
    prepopulated_fields = {'slug':('title',)}
    inlines = [GalleryAdmin]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Like)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(OrderProduct)
admin.site.register(Comment)