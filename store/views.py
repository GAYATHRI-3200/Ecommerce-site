from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder

from .models import * 


from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
#from .forms import OrderForm, CreateUserForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, OrderForm
from . forms import ContactForm
from django.conf import settings
from . import autoreply
def index(request):
	context = {}
	return render(request, 'store/index.html', context)	

def blog(request):
	context = {}
	return render(request, 'store/blog.html', context)
def Sblog(request):
	context = {}
	return render(request, 'store/single-blog.html', context)			



def store(request):

	data= cartData(request)
	cartItems= data['cartItems']	
	products = Product.objects.all()
	 #to get the product title and price from the data base(.models we used cause of the same dir)
	context = {'products' :products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	data= cartData(request)
	cartItems= data['cartItems']
	order= data['order']
	items= data['items']
	#if request.user.is_authenticated:
	#	customer = request.user.customer
	#	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	#	items = order.orderitem_set.all()
	#else:
		#Create empty cart for now for non-logged in user
	#	items = []
	#	order = {'get_cart_total':0, 'get_cart_items':0}

	
	
	context = {'items' :items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)



def checkout(request):
	
	data= cartData(request)
	cartItems= data['cartItems']
	order= data['order']
	items= data['items']
	context = {'items' :items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()


	return JsonResponse('item was added ', safe=False)
	


def processOrder(request):

	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		
		

	else:
		customer, order = guestOrder(request, data)
		

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
			order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)


	return JsonResponse('payment complete!!!', safe=False)

#def register(request):
#	context = {}
#	if request.POST:
#		form = UserRegisterForm(request.POST)
#		if form.is_valid():
#			form.save()
#			email = form.cleaned_data.get('email')
#			raw_password = form.cleaned_data.get('password1')
#			user = form.save()
#			#user = authenticate(email=email, password=raw_password)
#			#login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#			login(request,user)
#			return redirect('home')
#		else:
#			context['registration_form'] = form
#	else: 
#		form = UserRegisterForm() 
#		
#		context['registration_form'] = form
#	return render(request, 'store/register.html',context)	

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form, 'title': 'Register'})

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('store')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')

			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)
			print('user \n',user)

			if user:
				login(request, user)
				return redirect('store')
			else:
				messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def contact_form(request):
    """about page"""
    title = "Contact"
    form = ContactForm(request.POST or None) #form handling by view.
    confirmation = None

    if form.is_valid():
        user_name = form.cleaned_data['Username']
        user_message = form.cleaned_data['Message']
        emailsub = user_name + " tried contacting you on online gadgets shopping."
        emailFrom = form.cleaned_data['UserEmail']
        emailmessage = '%s %s user email: %s' %(user_message, user_name, emailFrom)
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(emailsub, emailmessage, emailFrom, list(emailTo), fail_silently=True)
        #Autoreply.
        autoreply.autoreply(emailFrom)
        title = "Thanks."
        confirmation = "We will get right back to you."
        form = None

    context = {'title':title, 'form':form, 'confirmation':confirmation,}
    template = 'contact.html'
    return render(request,'store/contact.html',context)
