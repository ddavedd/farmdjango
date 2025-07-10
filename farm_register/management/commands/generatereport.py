from django.core.management.base import BaseCommand, CommandError
from farm_register.models import Item, Product, Category, Deal, ProductPrice, ProductCategory, TransactionTotal, TransactionItem
from django.db.models import Sum, Count
from django.db import connection
import datetime

class Command(BaseCommand):
   args = 'No arguments'
   help = 'Runs a report of sales'
   def add_arguments(self, parser):
      parser.add_argument('report_type')
      #parser.add_argument('total')
         
   def handle(self, *args, **options):
      print(options['report_type'])
      if options['report_type']:
         if options['report_type'] == 'daily':
            print("Generate daily report only")
            for l in get_locations():
                generate_day(None, l, True)
         elif options['report_type'] == 'total':
            print("Generating total report")
            generate(2025)
            print("Done")
         elif options['report_type'] == 'detail':
            yearly_comparison()
            yearly_comparison(7)
            product_detail(2025)
            ### PRODUCT DETAIL BY MONTH ###
            #for month in [4,5,6,7,8,9,10,11,]:
               #product_detail(2024, month = month)
               #product_detail(2024, month = month, prod_id_list = [15,16,17,18,20,21,23,24,25,26,81,132,156,158,210,211,214,221,240,241,242,246,252,261,274,297,298,302,320,362,376,396,416,439,441,442,446,459,460,467,474,481,482,483,489,518,524,549], filename_prefix = "Fruit")
               #product_detail(2024, month = month, prod_id_list = [7,8,10,12,13,14,85,95,100,102,103,104,105,117,134,137,149,160,167,172,174,176,177,179,196,197,203,212,216,243,259,262,263,264,265,266,267,269,270,271,276,281,282,283,284,286,288,292,293,301,304,312,341,342,344,345,351,354,356,357,360,512,515,554,555], filename_prefix="Organic")
               #product_detail(2024, month = month, prod_id_list = [84,92,145,146,244,311,323,361,367,389,394,425,426,427,428,435,437,473], filename_prefix="PotatoGarlicFinger")
               #product_detail(2024, month = month, prod_id_list = [46,50,280,379,438,448,557], filename_prefix="CherryTomato")
               #product_detail(2024, month = month, prod_id_list = [36,181,272,275,290,315,321,324,395,415,420,422,423,433,447,450,462,466,487,488], filename_prefix="CutFlower")
               #product_detail(2024, month = month, prod_id_list = [331,332,457,519,536,546], filename_prefix="SignsPlants")
            ### YEAR TOTALS BY CATEGORY ###
            #product_detail(2024, prod_id_list = [15,16,17,18,20,21,23,24,25,26,81,132,156,158,210,211,214,221,240,241,242,246,252,261,274,297,298,302,320,362,376,396,416,439,441,442,446,459,460,467,474,481,482,483,489,518,524,549], filename_prefix = "Fruit")
            #product_detail(2024, prod_id_list = [7,8,10,12,13,14,85,95,100,102,103,104,105,117,134,137,149,160,167,172,174,176,177,179,196,197,203,212,216,243,259,262,263,264,265,266,267,269,270,271,276,281,282,283,284,286,288,292,293,301,304,312,341,342,344,345,351,354,356,357,360,512,515,554,555], filename_prefix="Organic")
            #product_detail(2024, prod_id_list = [84,92,145,146,244,311,323,361,367,389,394,425,426,427,428,435,437,473], filename_prefix="PotatoGarlicFinger")
            #product_detail(2024, prod_id_list = [46,50,280,379,438,448,557], filename_prefix="CherryTomato")
            #product_detail(2024, prod_id_list = [36,181,272,275,290,315,321,324,395,415,420,422,423,433,447,450,462,466,487,488], filename_prefix="CutFlower")
            #product_detail(2024, prod_id_list = [331,332,457,519,536,546], filename_prefix="SignsPlants")
         
         elif options['report_type'] == 'prices':
            price_list()
         elif options['report_type'] == 'comp':
            print("***Yearly Comparison by day***")
            yearly_comparison()
            print("***Yearly comparison by week***")
            yearly_comparison(7)
      else:
         print("Invalid arguments for running report")

