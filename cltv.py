############################################
# CUSTOMER LIFETIME VALUE 
############################################

# 1. Preparing Dataset
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (retention_rate / total_number_of_customers)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Cereating Segments
# 9. BONUS: Functionalization of All Operations

##################################################
# 1. Preparing Dataset
##################################################


import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel("path/dataset/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.isnull().sum()
df = df[~df["Invoice"].str.contains("C", na=False)]  

#Invoices starting with C are return invoices. 
#They have been removed from the data set in order not to fall to life during the analysis phase.

df.describe().T
df = df[(df['Quantity'] > 0)]  # let's get rid of negative numbers
df.dropna(inplace=True)        # what values should we remove


df["TotalPrice"] = df["Quantity"] * df["Price"]   # in the cltv account we will need the total price that customers leave us
cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})
cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']

#Frequency in R, F, M is the same as total transaction, monetary is the same as total price, recency is not present here


##################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
##################################################

cltv_c.head()
cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

##################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
##################################################

cltv_c.head()
cltv_c.shape[0]

cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

##################################################
# 4. Repeat Rate & Churn Rate  (retention_rate / total_number_of_customers)
##################################################



repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
churn_rate = 1 - repeat_rate

##################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
##################################################
#0.10 fixed value is the value determined by the company, may vary

cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10


##################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
##################################################

cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c["purchase_frequency"]

##################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
##################################################

cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

cltv_c.sort_values(by="cltv", ascending=False).head()

# the cltv values obtained --> means that if I need to choose to deal more with a group of customers, I know where I can focus

##################################################
# 8. Creating Segments
##################################################

cltv_c.sort_values(by="cltv", ascending=False).tail()

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

cltv_c.sort_values(by="cltv", ascending=False).head()

#oluşan segmentleri analiz edelim
cltv_c.groupby("segment").agg({"count", "mean", "sum"})

cltv_c.to_csv("cltc_c.csv")   #saving results



BONUS: Functionalization of All Operations
def create_cltv_c(dataframe, profit=0.10):

    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
    # avg_order_value
    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']
    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]
    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    # profit_margin
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    # Customer Value
    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])
    # Customer Lifetime Value
    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']
    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c




clv = create_cltv_c(df)

#uygulanılan bu yöntemin bazı kısıtları vardır, projeksiyon yönü düşüktür, kitle üzerinde bazı sabitleri barındırır ama kitlenin bazı genel davranışını göz önünde bulunduramaz
#dolayısıyla bu hesaba istatistiksel bir modelleme açısından yaklaşıldığında daha gelişmiş modeller söz konusu olmaktadır
