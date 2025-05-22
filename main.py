from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import pandas as pd
from fastapi.responses import JSONResponse
from psycopg2 import sql as psycopg2_sql

app = FastAPI()

# PostgreSQL connection settings
DB_CONFIG = {
    "host": "dpg-d0mucfjuibrs73f20utg-a.oregon-postgres.render.com",
    "port": 5432,
    "database": "nocodeql_db",
    "user": "nocodeql_db_user",
    "password": "KM5oxbbw7TopSEI9OOBNATnTdgfgsdwM"
}

# Request body format
class QueryRequest(BaseModel):
    sql: str

@app.post("/run-sql")
def run_sql(request: QueryRequest):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        df = pd.read_sql_query(request.sql, conn)
        conn.close()
        return {"result": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}

@app.get("/init-db")
def init_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Drop tables if they exist
        cur.execute("DROP TABLE IF EXISTS order_items;")
        cur.execute("DROP TABLE IF EXISTS orders;")
        cur.execute("DROP TABLE IF EXISTS products;")

        # Create products table
        cur.execute("""
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL
        );
        """)

        # Create orders table
        cur.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            customer_name TEXT NOT NULL,
            order_date DATE NOT NULL
        );
        """)

        # Create order_items table
        cur.execute("""
        CREATE TABLE order_items (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL
        );
        """)

        # Insert products
        cur.execute("""
        INSERT INTO products (name, category, price) VALUES
        ('Milk', 'Dairy', 50),
        ('Bread', 'Bakery', 30),
        ('Eggs (12 pack)', 'Poultry', 60),
        ('Soap Bar', 'Toiletries', 20),
        ('Shampoo', 'Toiletries', 120);
        """)

        # Insert orders
        cur.execute("""
        INSERT INTO orders (customer_name, order_date) VALUES
        ('Ramesh', '2025-05-01'),
        ('Priya', '2025-05-02'),
        ('Anjali', '2025-05-04'),
        ('Vijay', '2025-05-05'),
        ('Leela', '2025-05-06'),
        ('Suresh', '2025-05-07'),
        ('Sneha', '2025-05-08');
        """)

        # Insert order_items (expanded data)
        cur.execute("""
        INSERT INTO order_items (order_id, product_id, quantity) VALUES
        (1, 1, 2),
        (1, 4, 1),
        (2, 2, 1),
        (2, 5, 1),
        (3, 3, 1),
        (3, 1, 1),
        (4, 2, 2),
        (4, 5, 1),
        (5, 1, 3),
        (5, 3, 1),
        (6, 4, 2),
        (6, 5, 2),
        (7, 1, 1),
        (7, 2, 1),
        (7, 4, 1);
        """)

        conn.commit()
        conn.close()
        return JSONResponse({"message": "✅ Retail demo (expanded) data inserted successfully."})

    except Exception as e:
        return JSONResponse({"error": str(e)})