def get_date_sales(td, delta):
   end = td + delta
   days_transactions = TransactionTotal.objects.filter(timestamp__range=(td, end)).aggregate(Sum('total'))
   return days_transactions["total__sum"]

def get_date_count(td, delta):
   end = td + delta
   transaction_count = TransactionTotal.objects.filter(timestamp__range=(td, end)).aggregate(Count('total'))
   count = transaction_count["total__count"]
   if count is None:
      return 0
   else:
      return count
def colorize_number(number):
   colorized = None
   if isinstance(number, int):
      if number < 0:
         colorized = "<font color='red'>%i</font>" % number
      else:
         colorized = "<font color='green'>%i</font>" % number        
   else:
      if number < 0.0:
         colorized = "<font color='red'>%.0f</font>" % number
      else:
         colorized = "<font color='green'>%.0f</font>" % number
   return colorized
   
def yearly_comparison(delta=1):
   # Line up days of the week to make comparison accurate
   #datetime.datetime(2014, 1, 13, 0, 0, 0)
   #datetime.datetime(2015, 1, 12, 0, 0, 0)
   #first_year_date = datetime.datetime(2016, 1, 11, 0, 0, 0)
   #first_year_date = datetime.datetime(2018, 1, 8, 0, 0, 0)
   #second_year_date = datetime.datetime(2019, 1, 7, 0, 0, 0)
   #third_year_date = datetime.datetime(2020, 1, 13, 0, 0, 0)
   #fourth_year_date = datetime.datetime(2021, 1, 11, 0, 0, 0)
   #fifth_year_date = datetime.datetime(2022,1,10,0,0,0)
   #sixth_year_date = datetime.datetime(2023,1,9,0,0,0)
   #seventh_year_date = datetime.datetime(2024,1,8,0,0,0)
   seventh_year_date = datetime.datetime(2025,1,6,0,0,0)
   day_delta = datetime.timedelta(days=delta)
   
   year_dates = [ seventh_year_date]
   #year_dates = [fourth_year_date, fifth_year_date, sixth_year_date]
   totals = []
   trans_counts = []
   for i in range(len(year_dates)):
      totals.append(0.0)
      trans_counts.append(0)
   
   #sales_table = [["2014","$","Count","2015","$","Tot'15-Tot'14","Count","C15-C14","2016","$","Tot'16-Tot'15","Count","C16-C15", "2017", "$", "Tot'17-Tot'16","Count","C17-C16","2018", "$", "Tot'18-Tot'17","Count","C18-C17",'14TTD','15TTD','16TTD','17TTD','18TTD','18TTD-17TTD']]
   table_header = []
   for i in range(len(year_dates)):
      current_year = year_dates[i].year
      table_header.append(str(current_year))
      current_year = current_year % 100
      table_header.append("$")
      if i > 0:
         table_header.append("$%i - $%i" % (current_year, current_year-1))
      table_header.append("Count")
      if i > 0:
         table_header.append("#%i - #%i" % (current_year, current_year-1))
   for i in range(len(year_dates)):
      current_year = year_dates[i].year
      current_year = current_year % 100
      table_header.append("%i $T" % (current_year))
   table_header.append("$24-$23")
   
   #print table_header
   sales_table = []
   sales_table.append(table_header)
   print(sales_table)
   for day in range(int(350/delta)): # All year pretty much
      day_sales = []
      day_counts = []
      for i in range(len(year_dates)):
         day_sales.append(get_date_sales(year_dates[i], day_delta))
         day_counts.append(get_date_count(year_dates[i], day_delta))
      
      if sum(day_counts)==0:
         print("No transactions, skipping")
         print("Interval is " + str(delta))
         print(year_dates)
      else:
         print(year_dates)
         #print "Running sales for " + str(first_year_date) + " and " + str(second_year_date)
         day_sales = [0.0 if s is None else s for s in day_sales] 
         for s in range(len(day_sales)):
            totals[s] = totals[s] + day_sales[s]
            trans_counts[s] = trans_counts[s] + day_counts[s]
       
         diff_sales = []
         diff_counts = []
         for i in range(len(day_sales)-1):
            diff_sales.append(day_sales[i+1] - day_sales[i])
            diff_counts.append(day_counts[i+1] - day_counts[i])
            
         color_diff_sales = [colorize_number(d) for d in diff_sales]
         color_diff_counts = [colorize_number(d) for d in diff_counts]
         
         
         # next day or week
         #day_link = "<a href='./dates/westchester" + fifth_year_date.strftime("%Y-%m-%d") + ".html'>" + fifth_year_date.strftime("%m-%d") + "</a>\n"
         table_day = []
         for i in range(len(year_dates)):
            table_day.append(year_dates[i].strftime("%m-%d"))
            table_day.append("%.2f" % day_sales[i])
            if i > 0:
               table_day.append(color_diff_sales[i-1])
            table_day.append("%i" % day_counts[i])
            if i > 0:
               table_day.append(color_diff_counts[i-1])
         
         for i in range(len(totals)):
            table_day.append(int(totals[i]))
         if len(totals) >= 2:
            table_day.append(colorize_number(totals[-1]-totals[-2]))
         
         sales_table.append(table_day)
         
      # Move to the next date
      for i in range(len(year_dates)):
         year_dates[i] = year_dates[i] + day_delta
      
   # At the end, add the total sales to the bottom
   total_row = []
   for i in range(len(year_dates)):   
      total_row.append("Total")
      total_row.append("%.0f" % totals[i])
      if i > 0:
         total_row.append(colorize_number(int(totals[i]-totals[i-1])))
      total_row.append(trans_counts[i])
      if i > 0:
         total_row.append(colorize_number(trans_counts[i]-trans_counts[i-1]))
   sales_table.append(total_row)

   html = "<html><p>Generated at " + str(datetime.datetime.now()) + "</p>\n"
   html += convert_to_table(sales_table) + "</html>"
   html_file = open("year_comparison%i.html" % delta, "w")
   html_file.write(html)
   html_file.close()

   data = convert_to_gnuplot_data(sales_table)
   data_file = open("year_comparison%i.data" % delta, "w")
   data_file.write(data)
   data_file.close()
   
    
