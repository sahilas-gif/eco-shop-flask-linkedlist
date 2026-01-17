# 🌿 Eco-Friendly Shopping Store

Hey! This is my full-stack web development project. It's an e-commerce store for sustainable products that I built using **Python Flask** and **PostgreSQL**.

The cool part about this project is that I didn't just use a standard list for the shopping cart—I implemented a **Linked List** from scratch to handle the cart logic (adding items, calculating totals, etc.).

## Features
* **Product Page:** Browse eco-friendly items in a grid layout.
* **Smart Cart:** Uses a custom Linked List data structure to manage your items in memory.
* **Database Integration:** When you checkout, your order is actually saved to a local PostgreSQL database.
* **REST API:** The frontend talks to the backend using JSON.

## Tech Stack
* **Language:** Python
* **Framework:** Flask
* **Database:** PostgreSQL (using `psycopg2`)
* **Frontend:** HTML, CSS, JS

---

## How to Run This on Your Machine

### 1. Download the code
Clone this repo or download the zip file and extract it.
```bash
git clone [https://github.com/sahilas-gif/eco-shop-flask-linkedlist.git](https://github.com/sahilas-gif/eco-shop-flask-linkedlist.git)

2. Install the libraries
I included a requirements.txt file. Just run this to get Flask and the DB connector:

Bash

pip install -r requirements.txt
3. Database Setup (⚠️ Important!)
You need to set up your local database for this to work.

Open pgAdmin or your terminal.

Create a new database named demo.

Update the password in the code:

Open app.py in your code editor.

Scroll down to around line 55 where you see DB_PASS.

Change the password there to match your own PostgreSQL password.

Python

# In app.py
DB_PASS = "YOUR_ACTUAL_PASSWORD_HERE"  
4. Run the App
Bash

python app.py
Go to http://127.0.0.1:5000/ in your browser.
