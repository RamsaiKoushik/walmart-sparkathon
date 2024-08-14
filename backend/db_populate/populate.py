import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:23017/')
db = client['Ecommerce']


products_collection = db['products']
categories_collection = db['categories']

products_df = pd.read_csv("Hidden products.csv")
categories_df = pd.read_csv("average_embeddings.csv")

# Convert the dataframe to a dictionary and insert into MongoDB
records = products_df.to_dict(orient='records')
products_collection.insert_many(records)

# Rename columns to match MongoDB collection
categories_df.rename(columns={'sub_category': 'category_name', 'embeddings': 'avg_embedding'}, inplace=True)
# Convert the dataframe to a dictionary and insert into MongoDB

records = categories_df.to_dict(orient='records')
categories_collection.insert_many(records)


# # Populate Products Collection
# products_collection = db['products']
# products_data = []

# for _, row in products_df.iterrows():
#     product = {
#         'product_id': row['productid'],
#         'product_name': row['product_name'],
#         'category': row['category'],
#         'acutal_price': row['actual_price'],
#         'image_url': row['image_url'],
#         'discount_price': row['discount_price'],
#         'rating': row['rating'],
#         'number_of_ratings': row['number_of_ratings'],
#         'product_embedding': row['product_embedding'] 
#     }
#     products_data.append(product)

# products_collection.insert_many(products_data)