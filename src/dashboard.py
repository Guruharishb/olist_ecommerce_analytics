import tkinter as tk
from tkinter import ttk, messagebox

from src.query import (
    get_overview,
    get_monthly_revenue,
    get_top_products,
    get_top_sellers,
    get_top_customers,
    get_payment_distribution,
    get_delivery_analysis,
    get_order_status,
    get_review_analysis
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


BG = "#f4f6f8"
CARD = "#ffffff"
TEXT = "#222222"

root = tk.Tk()
root.title("Olist E-Commerce Analytics")
root.geometry("1200x750")
root.configure(bg=BG, padx=10, pady=10)


def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)


def create_tree(parent, columns, headings, widths=None):
    tree = ttk.Treeview(
        parent,
        columns=columns,
        show="headings",
        height=12
    )

    for index, column in enumerate(columns):
        tree.heading(column, text=headings[index])

        if widths:
            tree.column(column, width=widths[index])
        else:
            tree.column(column, width=180)

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    return tree


def create_card(parent, title, value, column):
    frame = tk.Frame(
        parent,
        bg=CARD,
        bd=1,
        relief="solid"
    )

    frame.grid(
        row=0,
        column=column,
        padx=5,
        pady=10,
        sticky="nsew"
    )

    title_label = tk.Label(
        frame,
        text=title,
        font=("Arial", 10),
        bg=CARD,
        fg=TEXT
    )

    title_label.pack(
        pady=(15, 5)
    )

    value_label = tk.Label(
        frame,
        text=value,
        font=("Arial", 16, "bold"),
        bg=CARD,
        fg=TEXT
    )

    value_label.pack(
        pady=(5, 15)
    )

    return value_label


def show_overview():
    try:
        result = get_overview()

        total_orders = result[0] or 0
        total_revenue = result[1] or 0
        average_order_value = result[2] or 0
        average_delivery = result[3] or 0
        cancellation_rate = result[4] or 0

        orders_value.config(
            text=f"{total_orders:,}"
        )

        revenue_value.config(
            text=f"₹ {total_revenue:,.2f}"
        )

        aov_value.config(
            text=f"₹ {average_order_value:,.2f}"
        )

        delivery_value.config(
            text=f"{average_delivery:.2f} days"
        )

        cancellation_value.config(
            text=f"{cancellation_rate:.2f}%"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def show_monthly_revenue():
    try:
        result = get_monthly_revenue()

        clear_tree(monthly_tree)

        months = []
        revenues = []

        for row in result:
            monthly_tree.insert(
                "",
                "end",
                values=row
            )

            months.append(str(row[0]))
            revenues.append(float(row[1] or 0))

        draw_chart(
            chart_frame,
            months,
            revenues,
            "Monthly Revenue",
            "Revenue"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )
def show_products():
    try:
        result = get_top_products()

        clear_tree(monthly_tree)

        monthly_tree.configure(
            columns=("product", "category", "units", "revenue"),
            show="headings"
        )

        monthly_tree.heading("product", text="Product ID")
        monthly_tree.heading("category", text="Category")
        monthly_tree.heading("units", text="Units Sold")
        monthly_tree.heading("revenue", text="Revenue")

        monthly_tree.column("product", width=180)
        monthly_tree.column("category", width=180)
        monthly_tree.column("units", width=100)
        monthly_tree.column("revenue", width=120)

        for row in result:
            monthly_tree.insert(
                "",
                "end",
                values=row
            )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )
def show_sellers():
    try:
        result = get_top_sellers()

        clear_tree(monthly_tree)

        monthly_tree.configure(
            columns=("seller", "items", "revenue"),
            show="headings"
        )

        monthly_tree.heading("seller", text="Seller ID")
        monthly_tree.heading("items", text="Items Sold")
        monthly_tree.heading("revenue", text="Revenue")

        monthly_tree.column("seller", width=220)
        monthly_tree.column("items", width=120)
        monthly_tree.column("revenue", width=150)

        for row in result:
            monthly_tree.insert(
                "",
                "end",
                values=row
            )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )
def show_customers():
    try:
        result = get_top_customers()

        clear_tree(customers_tree)

        for row in result:
            customers_tree.insert(
                "",
                "end",
                values=row
            )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def show_payments():
    try:
        result = get_payment_distribution()

        clear_tree(payments_tree)

        payment_types = []
        payment_values = []

        for row in result:
            payments_tree.insert(
                "",
                "end",
                values=row
            )

            payment_types.append(str(row[0]))
            payment_values.append(float(row[2] or 0))

        draw_chart(
            payment_chart_frame,
            payment_types,
            payment_values,
            "Payment Distribution",
            "Payment Value"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def show_delivery():
    try:
        result = get_delivery_analysis()

        delivered = result[0] or 0
        average = result[1] or 0
        fastest = result[2] if result[2] is not None else 0
        slowest = result[3] if result[3] is not None else 0
        late = result[4] or 0

        delivered_orders.config(
            text=f"{delivered:,}"
        )

        average_delivery_result.config(
            text=f"{average:.2f} days"
        )

        fastest_delivery.config(
            text=f"{fastest} days"
        )

        slowest_delivery.config(
            text=f"{slowest} days"
        )

        late_orders.config(
            text=f"{late:,}"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def show_status():
    try:
        result = get_order_status()

        clear_tree(status_tree)

        statuses = []
        counts = []

        for row in result:
            status_tree.insert(
                "",
                "end",
                values=row
            )

            statuses.append(str(row[0]))
            counts.append(int(row[1]))

        draw_chart(
            status_chart_frame,
            statuses,
            counts,
            "Order Status",
            "Orders"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def show_reviews():
    try:
        result = get_review_analysis()

        clear_tree(reviews_tree)

        scores = []
        counts = []

        for row in result:
            reviews_tree.insert(
                "",
                "end",
                values=row
            )

            scores.append(str(row[0]))
            counts.append(int(row[1]))

        draw_chart(
            review_chart_frame,
            scores,
            counts,
            "Review Score Distribution",
            "Reviews"
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def draw_chart(parent, x_values, y_values, title, y_label):
    for widget in parent.winfo_children():
        widget.destroy()

    figure = Figure(
        figsize=(8, 4),
        dpi=100
    )

    axis = figure.add_subplot(111)

    axis.bar(
        x_values,
        y_values
    )

    axis.set_title(title)
    axis.set_ylabel(y_label)

    axis.tick_params(
        axis="x",
        rotation=45
    )

    figure.tight_layout()

    canvas = FigureCanvasTkAgg(
        figure,
        master=parent
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass


title = tk.Label(
    root,
    text="Olist E-Commerce Analytics Dashboard",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=TEXT
)

title.pack(
    pady=(0, 15)
)


notebook = ttk.Notebook(root)

notebook.pack(
    fill="both",
    expand=True
)


overview_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    overview_tab,
    text="Overview"
)


overview_cards = tk.Frame(
    overview_tab,
    bg=BG
)

overview_cards.pack(
    fill="x"
)

for i in range(5):
    overview_cards.columnconfigure(
        i,
        weight=1
    )


orders_value = create_card(
    overview_cards,
    "Total Orders",
    "Loading...",
    0
)

revenue_value = create_card(
    overview_cards,
    "Total Revenue",
    "Loading...",
    1
)

aov_value = create_card(
    overview_cards,
    "Average Order Value",
    "Loading...",
    2
)

delivery_value = create_card(
    overview_cards,
    "Average Delivery",
    "Loading...",
    3
)

cancellation_value = create_card(
    overview_cards,
    "Cancellation Rate",
    "Loading...",
    4
)


tk.Button(
    overview_tab,
    text="Refresh Overview",
    command=show_overview,
    width=20
).pack(
    pady=30
)


sales_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    sales_tab,
    text="Sales"
)


sales_buttons = tk.Frame(
    sales_tab,
    bg=BG
)

sales_buttons.pack(
    pady=10
)


tk.Button(
    sales_buttons,
    text="Monthly Revenue",
    command=show_monthly_revenue,
    width=20
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    sales_buttons,
    text="Top Products",
    command=show_products,
    width=20
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    sales_buttons,
    text="Top Sellers",
    command=show_sellers,
    width=20
).grid(
    row=0,
    column=2,
    padx=5
)


monthly_tree = create_tree(
    sales_tab,
    ("month", "revenue"),
    ("Month", "Revenue"),
    (250, 250)
)


chart_frame = tk.Frame(
    sales_tab,
    bg=CARD
)

chart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


products_tree = create_tree(
    sales_tab,
    (
        "product_id",
        "category",
        "units_sold",
        "revenue"
    ),
    (
        "Product ID",
        "Category",
        "Units Sold",
        "Revenue"
    ),
    (250, 250, 150, 180)
)

products_tree.pack_forget()


sellers_tree = create_tree(
    sales_tab,
    (
        "seller_id",
        "items_sold",
        "revenue"
    ),
    (
        "Seller ID",
        "Items Sold",
        "Revenue"
    ),
    (300, 200, 200)
)

sellers_tree.pack_forget()


customers_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    customers_tab,
    text="Customers"
)


tk.Button(
    customers_tab,
    text="Load Top Customers",
    command=show_customers,
    width=25
).pack(
    pady=10
)


customers_tree = create_tree(
    customers_tab,
    (
        "customer",
        "orders",
        "spent"
    ),
    (
        "Customer",
        "Orders",
        "Total Spent"
    ),
    (400, 150, 250)
)


payments_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    payments_tab,
    text="Payments"
)


tk.Button(
    payments_tab,
    text="Load Payment Analysis",
    command=show_payments,
    width=25
).pack(
    pady=10
)


payments_tree = create_tree(
    payments_tab,
    (
        "type",
        "count",
        "value"
    ),
    (
        "Payment Type",
        "Count",
        "Total Value"
    ),
    (300, 200, 250)
)


payment_chart_frame = tk.Frame(
    payments_tab,
    bg=CARD
)

payment_chart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


delivery_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    delivery_tab,
    text="Delivery"
)


