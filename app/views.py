import re
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from app.models import Contact,ProductItems,MyOrders


def Home(request):
    prod=ProductItems.objects.all()
    context={"prod":prod}
    return render(request, "index.html",context)


def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phon=request.POST.get("num")
        desc=request.POST.get("desc")
        query=Contact(name=name,email=email,phoneno=phon,desc=desc)
        query.save()
        messages.info(request,f"Thank You. We will get back you soon {name}")

    return render(request, "contact.html")


def HandleSignup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        pass1 = request.POST.get("pass1")
        cpass = request.POST.get("pass2")
        if(pass1 != cpass):
            messages.warning(request,"Password is incorrect")
            return redirect("/signup")
        try:
            if User.objects.get(username=email):
                messages.info(request,"Already registered")
                return redirect("/signup")
        except:
            pass

        myuser = User.objects.create_user(email, uname, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request,"Signup Success")
        return redirect("/login")

    return render(request, "signup.html")


def HandleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        myuser = authenticate(username=email, password=pass1)

        if myuser is not None:
            login(request, myuser)
            return redirect("/")

        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/login")

    return render(request, "login.html")


def HandleLogout(request):
    logout(request)
    return redirect("/")


def products(request):
    myprod=ProductItems.objects.all()
    context={"myprod":myprod}
    return render(request,"products.html",context)


def myorders(request):
    if not request.user.is_authenticated:
        messages.warning(request,"You need to be logged in first")
        return redirect("/login")
    prod=ProductItems.objects.all()
    current_user=request.user.username
    items=MyOrders.objects.filter(email=current_user)
    print(items)
    context={"prod":prod,"items":items}
    if request.method =="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        item=request.POST.get("items")
        quan=request.POST.get("quantity")
        address=request.POST.get("address")
        phone=request.POST.get("num")
        print(name,email,item,quan,address,phone)
        price=""
        for i in prod:
            if item==i.prod_name:
                price=i.prod_price

            pass
        newPrice=int(price)*int(quan)
        myquery=MyOrders(name=name,email=email,items=item,address=address,quantity=quan,price=newPrice,phone_num=phone)
        myquery.save()
        messages.info(request,f"Order is Successful")
        return redirect("/orders")
    return render(request,"orders.html",context)




def deleteOrder(request,id):
    print(id)
    query=MyOrders.objects.get(id=id)
    query.delete()
    messages.success(request,"Order Cancelled Successfully..")
    return redirect("/orders")