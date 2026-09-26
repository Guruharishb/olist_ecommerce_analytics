import pandas as pd


BASE_PATH = "data/raw"

ORDERS_FILE = f"{BASE_PATH}/olist_orders_dataset.csv"
CUSTOMERS_FILE = f"{BASE_PATH}/olist_customers_dataset.csv"
ORDER_ITEMS_FILE = f"{BASE_PATH}/olist_order_items_dataset.csv"
PRODUCTS_FILE = f"{BASE_PATH}/olist_products_dataset.csv"
SELLERS_FILE = f"{BASE_PATH}/olist_sellers_dataset.csv"
PAYMENTS_FILE = f"{BASE_PATH}/olist_order_payments_dataset.csv"


def inspect_dataset(df, name):
    
    print(f"{name.upper()} DATASET")
    print("-" * 60)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())


orders = pd.read_csv(ORDERS_FILE)
customers = pd.read_csv(CUSTOMERS_FILE)
order_items = pd.read_csv(ORDER_ITEMS_FILE)
products = pd.read_csv(PRODUCTS_FILE)
sellers = pd.read_csv(SELLERS_FILE)
payments = pd.read_csv(PAYMENTS_FILE)


inspect_dataset(orders, "Orders")

print("\nOrder status counts:")
print(orders["order_status"].value_counts())

print("\nMissing delivered customer date by status:")
print(
    pd.crosstab(
        orders["order_status"],
        orders["order_delivered_customer_date"].isna()
    )
)

print("\nDelivered orders with missing customer delivery date:")
print(
    orders[
        (orders["order_status"] == "delivered")
        & orders["order_delivered_customer_date"].isna()
    ][[
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]].to_string(index=False)
)

print("\nMissing approved date by status:")
print(
    pd.crosstab(
        orders["order_status"],
        orders["order_approved_at"].isna()
    )
)

print("\nDelivered orders with missing approval date:")
print(
    orders[
        (orders["order_status"] == "delivered")
        & orders["order_approved_at"].isna()
    ][[
        "order_id",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]].to_string(index=False)
)

print("\nMissing carrier delivery date by status:")
print(
    pd.crosstab(
        orders["order_status"],
        orders["order_delivered_carrier_date"].isna()
    )
)

print("\nDelivered orders with missing carrier delivery date:")
print(
    orders[
        (orders["order_status"] == "delivered")
        & orders["order_delivered_carrier_date"].isna()
    ][[
        "order_id",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]].to_string(index=False)
)

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

print("\nData types after date conversion:")
print(orders.dtypes)

print("\nMissing dates after conversion:")
print(orders[date_columns].isna().sum())

print("\nDuplicate order IDs:")
print(orders["order_id"].duplicated().sum())

print("\nMissing order IDs:")
print(orders["order_id"].isna().sum())


inspect_dataset(customers, "Customers")

print("\nDuplicate customer IDs:")
print(customers["customer_id"].duplicated().sum())

print("\nMissing customer IDs:")
print(customers["customer_id"].isna().sum())

missing_customers = orders[
    ~orders["customer_id"].isin(customers["customer_id"])
]

print("\nOrders with missing customer references:")
print(len(missing_customers))


inspect_dataset(order_items, "Order Items")

print("\nDuplicate order_id + order_item_id:")
print(
    order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

missing_orders = order_items[
    ~order_items["order_id"].isin(orders["order_id"])
]

print("\nOrder items with missing order references:")
print(len(missing_orders))



inspect_dataset(products, "Products")

print("\nProducts with missing category:")
print(
    products[
        products["product_category_name"].isna()
    ].head(10).to_string(index=False)
)

print("\nProducts with missing weight:")
print(
    products[
        products["product_weight_g"].isna()
    ].to_string(index=False)
)


inspect_dataset(sellers, "Sellers")

missing_sellers = order_items[
    ~order_items["seller_id"].isin(sellers["seller_id"])
]

print("\nOrder items with missing seller references:")
print(len(missing_sellers))


inspect_dataset(payments, "Payments")

duplicate_payments = payments.duplicated(
    subset=["order_id", "payment_sequential"]
).sum()

print("\nDuplicate order_id + payment_sequential:")
print(duplicate_payments)

print("\nPayment types:")
print(payments["payment_type"].value_counts())

missing_payment_orders = payments[
    ~payments["order_id"].isin(orders["order_id"])
]

print("\nPayments with missing order references:")
print(len(missing_payment_orders))

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

print("\nDelivery days:")
print(orders["delivery_days"].describe())


payments["payment_type"] = payments["payment_type"].replace(
    "not_defined",
    "unknown"
)

print("\nCleaned payment types:")
print(payments["payment_type"].value_counts())
order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"],
    errors="coerce"
)

print("\nOrder items data types after transformation:")
print(order_items.dtypes)

print("\nMissing shipping limit dates:")
print(order_items["shipping_limit_date"].isna().sum())
print("\nNegative prices:")
print((order_items["price"] < 0).sum())

print("\nNegative freight values:")
print((order_items["freight_value"] < 0).sum())
print("\nPrice statistics:")
print(order_items["price"].describe())

print("\nFreight value statistics:")
print(order_items["freight_value"].describe())
print("\nNegative product values:")

numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for column in numeric_columns:

    print(column, ":", (products[column] < 0).sum())

review_dates = [
    "review_creation_date",
    "review_answer_timestamp"
]

reviews = pd.read_csv(
    "data/raw/olist_order_reviews_dataset.csv"
)

for column in review_dates:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors="coerce"
    )

print("\nReview data types after transformation:")
print(reviews.dtypes)

print("\nMissing review dates:")
print(reviews[review_dates].isna().sum())

import os

os.makedirs("data/processed", exist_ok=True)

orders.to_csv(
    "data/processed/orders.csv",
    index=False
)

customers.to_csv(
    "data/processed/customers.csv",
    index=False
)

order_items.to_csv(
    "data/processed/order_items.csv",
    index=False
)

products.to_csv(
    "data/processed/products.csv",
    index=False
)

sellers.to_csv(
    "data/processed/sellers.csv",
    index=False
)

payments.to_csv(
    "data/processed/payments.csv",
    index=False
)

reviews.to_csv(
    "data/processed/reviews.csv",
    index=False
)

print("\nProcessed datasets saved successfully.")