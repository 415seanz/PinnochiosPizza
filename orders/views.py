from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.core import serializers
from orders import models as orders_models


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
        #temp = serialize("json", User.objects.all(), fields=("username"))
        #print(temp)
        temp2 = User.objects.all().values_list("username")
        #print(temp2)
        list = []
        for i in temp2:
            list.append(i[0])
        #print(list)
        context = {}
        context["message"] = "Register Below"
        context["users"] = list
        return render(request, "orders/register.html", context)

def category_view(request,category="subs"):
    if request.method == "GET":
        itemNames = orders_models.Item.objects.distinct().filter(category__slug=category).values('name')
        json_serializer = serializers.get_serializer("json")()
        items = json_serializer.serialize(orders_models.Item.objects.filter(category__slug=category))
        sizes = json_serializer.serialize(orders_models.Size.objects.all())
        additions = json_serializer.serialize(orders_models.Addition.objects.all())
        toppings = json_serializer.serialize(orders_models.Topping.objects.all())
        return render(request, "orders/category.html", {"message": "Category Page", "category": category, "items": items, "itemNames": itemNames, "sizes": sizes, "additions": additions, "toppings": toppings})
    else:
        print(request.POST)
        item = orders_models.Item.objects.get(pk=request.POST["itemIdInput"])
        maxAdditions = orders_models.Addition.objects.filter(item__pk=item.pk).count()
        maxToppings = item.maxToppings
        orderItem = orders_models.OrderItem(item=item, orderItemPrice=request.POST["itemPrice"])
        orderItem.save(commit=False)

        #add each addition to the orderItem
        for i in range(maxAdditions):
            name = "check_" + i
            try:
                addition = orders_models.Addition.objects.get(pk=request.POST[name])
                orderItem.additions.add(addition)
            except:
                pass

        #add each topping to the orderItem
        if maxToppings != None:
            for j in range(maxToppings):
                topnum = "topping" + j
                topping = orders_models.Topping.objects.get(pk=request.POST[topnum])
                orderItem.toppings.add(topping)

        orderItem.save()
        orderItem.save_m2m()

        return HttpResponseRedirect(reverse("index"))