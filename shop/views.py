import stripe
from django.contrib import messages
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from shop.forms import LoginForm, RegisterForm, CustomerForm, ShippingAddressForm, CommentForm
from shop.models import Product, Category, Like, ShippingAddress, Customer, Comment
from shop.utils import get_cart_data, CartForUser


# Create your views here.


class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    template_name = 'shop/index.html'
    extra_context = {
        "title": "Shopping Time"
    }

    def get_queryset(self):
        categories = Category.objects.all()
        data = []
        for category in categories:
            products = category.products.all()
            data.append({
                "title": category.title,
                "products": products
            })
        return data


class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_detail.html'
    paginate_by = 1

    extra_context = {
        "title": "Shop List"
    }

    def get_queryset(self):
        search_field = self.request.GET.get('q')
        if search_field:
            category = Category.objects.get(slug=self.kwargs['slug'])
            products = category.products.filter(title__icontains=search_field)
            return products
        sort_field = self.request.GET.get('sort')
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = category.products.all()
        if sort_field:
            products = products.order_by(sort_field)
        return products


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    extra_context = {
        "title": "Product Detail",
    }

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product =Product.objects.get(slug=self.kwargs['slug'])
        context['comments'] = Comment.objects.filter(product=product)
        context['comment_form'] = CommentForm()
        return context


def login_register(request):
    context = {
        "title": "Auth User",
        "login_form": LoginForm(),
        "register_form": RegisterForm(),
    }
    return render(request, "shop/login_register.html", context)


def user_register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, "Successful created")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
    return redirect("login_register")


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("index")
    else:
        messages.error(request, "Invalid username or password")
        return redirect("login_register")


def user_logout(request):
    logout(request)
    return redirect("index")


class LikeView(ListView):
    model = Like
    context_object_name = 'products'
    template_name = 'shop/product_like.html'

    extra_context = {
        "title": "Likes Page"
    }

    def get_queryset(self):
        user = self.request.user
        likes = Like.objects.filter(user=user)
        products = [i.product for i in likes]
        return products


def user_like(request, product_slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product_slug)
    if user:
        user_products = Like.objects.filter(user=user)
        if product in [i.product for i in user_products]:
            like_product = Like.objects.get(user=user, product=product)
            like_product.delete()
        else:
            Like.objects.create(user=user, product=product)
    next_page = request.META.get("HTTP_REFERER", 'index')
    return redirect(next_page)


def cart(request):
    cart_info = get_cart_data(request)
    context = {
        "products": cart_info['products'],
        "order": cart_info['order'],
        "total_price": cart_info['cart_total_price'],
        "total_quantity": len(cart_info['products']),
        "customer_form": CustomerForm,
        "address_form": ShippingAddressForm,
        "title": "Cart"
    }
    return render(request, 'shop/cart.html', context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForUser(request, product_id, action)
        return redirect("cart")
    else:
        messages.error(request, 'You are not registered yet')
        return redirect("login_register")


def payment(request):
    from config import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.name = customer_form.cleaned_data['name']
            customer.email = customer_form.cleaned_data['email']
        address_form = ShippingAddressForm(data=request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "USD",
                        "product_data": {
                            "name": "Product of Coza Store"
                        },
                        "unit_amount": int(total_price)
                    },
                    'quantity': total_quantity
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('success'))
        )
    return redirect(session.url, 303)


def success_payment(request):
    context = {
        "title":"Success Page"
    }
    return render(request, 'shop/success.html', context)

def save_comment(request, product_id):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.product = Product.objects.get(pk=product_id)
        comment.save()
    else:
        pass
    next_page = request.META.get("HTTP_REFERER", 'product_detail')
    return redirect(next_page, product_id)
