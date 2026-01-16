from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)


class Node:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, name, price, qty):
        new_node = Node(name, price, qty)
        if self.head is None:
            self.head = new_node
        else:
            ptr = self.head
            while ptr.next:
                ptr = ptr.next
            ptr.next = new_node
        print("Debug: Added " + name + " to list")

    def get_all_items(self):
        items = []
        ptr = self.head
        grand_total = 0
        while ptr:
            t_price = ptr.price * ptr.qty
            grand_total = grand_total + t_price
            items.append({
                "name": ptr.name,
                "price": ptr.price,
                "qty": ptr.qty,
                "total": t_price
            })
            ptr = ptr.next
        return items, grand_total

    def clear_list(self):
        self.head = None


my_cart = LinkedList()

DB_HOST = "localhost"
DB_NAME = "demo"
DB_USER = "postgres"
DB_PASS = "YOUR_DB_PASSWORD"

products_list = [
    {"id": 1, "name": "Bamboo Toothbrush (4 Pack)", "price": 356.0, "image": "toothbrush.jpg"},
    {"id": 2, "name": "Reusable Steel Straw (5 Pack)", "price": 239.0, "image": "straw.jpg"},
    {"id": 3, "name": "Organic Cotton Bag (Set of 12)", "price": 379.0, "image": "bag.jpg"},
    {"id": 4, "name": "Glass Water Bottle", "price": 799.0, "image": "bottle.jpg"},
    {"id": 5, "name": "Solar Power Bank", "price": 1999.0, "image": "powerbank.jpg"},
    {"id": 6, "name": "Recycled Notebook (6 Pcs)", "price": 399.0, "image": "notebook.jpg"},
    {"id": 7, "name": "Wooden Cutlery Set (6 Pcs)", "price": 380.0, "image": "cutlery.jpg"},
    {"id": 8, "name": "Compost Trash Bags (45 Bags)", "price": 295.0, "image": "trashbags.jpg"},
    {"id": 9, "name": "Beeswax Wrap Pack (Set of 3)", "price": 418.0, "image": "beeswax.jpg"},
    {"id": 10, "name": "Hemp T-Shirt", "price": 1499.0, "image": "shirt.jpg"}
]


@app.route('/')
def home():
    return render_template('index.html', products=products_list)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    p_name = data['name']
    p_price = float(data['price'])
    p_qty = int(data['qty'])

    my_cart.add(p_name, p_price, p_qty)
    return jsonify({"msg": "Item added successfully!"})


@app.route('/get_cart_data')
def get_cart_data():
    items, total = my_cart.get_all_items()
    return jsonify({"items": items, "grand_total": total})


@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    c_name = data['c_name']

    if my_cart.head is None:
        return jsonify({"msg": "Cart is empty!"})

    try:
        con = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS EcoOrders (
            id SERIAL PRIMARY KEY,
            customer VARCHAR(50),
            product VARCHAR(50),
            qty INT,
            total_price NUMERIC(10,2)
        )
        """)

        ptr = my_cart.head
        while ptr:
            cost = ptr.price * ptr.qty

            cur.execute(
                "SELECT qty, total_price FROM EcoOrders WHERE customer=%s AND product=%s",
                (c_name, ptr.name)
            )
            row = cur.fetchone()

            if row:
                new_q = row[0] + ptr.qty
                new_p = float(row[1]) + cost
                cur.execute(
                    "UPDATE EcoOrders SET qty=%s, total_price=%s WHERE customer=%s AND product=%s",
                    (new_q, new_p, c_name, ptr.name)
                )
            else:
                cur.execute(
                    "INSERT INTO EcoOrders (customer, product, qty, total_price) VALUES (%s, %s, %s, %s)",
                    (c_name, ptr.name, ptr.qty, cost)
                )

            ptr = ptr.next

        con.commit()
        cur.close()
        con.close()

        my_cart.clear_list()
        return jsonify({"msg": "Thanks for purchasing!"})

    except Exception as e:
        print("DB Error:", e)
        return jsonify({"msg": "Database Connection Failed"})


if __name__ == '__main__':
    app.run(debug=True)
