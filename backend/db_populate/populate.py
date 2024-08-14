import pandas as pd
from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://localhost:23017/')
db = client['Ecommerce']

# Read CSV Files
products_df = pd.read_csv('products.csv')
users_df = pd.read_csv('users.csv')

# Populate Products Collection
products_collection = db['products']
products_data = []

for _, row in products_df.iterrows():
    product = {
        'productid': row['productid'],
        'product_name': row['product_name'],
        'category': row['category'],
        'acutal_price': row['actual_price'],
        'image_url': row['image_url'],
        'discount_price': row['discount_price'],
        'rating': row['rating'],
        'number_of_ratings': row['number_of_ratings'],
        'product_embedding': json.loads(row['product_embedding'])  # Assuming embedding is stored as a JSON array in CSV
    }
    products_data.append(product)

products_collection.insert_many(products_data)

# Populate Users Collection
users_collection = db['users']
users_data = []

for _, row in users_df.iterrows():
    user = {
        'userId': row['userId'],
        'username': row['username'],
        'password': row['password'],  # Ensure passwords are hashed in real scenarios
        'cart': json.loads(row['cart']),  # Assuming cart is a JSON array in CSV
        'previous_history': json.loads(row['previous_history'])  # Assuming previous history is a JSON object in CSV
    }
    users_data.append(user)

users_collection.insert_many(users_data)

# Populate Category Collection (Derived from Products Data)
categories_collection = db['categories']
categories_data = products_df.groupby('category')['product_embedding'].apply(list).to_dict()

for category, embeddings in categories_data.items():
    avg_embedding = [sum(x)/len(x) for x in zip(*embeddings)]  # Average the embeddings
    category_doc = {
        'name': category,
        'avg_embedding': avg_embedding
    }
    categories_collection.insert_one(category_doc)

print("Database populated successfully!")