def convert_to_gnuplot_data(table):
   data = "# Data generated for yearly comparison\n"
   for row in table:
      for item in row:
         data += str(item).strip() + "\t"
      data += "\n"
   return data

def get_locations():
   temp = TransactionTotal.objects.values_list('location').distinct()
   return [x[0] for x in temp]
      
def hourly_sales(date, location):
   print("Hourly Sales")
   hours_min = 0
   hours_max = 24
   hour_totals = []
   for hour in range(hours_min, hours_max):
      start_hour_date = datetime.datetime(date.year, date.month, date.day, hour, 0, 0)
      end_hour_date = datetime.datetime(date.year, date.month, date.day, hour, 59, 59)
      hour_trans_total = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(start_hour_date, end_hour_date)).aggregate(Sum('total'))
      hour_trans_count = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(start_hour_date, end_hour_date)).aggregate(Count('total'))
      if hour_trans_total["total__sum"] is None:
         hour_totals.append([hour, 0.0, 0])
      else:
         hour_totals.append([hour, "%.2f" % hour_trans_total["total__sum"], hour_trans_count["total__count"]])

   first = get_first_hour_with_sales(hour_totals)
   last = get_last_hour_with_sales(hour_totals)
   if first is None:
      print("No sales for date... Error")
      return []
   else:
      return hour_totals[first:last+1]
      
def get_first_hour_with_sales(hour_totals):
   for h in hour_totals:
      if float(h[1]) > 0.01:
         return h[0]
   return None

def get_last_hour_with_sales(hour_totals):
   hour_with_sales = None
   for h in hour_totals:
      if float(h[1]) > 0.01:
         hour_with_sales = h[0]         
   return hour_with_sales
   
def total_money_count(year, location=None):
   print("Total Money Count")
   if location is None:
      total_money = TransactionTotal.objects.filter(timestamp__year=year).aggregate(Sum('total'))
   else:
      total_money = TransactionTotal.objects.filter(timestamp__year=year).filter(location=location).aggregate(Sum('total'))
      print("Generating money count for location " + location)
   total_money_count = total_money["total__sum"]
   if total_money_count is None:
      total_money_count = 0.0
   return total_money_count
   
