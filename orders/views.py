from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.core import serializers
from orders import models as orders_models
from decimal import Decimal
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
      return render(request, "orders/login.html", {"message": "Please log in below"})
    context = {
      "user": request.user,
      "categories": orders_models.Category.objects.all()
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          return HttpResponseRedirect(reverse("index"))
        else:
          return render(request, "orders/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "orders/login.html", {"message": "Please log in below"})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

def register_view(request):
    # if user is submitting form, save user and authenticate automatically
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST["firstName"]
        user.last_name = request.POST["lastName"]
        user.save()
        logged = authenticate(request, username=username, password=password)
        login(request, logged)
        return HttpResponseRedirect(reverse("index"))
    else:
        #gather list of usernames and present form with that context
        temp2 = User.objects.all().values_list("username")
        list = []
        for i in temp2:
            list.append(i[0])
        context = {}
        context["message"] = "Register Below"
        context["users"] = list
        return render(request, "orders/register.html", context)

def category_view(request,category="subs"):
    if not request.user.is_authenticated:
      return render(request, "orders/login.html", {"message": "Please log in below"})
    #send models to javascript
    if request.method == "GET":
        itemNames = orders_models.Item.objects.distinct().filter(category__slug=category).values('name')
        json_serializer = serializers.get_serializer("json")()
        items = json_serializer.serialize(orders_models.Item.objects.filter(category__slug=category))
        categoryName = orders_models.Category.objects.distinct().filter(slug=category).values('name')[0]["name"]
        sizes = json_serializer.serialize(orders_models.Size.objects.all())
        additions = json_serializer.serialize(orders_models.Addition.objects.all())
        toppings = json_serializer.serialize(orders_models.Topping.objects.all())
        return render(request, "orders/category.html", {"message": "Category Page", "category": category, "items": items, "itemNames": itemNames, "sizes": sizes, "additions": additions, "toppings": toppings, "categoryName": categoryName})

    #take values from form and save order item
    else:
        item = orders_models.Item.objects.get(pk=request.POST["itemIdInput"])
        maxAdditions = orders_models.Addition.objects.filter(item__pk=item.pk).count()
        maxToppings = item.maxToppings
        orderItem = orders_models.OrderItem(item=item, orderItemPrice=request.POST["itemPrice"], user=request.user)
        orderItem.save()

        #add each addition to the orderItem
        for i in range(maxAdditions):
            name = "check_" + str(i)
            try:
                addition = orders_models.Addition.objects.get(pk=request.POST[name])
                orderItem.additions.add(addition)
            except:
                pass

        #add each topping to the orderItem
        if maxToppings != None:
            for j in range(maxToppings):
                topnum = "topping_" + str(j)
                topping = orders_models.Topping.objects.get(pk=request.POST[topnum])
                orderItem.toppings.add(topping)

        return HttpResponseRedirect(reverse("cart"))

def cart_view(request):
    if not request.user.is_authenticated:
      return render(request, "orders/login.html", {"message": "Please log in below"})

    #determin user and price
    user = request.user.pk
    items = orders_models.OrderItem.objects.filter(user=user,order__isnull=True)
    price = Decimal(0.00);
    for item in items:
        price += Decimal(item.orderItemPrice)

    # if it's a get request, show the cart with that user's open items
    if request.method == "GET":
        return render(request, "orders/cart.html",{"items": items, "price": price})

    else:
        #create order and redirect to order screen
        action = request.POST["action"]
        if action == "placeOrder":
            order = orders_models.Order(user=request.user, timestamp=timezone.now(), status="Order Placed", totalPrice=price)
            order.save()
            for item in items:
                item.order = order
                item.save()
            orderList = orders_models.Order.objects.filter(user=user).order_by('-timestamp')
            return render(request, "orders/orders.html",{"orders": orderList})
        else:
            orders_models.OrderItem.objects.filter(pk=action).delete()
            items = orders_models.OrderItem.objects.filter(user=user,order__isnull=True)
            price = Decimal(0.00);
            for item in items:
                price += Decimal(item.orderItemPrice)
            return render(request, "orders/cart.html",{"items": items, "price": price})

def orders_view(request):
    if not request.user.is_authenticated:
      return render(request, "orders/login.html", {"message": "Please log in below"})

    #display orders
    user = request.user.pk
    orders = orders_models.Order.objects.filter(user=user).order_by('-timestamp')
    return render(request, "orders/orders.html",{"orders": orders})

#@staff_member_required
def staff_view(request):
    if not request.user.is_authenticated:
      return render(request, "orders/login.html", {"message": "Please log in below"})

    json_serializer = serializers.get_serializer("json")()
    users = json_serializer.serialize(User.objects.all().only('email'))

    if request.method == "GET":
        status_values = orders_models.Order.objects.distinct().values('status')
        json_serializer = serializers.get_serializer("json")()
        orders = json_serializer.serialize(orders_models.Order.objects.all().order_by('-timestamp'))
        return render(request, "orders/staff.html",{"orders": orders, "statuses": status_values, "users": users})

    else:
        action = request.POST["actionInput"]
        ordernum = request.POST["ordernumInput"]

        #if user clicks delete, delete appropriate order
        if action == "delete":
            orders_models.Order.objects.filter(pk=ordernum).delete()
            status_values = orders_models.Order.objects.distinct().values('status')
            json_serializer = serializers.get_serializer("json")()
            orders = json_serializer.serialize(orders_models.Order.objects.all().order_by('-timestamp'))
            return render(request, "orders/staff.html",{"orders": orders, "statuses": status_values, "users": users})

        #if user clicks mark complete, complete appropriate order
        elif action == "complete":
            order = orders_models.Order.objects.get(pk=ordernum)
            order.status = "Complete"
            order.save()
            status_values = orders_models.Order.objects.distinct().values('status')
            json_serializer = serializers.get_serializer("json")()
            orders = json_serializer.serialize(orders_models.Order.objects.all().order_by('-timestamp'))
            return render(request, "orders/staff.html",{"orders": orders, "statuses": status_values, "users": users})

        #if user clicks view, open order and show details
        elif action == "view":
            url = "/staff/" + ordernum
            return HttpResponseRedirect(url)

#@staff_member_required
def vieworder_view(request, ordernum=1):

    if not request.user.is_authenticated:
      return render(request, "orders/login.html", {"message": "Please log in below"})

    if request.method == "POST" and request.POST["action"] == "deleteOrder":
          orders_models.Order.objects.filter(pk=ordernum).delete()

    elif request.method == "POST" and request.POST["action"] == "completeOrder":
        order = orders_models.Order.objects.get(pk=ordernum)
        order.status = "Complete"
        order.save()

    items = orders_models.OrderItem.objects.filter(order=ordernum)
    orderStatus = orders_models.Order.objects.get(pk=ordernum).status
    price = Decimal(0.00);
    for item in items:
        price += Decimal(item.orderItemPrice)
    return render(request, "orders/staff/vieworder.html", {"ordernum": ordernum, "items": items, "price": price, "orderStatus": orderStatus})
