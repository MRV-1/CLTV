# CLTV
CLTV, one of the CRM techniques, is based on the calculation process.


** I could not add the file to the project directory because the file size is large. Download it from the link below. 
https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

-** If you cannot access the data, I can provide the data if you contact me.

############################################
# CUSTOMER LIFETIME VALUE 
############################################

 1. Preparing Dataset
 2. Average Order Value (average_order_value = total_price / total_transaction)
 3. Purchase Frequency (total_transaction / total_number_of_customers)
 4. Repeat Rate & Churn Rate (retention_rate / total_number_of_customers)
 5. Profit Margin (profit_margin =  total_price * 0.10)
 6. Customer Value (customer_value = average_order_value * purchase_frequency)
 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
 8. Cereating Segments
 9. BONUS: Functionalization of All Operations

##################################################
# 1. Preparing Dataset
##################################################



 Dataset Story
 Online Retail II dataset of a UK-based online retail store
 It includes sales between 01/12/2009 - 09/12/2011.


 Variables
 InvoiceNo: Invoice number. Unique number for each transaction, i.e. invoice. If it starts with C, the canceled transaction.
 StockCode: Product code. Unique number for each product.
 Description: Product name
 Quantity: Product quantity. It expresses how many of the products in the invoices are sold.
 InvoiceDate: Invoice date and time.
 UnitPrice: Product price (in pounds sterling)
 CustomerID Unique customer number
 Country: Country name. The country where the customer lives.

# There were many different segmentation processes, the process to be used here will be according to the Lifetime Value.

You can review my article below for details of the transactions.

https://medium.com/@merveatasoy48/crm-analytics-and-cltv-calculating-41b2127ad957

If there is anything you don't understand, please contact me.



