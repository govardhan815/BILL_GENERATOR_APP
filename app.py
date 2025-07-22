from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'database.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product TEXT NOT NULL,
            qty INTEGER NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL
        )''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    customer = request.form['customer']
    product = request.form['product']
    qty = int(request.form['qty'])
    price = float(request.form['price'])
    total = qty * price

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO bills (customer, product, qty, price, total) VALUES (?, ?, ?, ?, ?)",
              (customer, product, qty, price, total))
    bill_id = c.lastrowid
    conn.commit()
    conn.close()
    return redirect(url_for('show_bill', bill_id=bill_id))

@app.route('/bill/<int:bill_id>')
def show_bill(bill_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM bills WHERE id = ?", (bill_id,))
    row = c.fetchone()
    conn.close()
    return render_template('bill.html', bill=row)

@app.route('/view')
def view_bills():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM bills")
    rows = c.fetchall()
    conn.close()
    return render_template('view_bills.html', data=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
