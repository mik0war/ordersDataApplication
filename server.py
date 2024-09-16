from flask import Flask, jsonify
import psycopg2

from order import Order, Product

application = Flask(__name__)

def create_connection():

    connection = psycopg2.connect(host='127.0.0.1', port='5432',
                                  database='OrdersApplicationDB', user='administrator', password='root')

    cursor = connection.cursor()

    return connection, cursor


@application.route('/order/<int:order_id>')
@application.route('/order/all')
def get_all_orders(order_id=None):
    connection, cursor = create_connection()

    if order_id is None:
        cursor.execute('''SELECT Order_.orderId, user_fio, description, date_time, Product.productId, name_, cost, count
                            FROM Order_ 
                            JOIN ProductOrder 
                            ON ProductOrder.OrderId = Order_.OrderId
    
                            JOIN Product 
                            ON Product.ProductId = ProductOrder.ProductId''')
    else:
        cursor.execute('''SELECT Order_.orderId, user_fio, description, date_time, Product.productId, name_, cost, count
                                FROM Order_ 
                                JOIN ProductOrder 
                                ON ProductOrder.OrderId = Order_.OrderId
        
                                JOIN Product 
                                ON Product.ProductId = ProductOrder.ProductId
                                WHERE Order_.OrderId = %s''', [order_id])

    orders_data = cursor.fetchall()
    close_connection(connection, cursor)

    objects_list = []
    print(orders_data)
    for line in orders_data:
        if objects_list.__len__() == 0 or objects_list[objects_list.__len__()-1].id != line[0]:
            objects_list.append(Order(line[0], line[1], line[3], line[2],
                                [Product(line[5], line[6], line[7])]))
        else:
            objects_list[objects_list.__len__() - 1].products.append(
                Product(line[5], line[6], line[7]))

    dict_result = []

    for line in objects_list:
        line.products = [i.__dict__ for i in line.products]
        dict_result.append(line.__dict__)

    return dict_result


def close_connection(con, cur):
    con.close()
    cur.close()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5001)
