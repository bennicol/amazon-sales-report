import pandas as pd
import matplotlib.pyplot as plt



def load_data():
    sales = pd.read_csv("data/amazon.csv", low_memory=False)
    return sales



def dataset_overview(sales):
    rows = sales.shape[0] # Finding the number of rows in the dataset
    columns = sales.shape[1] # Finding the number of columns in the dataset
    data_types = sales.dtypes.astype(str) # Gives all of the datatypes in the dataset
    text = data_types.isin(["string", "object"]).sum() # And then we make the output look more presentable
    integer = (data_types == "int64").sum()
    floating = (data_types == "float64").sum()
    boolean = (data_types == "bool").sum()
    missing_values = sales.isnull().sum()
    missing_values = missing_values[missing_values > 0] # Only shows the columns with missing values

    print(f"""
Rows: {rows}

Columns: {columns}

Data Types:
Text: {text}
Integer: {integer}
Float: {floating}
Boolean: {boolean}

Missing Values: 
{missing_values}

Insights: A large dataset to work with and find trends, but with lots of missing values.""") # Adding insights for the client



def clean_data(sales):
    sales["Date"] = pd.to_datetime(sales["Date"], format="%m-%d-%y")
    
    sales = sales.drop(columns=["Unnamed: 22"]) # Only there because of extra coma at the end
    
    sales = sales.drop(columns=["promotion-ids"]) # Too many missing values to be able to work with

    sales = sales.dropna(subset=["Amount"]) # Drop missing data, better that than the dataset not working well
    
    sales["Courier Status"] = sales["Courier Status"].fillna("Unknown")  # Fill columns
    sales["currency"] = sales["currency"].fillna(sales["currency"].mode()[0])

    sales["ship-city"] = sales["ship-city"].fillna("Unknown")   # Small location gaps
    sales["ship-state"] = sales["ship-state"].fillna("Unknown")

    duplicates = sales.duplicated().sum() # Check duplicates
    if duplicates == 0:
        print("""
 - No duplicate rows to take into account """)
    else:
        print(f"""
Duplicate rows: {duplicates}""")
        
    invalid_amount = (sales["Amount"] == 0) | (sales["Amount"] == ",") # Deleting rows with amount equal to 0 or comma
    sales = sales[~invalid_amount] 

    print(""" - Removed empty column formed by commas (Unnamed: 22)
 - Deleted promotion-ids column due to large amount of missing values
 - Removed invalid values in the amount column
 - Filled in gaps in Courier Status, currency, ship-city and ship-state""")

    return sales



def create_columns(sales):

    sales["Month"] = sales["Date"].dt.to_period("M") # Month Column
    sales["Year"] = sales["Date"].dt.to_period("Y") # Year Column

    def simplify_status(status): # Simplifies the status column, avoiding future problems
        if "Shipped" in status:
            return "Shipped"
        elif "Cancelled" in status:
            return "Cancelled"
        elif "Pending" in status:
            return "Pending"
        else:
            return "Other"
        
    sales["Simplified_Status"] = sales["Status"].apply(simplify_status) 
    sales["Weekend Order"] = sales["Date"].dt.dayofweek >= 5 # Creating a weekend order column to see when clients mainly order products

    return sales



def revenue(sales):
    total_revenue = sales["Amount"].sum() # Calculates total revenue of the database
    highest_order_value = sales["Amount"].max() # Finds the most expensive order
    lowest_order_value = sales["Amount"].min() # Finds the cheapest order

    print(f"""
Total Revenue: ₹{total_revenue:,.2f}

Highest Order Value: ₹{highest_order_value:,.2f}

Lowest Order Value: ₹{lowest_order_value:,.2f}

Insight: The analysis shows us a large amount of sales in only four months, being ₹{total_revenue:,.2f}. There is a large price difference between the lowest and highest order, suggesting a large variety of products being sold.""")
    


def order(sales):
    total_orders = len(sales)
    orders_shipped = (sales["Simplified_Status"] == "Shipped").sum()
    orders_cancelled = (sales["Simplified_Status"] == "Cancelled").sum()
    orders_pending = (sales["Simplified_Status"] == "Pending").sum()
    cancellation_rate = (sales["Simplified_Status"] == "Cancelled").sum() / len(sales) * 100 # Calculating the cancellation rate

    print(f"""
Total Orders: {total_orders}

Completed Orders: {orders_shipped}

Cancelled Orders: {orders_cancelled}

Pending Orders: {orders_pending}

Cancellation Rate: {cancellation_rate:.2f} %

Insight: The low cancellation rate shows us that more than 90 % of products are shipped to the buyer. """)