def by_day_transaction_type(transaction_date, location=None):
   print("Transactions by payment type, location data not used")
   end_of_day = datetime.datetime(transaction_date.year, transaction_date.month, transaction_date.day, 23, 59, 59)
   transaction_types = ["CASH","CHECK","CREDIT CARD","UNKNOWN"]
   output_list = []
   for t_type in transaction_types:
      trans = TransactionTotal.objects.filter(timestamp__range=(transaction_date, end_of_day)).filter(transaction_type=t_type)
      output_list.append([t_type, len(trans), "%.2f" % sum([t.total for t in trans])])
   return output_list
    
def trans_items_in_day(date, trans_location): 
   end_of_day = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
   day_transactions = TransactionTotal.objects.filter(location=trans_location).filter(timestamp__range=(date, end_of_day))
   day_trans_ids = [d.id for d in day_transactions]
   return TransactionItem.objects.filter(transaction__in=day_trans_ids)

def price_list():
   products = Product.objects.all().order_by('name')
   for p in products:
      prices = ProductPrice.objects.filter(product_id=p.id)
      latest_price = prices[len(prices)-1].price
      print("%s %.2f" % (p.name, latest_price))
      
   
def by_day_product_count(date, location):
   print("By day product count")
   product_counts = []
   transaction_items_for_day = trans_items_in_day(date, location)
   products = transaction_items_for_day.filter(is_product=1)
   #print products
   totals = products.values('product_or_deal_id').annotate(total=Sum('amount'))
   for total in totals:
      # THIS IS GOING TO BE WRONG UNTIL YOU GET CURRENT AND PAST PRICES INSTEAD OF JUST THE NEWEST PRICE
      this_product_id = total['product_or_deal_id']      
      prices = ProductPrice.objects.filter(product_id=this_product_id)
      if len(prices) == 0:
         print("ERROR, NO PRICE")
         print(total)
         print(this_product_id)
         print(prices)
      latest_price = prices[len(prices)-1].price
      dollars = total['total'] * latest_price
      product_counts.append([get_product_name(total['product_or_deal_id']), total['total'], latest_price, dollars])
   product_counts.sort()
   return product_counts
   
def by_day_deal_count(date, location):
   print("By day deal count")
   deal_counts = []
   transaction_items_for_day = trans_items_in_day(date, location)
   deals = transaction_items_for_day.filter(is_product=0)
   totals = deals.values('product_or_deal_id').annotate(total=Sum('amount'))
   for total in totals:
      deal_counts.append([get_deal_name(total['product_or_deal_id']), total['total']])
   deal_counts.sort()
   return deal_counts


def get_trans_product_item_count(trans_item):
   product = Product.objects.get(id=trans_item.product_or_deal_id)
   if product is not None:
      return product.item_count * trans_item.amount
   else:
      print("Error getting number of basic items in a transaction item")
      return 0.0
   
def get_corn_count_in_sacks(date, location):
   print("Get corn count in sacks")
   transaction_items_for_day = trans_items_in_day(date, location)
   corn_item = Item.objects.get(name="Corn")
   corn_products = Product.objects.filter(item=corn_item)
   cleaned_ids = [c.id for c in corn_products]
   trans_items_corn = transaction_items_for_day.filter(product_or_deal_id__in=cleaned_ids, is_product=1)
   #for t in trans_items_corn:
   #   print t
   #   print get_trans_product_item_count(t)
      
   return sum([get_trans_product_item_count(t) for t in trans_items_corn])/60.0

def by_day_department_money_count(date, location):
   print("By day department money count")
   day_transactions = trans_items_in_day(date, location)
   money_counts = []
   for cat in Category.objects.all():
      product_ids = ProductCategory.objects.filter(category=cat.id).values('product')
      cleaned_ids = [p['product'] for p in product_ids]
      trans_items_in_category = day_transactions.filter(product_or_deal_id__in=cleaned_ids).filter(is_product=1)
      total = sum([t.product_price() for t in trans_items_in_category])
      #for t in trans_items_in_category:
      #   print t      
      #   print t.product_price()
      #   print t.amount
               
      #print total
      money_counts.append([cat.name, "%.2f" % total])
      #print "Done with category"
   return money_counts
   
def get_product_name(product_id):
   return Product.objects.get(pk=product_id).name
   
