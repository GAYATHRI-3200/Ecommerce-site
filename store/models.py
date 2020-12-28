from django.db import models
from django.contrib.auth.models import User
# Create your models here.
     	
		

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	

	def __str__(self):
		return self.name.__str__()



class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	digital = models.BooleanField(default=False, null=True, blank=False)
	image = models.ImageField(null=True, blank=False)
	
	def __str__(self):
		return self.name.__str__()

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
		
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id) #cause integer

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = (sum([item.get_total for item in orderitems]))
		return total
	
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = (sum([item.quantity for item in orderitems]))
		return total

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping
	


	

class OrderItem(models.Model):#to get the product added in the cart
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)#here foreign key is used cause many products can be added to the cart
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)#single order can have multiple ordered items, its a child of order
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = (self.product.price * self.quantity)
		return total
		
		
	



class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)#to store the address to validate
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address.__str__()

#class Contact(models.Model):
#    name = models.CharField(max_length=50)
#    email = models.EmailField()
#    message = models.TextField()




	
