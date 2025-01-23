from django.contrib import admin

from farm_register.models import Item, Product, ProductPrice, Category, ProductCategory, Deal, TransactionTotal, TransactionItem

#admin.site.register(Item)
#admin.site.register(Product)
#admin.site.register(ProductPrice)
#admin.site.register(Category)
#admin.site.register(ProductCategory)
#admin.site.register(Deal)
#admin.site.register(TransactionTotal)
admin.site.register(TransactionItem)

class ItemAdmin(admin.ModelAdmin):
   list_display = ['name', 'id']

class TransactionItemInline(admin.StackedInline):
   model = TransactionItem
   extra = 0
   readonly_fields = ('is_product', 'product_or_deal_id', 'amount')

class TransactionTotalAdmin(admin.ModelAdmin):
   actions = None
   ordering = ['-timestamp', 'total']
   search_fields = ['timestamp', 'total']
   readonly_fields = ('total','subtotal','edible_tax','nonedible_tax','timestamp','cashier','location','transaction_time','transaction_type')
   list_display = ('timestamp','total', 'subtotal','edible_tax','nonedible_tax', 'cashier')
   list_filter = ('timestamp', 'cashier')
   #fields = ('total','subtotal','edible_tax','nonedible_tax','timestamp')
   inlines = [TransactionItemInline]
   
class CategoryAdmin(admin.ModelAdmin):
   list_display = ['name','enabled','id']
   list_editable = ['enabled']
   
class ProductPriceAdmin(admin.ModelAdmin):
   readonly_fields = ('price','time',)
   fields = ('price','time')
   #def has_delete_permission(self, request, obj=None):
   #   return False
      
   #def has_change_permission(self, request, obj=None):
   #   return False

class DealAdmin(admin.ModelAdmin):
   readonly_fields = ('product','product_count','discount','time',)
   fields = ('product','product_count','discount','time','enabled')
   list_display = ['product','product_count', 'discount','enabled','time','id']  
class ProductPriceInline(admin.StackedInline):
   model = ProductPrice
   #readonly_fields = ('price',)
   #fields = ('price','time')
   extra = 0
   
   #def has_delete_permission(self, request, obj=None):
   #   return False
      
   #def has_change_permission(self, request, obj=None):
   #   return False
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['product','get_product_enabled','get_product_id','category'] 
    list_filter = ['category', 'product__enabled']

    def get_product_enabled(self, obj):
        return obj.product.enabled
    def get_product_id(self,obj):
        return obj.product.id

class ProductCategoryInline(admin.StackedInline):
   model = ProductCategory
   extra = 0
   
class DealInline(admin.StackedInline):

   def has_delete_permission(self, request, obj=None):
      return False
      
   def has_change_permission(self, request, obj=None):
      return False
      
   model = Deal   
   extra = 0

#class TransactionItemAdmin(admin.ModelAdmin):
#   list_display = ['transaction_id','product_or_deal_id','amount']
#class ProductCategoryAdmin(admin.ModelAdmin):
#   list_filter = ['category']
   
class ProductAdmin(admin.ModelAdmin):
   list_per_page = 100
   ordering = ['-enabled', 'name']
   search_fields = ['name']
   list_display = ('name','enabled','current_price','id')
   list_editable = ['enabled']
   list_filter = ['enabled','tax_rate_nonedible','product_type']
   inlines = [ProductPriceInline, ProductCategoryInline, DealInline]

admin.site.register(Item, ItemAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)   
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(TransactionTotal, TransactionTotalAdmin)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(ProductCategory, ProductCategoryAdmin)