def get_deal_name(deal_id):
   deal = Deal.objects.get(pk=deal_id)
   return str(deal.product_count) + " " + deal.product.name 


def yearly_product_count(year):
   print("Year currently not working")
   first_trans_of_year = TransactionTotal.objects.filter(timestamp__year=year)
   if len(first_trans_of_year) == 0:
      return []
   else:
      first_trans_of_year = first_trans_of_year[0].id
   print("Yearly product count")
   product_counts = []
   totals = TransactionItem.objects.filter(transaction_id__gt=first_trans_of_year).filter(is_product=1).values('product_or_deal_id').annotate(total=Sum('amount'))
   for total in totals:
      product_counts.append([get_product_name(total["product_or_deal_id"]), total['total']])   
   product_counts.sort()
   print(product_counts)
   print("Finished yearly product count")
   return product_counts

   
def yearly_department_money_count(year):
   print("Year currently not working")
   print("Yearly Department money count")
   first_trans_of_year = TransactionTotal.objects.filter(timestamp__year=year)
   if len(first_trans_of_year) == 0:
      return []
   else:
      first_trans_of_year = first_trans_of_year[0].id
   categories = Category.objects.all()
   counts = []
   for cat in categories:
      product_ids = ProductCategory.objects.filter(category=cat.id).values('product')
      cleaned_ids = [p['product'] for p in product_ids]
      print("Number of ids in " + str(cat) + " is " + str(len(cleaned_ids)))
      trans_items_in_category = TransactionItem.objects.filter(transaction_id__gt=first_trans_of_year).filter(product_or_deal_id__in=cleaned_ids).filter(is_product=1)
      total = sum([t.product_price() for t in trans_items_in_category])
      counts.append([cat.name, total])
   return counts
   
def counts_all_dates(transaction_dates):
   print("Count all dates")
   counts = []
   for td in transaction_dates:
      almost_midnight = datetime.datetime(td.year, td.month, td.day, 23, 59, 59)
      days_transactions = TransactionTotal.objects.filter(timestamp__range=(transaction_date, almost_midnight)).aggregate(Sum('total'))
      counts.append([transaction_date, days_transactions["total__sum"]])
   return counts

def convert_to_table(input_list):
   html = "<table border=1>\n"
   for item in input_list:
      html += "<tr>\n"
      for x in item:
         html += "\t<td>" + str(x).strip() + "</td>\n"
      html += "</tr>\n"
   html += "</table>\n"
   return html

def generate_location(location, year):
   location_html = "<html>"
   location_html += "<h3>" + location + "</h3>"
   print("Generating location " + location)
   location_html += "<p>Generated at " + str(datetime.datetime.now()) + "</p>"
   
   location_html += "<a href='dates/" + location + "today.html'>Today</a>"
   print("Tally total sum")
   tot = TransactionTotal.objects.filter(timestamp__year=year).filter(location=location).aggregate(Sum('total'))['total__sum']
   if tot is None:
      tot = 0.0
   totals = [["Total"] + ["%.2f" % tot]]

   print("Tally subtotal sum")
   sub = TransactionTotal.objects.filter(timestamp__year=year).filter(location=location).aggregate(Sum('subtotal'))["subtotal__sum"]
   if sub is None:
      sub = 0.0
   totals += [["Subtotal"] + ["%.2f" % sub]]

   print("Tally Tax Edible sum")
   tax_ed = TransactionTotal.objects.filter(timestamp__year=year).filter(location=location).aggregate(Sum('edible_tax'))["edible_tax__sum"]
   if tax_ed is None:
      tax_ed = 0.0
   totals += [["Tax Edible"] + ["%.2f" % tax_ed]]

   print("Tally Tax Nonedible sum")
   tax_noned = TransactionTotal.objects.filter(timestamp__year=year).filter(location=location).aggregate(Sum('nonedible_tax'))["nonedible_tax__sum"]
   if tax_noned is None:
      tax_noned = 0.0
   totals += [["Tax Nonedible"] + ["%.2f" % tax_noned]]
   
   print("Totals for location tallied")
   print(totals)
   location_html += convert_to_table(totals)
      
   transaction_dates = TransactionTotal.objects.filter(timestamp__year=year).filter(location=location).datetimes('timestamp','day')
   dates = [["Date","Total","Count","Credit","Check","Cash","Unknown"]]
   for transaction_date in transaction_dates:
      print(transaction_date)
      print("Generating day" + str(transaction_date))
      
      link_object = generate_day(transaction_date, location)
      dates.append(link_object)

   location_html += convert_to_table(dates)

   location_file = open(location+".html", "w")
   location_file.write(location_html)
   location_file.close()