delivery_cards = tk.Frame(
    delivery_tab,
    bg=BG
)

delivery_cards.pack(
    fill="x"
)

for i in range(5):
    delivery_cards.columnconfigure(
        i,
        weight=1
    )


delivered_orders = create_card(
    delivery_cards,
    "Delivered Orders",
    "-",
    0
)

average_delivery_result = create_card(
    delivery_cards,
    "Average Delivery",
    "-",
    1
)

fastest_delivery = create_card(
    delivery_cards,
    "Fastest Delivery",
    "-",
    2
)

slowest_delivery = create_card(
    delivery_cards,
    "Slowest Delivery",
    "-",
    3
)

late_orders = create_card(
    delivery_cards,
    "Late Orders",
    "-",
    4
)


tk.Button(
    delivery_tab,
    text="Load Delivery Analysis",
    command=show_delivery,
    width=25
).pack(
    pady=30
)


status_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    status_tab,
    text="Order Status"
)


tk.Button(
    status_tab,
    text="Load Order Status",
    command=show_status,
    width=25
).pack(
    pady=10
)


status_tree = create_tree(
    status_tab,
    (
        "status",
        "count"
    ),
    (
        "Order Status",
        "Orders"
    ),
    (350, 250)
)


status_chart_frame = tk.Frame(
    status_tab,
    bg=CARD
)

status_chart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


reviews_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    reviews_tab,
    text="Reviews"
)


tk.Button(
    reviews_tab,
    text="Load Review Analysis",
    command=show_reviews,
    width=25
).pack(
    pady=10
)


reviews_tree = create_tree(
    reviews_tab,
    (
        "score",
        "count"
    ),
    (
        "Review Score",
        "Reviews"
    ),
    (350, 250)
)


review_chart_frame = tk.Frame(
    reviews_tab,
    bg=CARD
)

review_chart_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


show_overview()

root.mainloop()