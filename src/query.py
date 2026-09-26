from src.database import get_connection


def get_overview():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            (select count(*) from orders),
            (select sum(payment_value) from payments),
            (
                select avg(order_total)
                from (
                    select order_id, sum(payment_value) as order_total
                    from payments
                    group by order_id
                ) as order_payments
            ),
            (select avg(delivery_days) from orders),
            (
                select
                    100.0 * sum(
                        case
                            when order_status = 'canceled' then 1
                            else 0
                        end
                    ) / count(*)
                from orders
            )
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_monthly_revenue():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            date_format(o.order_purchase_timestamp, '%Y-%m') as month,
            round(sum(p.payment_value), 2) as revenue
        from orders o
        join payments p
            on o.order_id = p.order_id
        group by
            date_format(o.order_purchase_timestamp, '%Y-%m')
        order by month
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_top_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            oi.product_id,
            coalesce(p.product_category_name, 'unknown') as category,
            count(*) as units_sold,
            round(sum(oi.price), 2) as revenue
        from order_items oi
        left join products p
            on oi.product_id = p.product_id
        group by
            oi.product_id,
            p.product_category_name
        order by units_sold desc
        limit 10
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_top_sellers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            seller_id,
            count(*) as items_sold,
            round(sum(price), 2) as revenue
        from order_items
        group by seller_id
        order by revenue desc
        limit 10
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_top_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            c.customer_unique_id,
            count(o.order_id) as orders_count,
            round(sum(p.payment_value), 2) as total_spent
        from customers c
        join orders o
            on c.customer_id = o.customer_id
        join payments p
            on o.order_id = p.order_id
        group by c.customer_unique_id
        order by total_spent desc
        limit 10
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_payment_distribution():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            payment_type,
            count(*) as payment_count,
            round(sum(payment_value), 2) as total_value
        from payments
        group by payment_type
        order by total_value desc
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_delivery_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            count(*) as delivered_orders,
            round(avg(delivery_days), 2) as average_delivery_days,
            min(delivery_days) as fastest_delivery,
            max(delivery_days) as slowest_delivery,
            sum(
                case
                    when order_delivered_customer_date >
                         order_estimated_delivery_date
                    then 1
                    else 0
                end
            ) as late_orders
        from orders
        where order_delivered_customer_date is not null
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_order_status():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            order_status,
            count(*) as order_count
        from orders
        group by order_status
        order by order_count desc
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_review_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        select
            review_score,
            count(*) as review_count
        from reviews
        group by review_score
        order by review_score
    """)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result