def generate_day(transaction_date, location, now=False):
      if now:
         date_string = datetime.datetime.now().strftime("%Y-%m-%d")
         #print "NOW!"
         #print date_string
         date = datetime.datetime.now()
         date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)      
         transaction_date = date         
         #print date
      else:
         date_string = transaction_date.strftime("%Y-%m-%d")
         date = transaction_date
         #print "Date should look like below"         
         #print date
         #print "..."
      end_of_day = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
      day_transactions = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(date, end_of_day)).aggregate(Sum("total"))
      total = day_transactions["total__sum"]
      day_credit = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(date, end_of_day)).filter(transaction_type="CREDIT CARD").aggregate(Sum("total"))["total__sum"]
      if day_credit is None:
        day_credit = 0.0
      day_check = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(date, end_of_day)).filter(transaction_type="CHECK").aggregate(Sum("total"))["total__sum"]
      if day_check is None:
        day_check = 0.0
      day_cash = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(date, end_of_day)).filter(transaction_type="CASH").aggregate(Sum("total"))["total__sum"]
      if day_cash is None:
        day_cash = 0.0
      day_unknown = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(date, end_of_day)).filter(transaction_type="UNKNOWN").aggregate(Sum("total"))["total__sum"] 
      if day_unknown is None:
        day_unknown = 0.0
      trans_counts = TransactionTotal.objects.filter(location=location).filter(timestamp__range=(date, end_of_day)).count()
      
      day_html = "<html>"
      day_html += "<p>Generated at " + str(datetime.datetime.now()) + "</p>"
      day_html += convert_to_table([["Corn Sack Count", "%.2f" % get_corn_count_in_sacks(transaction_date, location)]])
      day_html += convert_to_table([["Transaction Type","Count","Amount"]] + by_day_transaction_type(transaction_date, location))
      day_html += convert_to_table([["Hour", "$", "Transactions"]] + hourly_sales(transaction_date, location) + [["Total","%.2f" % total, str(trans_counts)]])
      day_html += convert_to_table([["Department", "$"]] + by_day_department_money_count(transaction_date, location))      
      day_html += convert_to_table([["Product", "Count", "Price", "$"]] + by_day_product_count(transaction_date, location))
      day_html += convert_to_table([["Deal","Count"]] + by_day_deal_count(transaction_date, location))
      
      
      day_html += "</html>"
      
      day_file = open("dates/" + location + date_string + ".html", "w")
      day_file.write(day_html)
      day_file.close()   
      return ["<a href='dates/" + location + date_string + ".html'>" + date_string + "</a>", "%.2f" % total, trans_counts, "%.2f" % day_credit, "%.2f" % day_check, "%.2f" % day_cash, "%.2f" % day_unknown ]

def generate_month(year):
   for month in range(1,13):
      pass   
   
def generate(year):
   print("Generating report")
   # These go on home page
   index_html = "<html>"
   index_html = "Overall totals. For individual totals click on location link\n<br/>"
   print(get_locations())
   location_links = []
   for l in get_locations():
      generate_location(str(l), year)
      location_links.append(["<a href='" + str(l) + ".html'>" + str(l) + "</a>"])
      
   index_html += "<a href='year_comparison1.html'>Daily Comparison</a>\n"
   index_html += "<a href='year_comparison7.html'>Weekly Comparison</a>\n"
   totals = [["Total"] + ["%.2f" % total_money_count(year)]]
   sub = TransactionTotal.objects.filter(timestamp__year=year).aggregate(Sum('subtotal'))["subtotal__sum"]
   if sub is None:
      sub = 0.0
   totals += [["Subtotal"] + ["%.2f" % sub]]
   tax_ed = TransactionTotal.objects.filter(timestamp__year=year).aggregate(Sum('edible_tax'))["edible_tax__sum"]
   if tax_ed is None:
      tax_ed = 0.0
   totals += [["Tax Edible"] + ["%.2f" % tax_ed]] 
   tax_noned = TransactionTotal.objects.filter(timestamp__year=year).aggregate(Sum('nonedible_tax'))["nonedible_tax__sum"]
   if tax_noned is None:
      tax_noned = 0.0
   totals += [["Tax Nonedible"] + ["%.2f" % tax_noned]]
   
   yearly_dept = [["Department", "$"]] + yearly_department_money_count(year) 
   yearly_product = [["Product", "Count"]] + yearly_product_count(year)
   
   index_html += convert_to_table(location_links)
   index_html += convert_to_table(totals)
   index_html += convert_to_table(yearly_dept)
   index_html += convert_to_table(yearly_product)

   index_html += "</html>"
   
   f = open("index.html","w")
   f.write(index_html)
   f.close()
   f = open("%i_index.html" % year,"w")
   f.write(index_html)
   f.close()
   
