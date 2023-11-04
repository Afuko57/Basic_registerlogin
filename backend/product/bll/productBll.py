from fastapi import HTTPException
from product.model.product_model import Product
import config.database as db

# Create a new product
def create_product(product: Product):
    connection = db.db
    try:
        with connection.cursor() as cursor:
            sql = '''INSERT INTO products (product_name, price, quantity, date_added, date_modified, product_code)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (
                product.product_name,
                product.price,
                product.quantity,
                product.date_added,
                product.date_modified,
                product.product_code,
            )
            cursor.execute(sql, values)
            connection.commit()
            return get_product_by_id(cursor.lastrowid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Product creation failed") from e

# Get all products
def get_products():
    connection = db.db
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()

            product_objects = []
            for product in products:
                product_object = Product(
                    id=product[0],
                    product_name=product[1],
                    price=product[2],
                    quantity=product[3],
                    date_added=product[4],
                    date_modified=product[5],
                    product_code=product[6],
                )
                product_objects.append(product_object)

            return product_objects
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch product.") from e

# Get a single product by ID
def get_product_by_id(product_id):
    connection = db.db
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
            product_data = cursor.fetchone()

            if product_data:
                product = Product(
                    id=product_data[0],
                    product_name=product_data[1],
                    price=product_data[2],
                    quantity=product_data[3],
                    date_added=product_data[4],
                    date_modified=product_data[5],
                    product_code=product_data[6],
                )
                return product
            else:
                raise HTTPException(status_code=404, detail="Not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch product.") from e

# Update an existing product
def update_product(product_id, product: Product):
    connection = db.db
    try:
        with connection.cursor() as cursor:
            sql = '''UPDATE products
                     SET product_name = %s,
                         price = %s,
                         quantity = %s,
                         date_modified = %s,
                         product_code = %s
                     WHERE id = %s'''
            values = (
                product.product_name,
                product.price,
                product.quantity,
                product.date_modified,
                product.product_code,
                product_id,
            )
            cursor.execute(sql, values)
            connection.commit()
            return cursor.rowcount
    except Exception as e:
        raise HTTPException(status_code=500, detail="Update Failed.") from e

# Delete a product by ID
def delete_product(product_id):
    connection = db.db
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM products WHERE id = %s'
            cursor.execute(sql, (product_id,))
            connection.commit()
            return cursor.rowcount
    except Exception as e:
        raise HTTPException(status_code=500, detail="Delete Failed.") from e
