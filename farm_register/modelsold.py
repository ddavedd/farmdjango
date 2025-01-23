from django.db import models

# Create your models here.
class Item(models.Model):
   id = models.AutoField(primary_key=True) 
   name = models.CharField(max_length=200)

   def __str__(self):
      return self.name
      
class Product(models.Model):
   id = models.AutoField(primary_key=True)
   item = models.ForeignKey(Item, on_delete=models.CASCADE,)
   item_count = models.FloatField()
   name = models.CharField(max_length=200)
   tax_rate_nonedible = models.BooleanField()
   enabled = models.BooleanField()
   TYPE_OF_PRODUCT = (
      ("SP", "Set Price"),
      ("WT", "By Weight"),
      ("PM", "Premarked"),
   )
   product_type = models.CharField(max_length=2, choices=TYPE_OF_PRODUCT)
   color = models.CharField(max_length=100, default="grey")
   
   def current_price(self):
      # Get the products in order of newest to oldest
      x = ProductPrice.objects.filter(product_id__exact=self.id).order_by('-time')
      if x is None:
         return "No price set"
      else:
         # return the newest entry
         print("-----------")
         print(x)
         print(self)
         print("-----------")
         return x[0].price
   
   def __str__(self):
      return self.name
      
class Category(models.Model):
   id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=200)
   color = models.CharField(max_length=100, default="grey")
   #order_number = models.IntegerField()
   enabled = models.BooleanField(default="True")
   
   def __str__(self):
      return self.name
      
class ProductCategory(models.Model):
   id = models.AutoField(primary_key=True)
   product = models.ForeignKey(Product,on_delete=models.CASCADE,)
   category = models.ForeignKey(Category,on_delete=models.CASCADE,)

   def __str__(self):
      return self.product.__str__() + " -> " + self.category.__str__()

class ProductPrice(models.Model):
   id = models.AutoField(primary_key=True)
   product = models.ForeignKey(Product,on_delete=models.CASCADE,)
   price = models.FloatField()
   time = models.DateTimeField(auto_now=True)
   
   def __str__(self):
      return self.product.__str__() + " $" + str(self.price) + " set: " + str(self.time)
   
class Deal(models.Model):
   id = models.AutoField(primary_key=True)
   product = models.ForeignKey(Product,on_delete=models.CASCADE,)
   product_count = models.IntegerField()
   discount = models.FloatField()
   time = models.DateTimeField(auto_now=True)
   enabled = models.BooleanField()

   def __str__(self):
      return str(self.product_count) + " " + self.product.__str__()
   
#class DealPrice(models.Model):
#   deal = models.ForeignKey(Deal)
#   price = models.FloatField()
#   time = models.DateTimeField(auto_now=True)
#
#   def __unicode__(self):
#      return self.deal.__unicode__() + " for " + str(self.price)
      
class TransactionTotal(models.Model):
   id = models.AutoField(primary_key=True)
   total = models.FloatField()
   subtotal = models.FloatField()
   edible_tax = models.FloatField()
   nonedible_tax = models.FloatField()
   timestamp = models.DateTimeField(auto_now=True)
   cashier = models.CharField(max_length=100)
   transaction_time = models.IntegerField()
   location = models.CharField(max_length=100, default="stand")
   transaction_type = models.CharField(max_length=100, default="Unknown")
   
   def __str__(self):
      return "Total: %.2f Subtotal %.2f Ed Tax %.2f Noned Tax %.2f %s" % \
      (self.total, self.subtotal, self.edible_tax, self.nonedible_tax, str(self.timestamp))
   
class TransactionItem(models.Model):
   id = models.AutoField(primary_key=True)
   transaction = models.ForeignKey(TransactionTotal,on_delete=models.CASCADE,)
   is_product = models.BooleanField()
   product_or_deal_id = models.IntegerField()
   amount = models.FloatField()
   
   def __str__(self):
   #   return str(self.product_or_deal_id) + " " + str(self.amount)
      if self.is_product:
         return self.product_name() + " " + str(self.amount) + " Total $ " + str(self.product_price())  
      else:
         return "Deal: " + str(self.product_or_deal_id) + " x " + str(self.amount)
   def product_name(self):
      if self.is_product:
         return Product.objects.get(pk=int(self.product_or_deal_id)).name
      else:
         return "Not a product"
   
   def get_type_of_product(self):
      if self.is_product:
        return Product.objects.get(pk=int(self.product_or_deal_id)).product_type
      else:
         return "Not a product"
         
   def time_of_sale(self):
      return TransactionTotal.objects.get(pk=self.transaction.id).timestamp      
   
   def product_price(self):
      timestamp = TransactionTotal.objects.get(pk=self.transaction.id).timestamp
      prices = ProductPrice.objects.filter(product__id=int(self.product_or_deal_id)).filter(time__lte=timestamp).order_by('time').reverse()
      if len(prices) == 0:
         print("No price for product! Error...")
         print(self.get_type_of_product())
         print(self.product_or_deal_id)
         print(self.product_name())
         return 0.0
         
      else:      
         price = prices[0].price
      product_type = self.get_type_of_product()
      if product_type == "SP": # SET PRICE
         return self.amount * price
      elif product_type == "WT": # BY WEIGHT
         return self.amount * price
      elif product_type == "PM": # PREMARKED
         return self.amount
      else:
	 #print "Product type is " + self.get_type_of_product()
         deal = Deal.objects.get(pk=int(self.product_or_deal_id))
	 #print "Error getting product price for " + str(deal.product_count) + " " + deal.product.name + " discount of " + str(deal.discount)
         return deal.discount * self.amount
      
      
      
