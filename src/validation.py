import pandas as pd

BASE_PATH = "data/processed"

orders = pd.read_csv(f"{BASE_PATH}/orders.csv")
customers = pd.read_csv(f"{BASE_PATH}/customers.csv")
order_items = pd.read_csv(f"{BASE_PATH}/order_items.csv")
products = pd.read_csv(f"{BASE_PATH}/products.csv")
sellers = pd.read_csv(f"{BASE_PATH}/sellers.csv")
payments = pd.read_csv(f"{BASE_PATH}/payments.csv")
reviews = pd.read_csv(f"{BASE_PATH}/reviews.csv")


print("Orders:", orders.shape)
print("Customers:", customers.shape)
print("Order Items:", order_items.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)


print("\nDuplicate order IDs:")
print(orders["order_id"].duplicated().sum())

print("\nDuplicate customer IDs:")
print(customers["customer_id"].duplicated().sum())

print("\nDuplicate product IDs:")
print(products["product_id"].duplicated().sum())

print("\nDuplicate seller IDs:")
print(sellers["seller_id"].duplicated().sum())

print("\nDuplicate order item keys:")
print(
    order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

print("\nDuplicate payment keys:")
print(
    payments.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

print("\nDuplicate review keys:")
print(
    reviews.duplicated(
        subset=["review_id", "order_id"]
    ).sum()
)
print("\nOrders with missing customers:")
print(
    (~orders["customer_id"].isin(customers["customer_id"])).sum()
)

print("\nOrder items with missing orders:")
print(
    (~order_items["order_id"].isin(orders["order_id"])).sum()
)

print("\nOrder items with missing products:")
print(
    (~order_items["product_id"].isin(products["product_id"])).sum()
)

print("\nOrder items with missing sellers:")
print(
    (~order_items["seller_id"].isin(sellers["seller_id"])).sum()
)

print("\nPayments with missing orders:")
print(
    (~payments["order_id"].isin(orders["order_id"])).sum()
)

print("\nReviews with missing orders:")
print(
    (~reviews["order_id"].isin(orders["order_id"])).sum()
)