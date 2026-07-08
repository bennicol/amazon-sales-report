# Amazon Sales Analysis

## Project Overview

This project analyses Amazon sales data to identify customer behaviour, order performance, and sale trends.

The goal of this analysis is to transform data from large datasets into meaningful insights using Python, pandas, and Matplotlib.

---

## Objectives

The main objectives of this project are:

- Clean the dataset for analysis.
- Analyse revenue and order performance.
- Identify monthly sales trends.
- Analyse cancellation rates.
- Compare fulfilment methods.
- Compare B2B and B2C order behaviour.
- Create charts to visually present findings.

---

## Dataset

The dataset contains Amazon order information, including:

- Order ID
- Order date
- Order status
- Fulfilment method
- Sales channel
- Product category
- Quantity
- Sales amount
- Customer location
- B2B status

The dataset contains over 100,000 order records.

---

## Data Cleaning

The following cleaning steps were performed:

- Converted dates into datetime format.
- Removed unnecessary columns.
- Removed columns with excessive missing values.
- Handled missing values in important columns.
- Checked for duplicate rows.
- Removed invalid sales amounts.
- Created new analytical columns.

New columns created:

- Month
- Year
- Simplified Status
- Weekend Order

---

## Analysis Performed

### Financial Analysis

Calculated:

- Total revenue
- Highest order value
- Lowest order value

### Order Analysis

Analysed:

- Total orders
- Completed orders
- Cancelled orders
- Pending orders
- Cancellation rate

### Monthly Analysis

Compared:

- Monthly revenue
- Average order value
- Number of orders

### Customer and Fulfilment Analysis

Explored:

- B2B vs B2C orders
- Revenue by fulfilment method
- Order status distribution

---

## Visualisations

The project creates the following charts:

- Monthly revenue 
- Monthly orders 
- Order status
- Revenue by fulfilment 
- B2B vs B2C comparison

---

## Key Findings

Some examples of insights generated:

- The dataset generated significant revenue over the analysed period.
- The majority of orders were successfully completed.
- Revenue changed throughout the analysed months, showing different trends.
- Amazon fulfilment represented the largest fulfilment channel.
- B2C orders were much more common than B2B orders.

---

## Technologies Used

- Python
- Pandas
- Matplotlib
- VsCode

---

## Notes

- The dataset used in this project is not included to to its size and usage restrictions.

---

## Project Structure


Amazon_Sales_Report/
│
├── data/
│ └── amazon.csv
│
├── charts/
│ ├── monthly_revenue.png
│ ├── orders_per_month.png
│ ├── order_status.png
│ ├── revenue_by_fulfilment.png
│ └── b2b_vs_b2c.png
│
├── src/
│ └── main.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE


---

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/bennicol/amazon-sales-report.git
Install dependencies:
pip install -r requirements.txt
Run the analysis:
python src/main.py