def detailed_report(product, year, month=None):
   print(product)
   if month:
      this_year = datetime.datetime(year, month,1,0,0,0)
      end = datetime.datetime(year, month+1, 1,0,0,0)
   else:
      this_year = datetime.datetime(year,1,1,0,0,0)
      end = datetime.datetime(year+1,1,1,0,0,0)
   
   prod_prices = ProductPrice.objects.filter(product_id=product.id).order_by('time')
   transactions = TransactionItem.objects.filter(product_or_deal_id=product.id).filter(is_product=1)
   table_values = [[product.name, product.id],["From %s to %s" % (str(this_year), str(end)), "Amount Sold", "Price", "Total $"]]
   total_money = 0.0
   total_items = 0.0
   for i in range(len(prod_prices)):
      #print prod_prices[i]
      
      current_time = prod_prices[i].time
      if i < len(prod_prices)-1:
         next_time = prod_prices[i+1].time
      else:
         next_time = datetime.datetime.now()
      print(current_time, next_time)
      start = max(this_year, current_time)
      finish = min(end, next_time)
      #transactions_in_range_total = transactions.filter(transaction__timestamp__gt=this_year).filter(transaction__timestamp__lt=end).filter(transaction__timestamp__range=(current_time,next_time)).aggregate(Sum('amount'))
      transactions_in_range_total = transactions.filter(transaction__timestamp__range=(start, finish)).aggregate(Sum('amount'))
      
      amount_sum = transactions_in_range_total['amount__sum']
      if amount_sum is None:
         amount_sum = 0
      current_price = prod_prices[i].price
      current_money = amount_sum * current_price
      print(amount_sum, current_price, current_money)
      total_money += current_money
      total_items += amount_sum
      if current_money > .01:
         table_values.append([str(current_time), amount_sum, current_price, current_money])
      #print transactions
      #print total
   print(total_money)
   table_values.append(["Total", total_items, "", total_money])
   if total_money > .01:
      return table_values, total_money
   else:
      return None, None
      
def product_detail(year, month=None, prod_id_list=None, filename_prefix=None):
   grand_total = 0.0
   if prod_id_list is None:
      matching_products = Product.objects.order_by('name')
   else:
      matching_products = Product.objects.filter(pk__in=prod_id_list).order_by('name')
   html = "<html>"
   html += "<p>Generated at " + str(datetime.datetime.now()) + "</p>"
   for product in matching_products:
      table, total_money = detailed_report(product, year, month)
      if table:
         html += convert_to_table(table)
         grand_total += total_money
   html += "<p>Grand Total - %.2f</p>" % grand_total
   html += "</html>"
   if filename_prefix:
      filename = filename_prefix + "_"
   else:
      filename = ""
   if month:
      filename += "%i_%i_detail.html" % (year, month)
   else:
      filename += "%i_detail.html" % (year)
      
   detail_file = open(filename, "w")
   detail_file.write(html)
   detail_file.close()
   print(connection.queries)
   
def get_price_at_time(product_id, time):
    prod_prices = ProductPrice.objects.filter(product_id=product.id).order_by('time')
    prev_price = prod_prices[0]
    for prod_price in prod_prices:
        if time < prod_price.time:
            return prev_price
        else:
            prev_price = prod_price 
    return None