def monthly_analysis(sales): # Making a table showing average order value, revenue and orders per month
    monthly_analysis = (sales.groupby([sales["Date"].dt.month, sales["Date"].dt.month_name()]).agg(Revenue=("Amount", "sum"),Average_Order_Value=("Amount", "mean"),Orders=("Order ID", "count")).droplevel(0))
    highest_revenue = monthly_analysis["Revenue"].max()
    lowest_revenue = monthly_analysis["Revenue"].min()

    decline = (highest_revenue - lowest_revenue) / highest_revenue * 100
    print(f"""
Revenue, Average Order Value and Orders by Month: 
{monthly_analysis.round(2)}

Insight: Revenue increase in sales from March to April, and then a slow decline, showing a {decline:.2f} % decrease from April to June.""")



def charts(sales): # Making charts for visual analysis

    monthly_revenue = sales.groupby("Month")["Amount"].sum() # Creating a line chart showing monthly revenue
    plt.figure(figsize=(8, 5))
    monthly_revenue.plot(kind="line", marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("charts/monthly_revenue.png")
    plt.show()

    orders_per_month = sales.groupby("Month").size() # Similar to monthly revenue, but instead using orders per month
    plt.figure(figsize=(8, 5))
    orders_per_month.plot(kind="line", marker="o")
    plt.title("Monthly Orders")
    plt.xlabel("Month")
    plt.ylabel("Orders")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("charts/orders_per_month.png")
    plt.show()

    order_status = sales["Simplified_Status"].value_counts()
    plt.figure(figsize=(8, 5))
    order_status.plot(kind="bar")
    plt.title("Order Status")
    plt.xlabel("Status")
    plt.ylabel("Times")
    plt.tight_layout()
    plt.savefig("charts/order_status.png")
    plt.show()
    
    revenue_by_fulfilment = sales.groupby("Fulfilment")["Amount"].sum() # Comparing revenue by amazon or by merchant
    plt.figure(figsize=(8, 5))
    revenue_by_fulfilment.plot(kind="bar")
    plt.title("Revenue by Fulfilment")
    plt.xlabel("Fulfilment")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig("charts/revenue_by_fulfilment.png")
    plt.show()
    
    b2b_vs_b2c = sales.groupby("B2B").size() # Showing which is more popular, B2B or B2C
    plt.figure(figsize=(8, 5))
    b2b_vs_b2c.plot(kind="bar")
    plt.title("B2B vs B2C")
    plt.xlabel("B2B")
    plt.ylabel("Orders")
    plt.tight_layout()
    plt.savefig("charts/b2b_vs_b2c.png")
    plt.show() 

    print("""
Monthly Revenue
Insight: Very high revenue over 4 months, have to make sure the amount of revenue doesn't decline up to a certain level.

Orders per month
Insight: Similar to monthly orders, a sharp increase from March to June and then a slow decline.
          
Order Status
Insight: High amount of orders shipped and completed

Revenue by Fulfilment
Insight: Main source of income coming from Amazon, representing the largest fulfilment channel in this database.
          
B2B vs B2C
Insight: Low amount of business to business sales. """)


def key_findings():
    print("""
Key Findings
------------

• Sales remained strong throughout the four-month period.
• Order fulfilment was highly successful, with over 90% of orders shipped.
• Revenue peaked in April before declining in the following months.
• Amazon fulfilment generated most of the revenue.
• B2C orders were much more common than B2B orders.""")
    
def final_report(): # A final report to keep things clear
    print("""
-------------------
AMAZON SALES REPORT
-------------------""")
    sales = load_data()
    print("""
Dataset Overview
----------------""")
    dataset_overview(sales)
    print("""
Data Cleaning
-------------""")
    sales = clean_data(sales)
    sales = create_columns(sales)
    print("""
Financial Performance
---------------------""")
    revenue(sales)
    print("""
Order Performance
-----------------""")
    order(sales)
    print("""
Monthly Analysis
----------------""")
    monthly_analysis(sales)
    print("""
Charts
------""")
    charts(sales)



def main(): # Main contains the report and then executes it
    final_report()


if __name__ == "__main__":
    main()
