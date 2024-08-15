from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from MLModel import MultiArmedBandit
from sklearn.metrics.pairwise import cosine_similarity
from bson.objectid import ObjectId
from transformers import BertTokenizer, BertModel
from flask_cors import CORS
import datetime
import torch
import re
import ast 
import numpy as np

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Ecommerce"

CORS(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# mab = MultiArmedBandit()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
users_collection = mongo.db.users  # Collection for storing users
categories_collection = mongo.db.categories
rewards_collection = mongo.db.rewards


def populate_rewards_for_new_user(user_id):
    try:
        # Fetch all categories
        categories = categories_collection.find()
        reward_data = {}

        for category in categories:
            category_id = str(category['_id'])  # Assuming '_id' is used as category_id
            reward_data[category_id] = {
                "alpha":1, 
                "beta": 1
            }

        # Insert into rewards collection
        rewards_collection.insert_one({
            "user_id": user_id,
            "categories": reward_data
        })
        return {"message": "Rewards data populated successfully", "user_id": str(user_id)}, 200
    except Exception as e:
        print({"error": str(e)})
        return {"error": str(e)}, 500
    

def update_rewards_logic(user_id, category, x):

    # Retrieve the current values of alpha and beta
    user_rewards = mongo.db.rewards.find_one({"user_id": ObjectId(user_id)})
   
    if not user_rewards or category not in user_rewards['categories']:
        # print("huh")
        # print(not user_rewards)
        # print(user_rewards)
        return {"error": "Category not found for the user"}, 404

    current_alpha = user_rewards['categories'][category].get('alpha', 1)
    current_beta = user_rewards['categories'][category].get('beta', 1)

    # Calculate new values for alpha and beta
    new_alpha = current_alpha + x
    new_beta = current_beta + (1 - x)

    # Update the rewards collection
    update_result = mongo.db.rewards.update_one(
        {"user_id": ObjectId(user_id)},
        {"$set": {f"categories.{category}.alpha": new_alpha, f"categories.{category}.beta": new_beta}},
        upsert=True
    )

    if update_result.modified_count > 0 or update_result.upserted_id is not None:
        return {"message": "Rewards updated successfully"}, 200
    else:
        return {"error": "Failed to update rewards"}, 400

@app.route('/update_rewards/<user_id>/<product_id>', methods=['POST'])
def update_rewards(user_id, product_id):
    delta = request.json.get('delta')

    if delta is None:
        return jsonify({"error": "delta is required"}), 400

    try:
        delta = float(delta)
        product = mongo.db.products.find_one({'_id':ObjectId(product_id)})
        if product:
            category = mongo.db.categories.find_one({'sub_category':product['sub_category']})
            if category:
                response, status_code = update_rewards_logic(user_id, str(category['_id']), delta)
            else:
                return jsonify({"error":"category not found"}),400
        else:
            return jsonify({"error":"product not found"}),400
        
        return jsonify(response), status_code

    except ValueError:
        return jsonify({"error": "Invalid value for delta"}), 400


@app.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "cart":[],
        "previous_history":[]
    }).inserted_id

    # if(populate_response.get('error',"no_error")!="no_error"):
    #     return jsonify({"message": "error populating the rewards table", "user_id": str(user_id)}),201

    return populate_rewards_for_new_user(user_id)


@app.route('/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users_collection.find_one({"username": username})

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful", "user_id": str(user['_id'])}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc
def tensor_to_numpy(tensor):
    if tensor.requires_grad:  # Check if the tensor requires gradients
        tensor = tensor.detach()  # Detach from the computation graph
    if tensor.is_cuda:  # Check if the tensor is on GPU
        tensor = tensor.cpu()  # Move to CPU
    return tensor.numpy()  # Convert to NumPy array

# Function to get user data (not as an endpoint)
def get_user_data(user_id):
    # print(user_id)
    # userId = str(user_id)
    return mongo.db.users.find_one({'_id': ObjectId(user_id)})

# Endpoint to get user embeddings for recommendations
def getembedding(text):
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    print(type(output.pooler_output))
    return tensor_to_numpy(output.pooler_output)

def get_user_embeddings(user_id):
    user_data = get_user_data(user_id)
    
    if not user_data or 'previous_history' not in user_data:
        print("There There")
        return []

    # Retrieve and concatenate product descriptions
    product_descriptions = ""
    for order in user_data['previous_history']:
        print("order")
        # print(order)
        for product in order['items']:
            # print(product)
            product_data = mongo.db.products.find_one({'_id': ObjectId(product['product_id'])})
            print(product_data)
            if product_data and 'name' in product_data:
                product_descriptions += product_data['name'] + " "
                # print(product_descriptions)
                print("product_descriptions")

    if not product_descriptions:
        return []

    # Tokenize and encode the concatenated descriptions using BERT
    # inputs = tokenizer(product_descriptions, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    # with torch.no_grad():
    #     outputs = model(**inputs)

    # Get the embedding (usually using the [CLS] token's embedding, which is the first token)
    # user_embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
    user_embedding = getembedding(product_descriptions)
    # print(user_embedding.detach().numpy())
    print(type(user_embedding))
    return user_embedding

@app.route('/get_all_products', methods=['GET'])
def get_all_products():
    try:
        products = mongo.db.products.find()  # Retrieve all products
        product_list = []
        for product in products:
            # Convert ObjectId to string and exclude MongoDB internal fields
            product['_id'] = str(product['_id'])
            product_list.append(product)
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_category_embedding():
    categories = mongo.db.categories.find()  # Assuming you have a 'categories' collection
    category_embeddings = {}

    for category in categories:
        category_name = category.get('sub_category')
        category_embedding = category.get('embeddings')
        if category_name and category_embedding:
            category_embeddings[category_name] = category_embedding

    return category_embeddings
def extract_2d_array_list(data_str):

    data_str = data_str.replace('\n', ' ')

    # Replace one or more spaces with a single comma
    data_str = re.sub(r'\s+', ',', data_str)

    # Ensure there are no extra commas at the end
    data_str = '[' + data_str.strip(',') + ']'

    # Evaluate the string safely
    numbers = ast.literal_eval(data_str)

    array = np.array(numbers).reshape((-1, 768))  
    return array

@app.route('/get_recommendation/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    user_embedding = get_user_embeddings(user_id)
    # print(user_embedding)
    # print(len(user_embedding))
    category_embedding = get_category_embedding()
    # print("help")
    category_similarity = {}
    # print(category_embedding)
    # print(user_embedding)
    for ch in category_embedding:
        print(ch)
        # print(type(category_embedding[ch]))
        print(len(user_embedding))
        category_similarity[ch] = cosine_similarity(user_embedding,extract_2d_array_list(category_embedding[ch]))[0][0]

    sorted_dict = dict(sorted(category_similarity.items(), key=lambda item: item[1], reverse=True))

    # print(sorted_dict)
    i=0
    ls = list(sorted_dict.keys())
    # for item in sorted_dict:
    #     print(item.key)
    #     ls.append(item[0])
    #     i+=1
    #     if (i==5):
    #         break
    ls = ls[:5]
    print(ls)
    alpha_beta_similarity = {}
    for category in ls:
        rewards_data = mongo.db.rewards.find_one({"user_id": ObjectId(user_id)})
        print(rewards_data['categories'])
        print(category)
        category_record = mongo.db.categories.find_one({'sub_category': category})
        category_id = str(category_record['_id'])
        alpha = rewards_data['categories'][category_id]['alpha']
        print(alpha)
        beta = rewards_data['categories'][category_id]['beta']
        print(beta)
        alpha_beta_similarity[category] = alpha/(alpha+beta)
    
    sorted_dict_rewards = dict(sorted(alpha_beta_similarity.items(), key=lambda item: item[1], reverse=True))
    lsf = []
    for item in sorted_dict_rewards:
        lsf.append(item[0])

    recommendations = []
    for category in lsf:
        category_list = mongo.db.products.find({'sub_category': category})
        top_2_items = sorted(category_list, key=lambda x: x.ratings, reverse=True)[:2]
        recommendations.extend(top_2_items)
    
    return jsonify(recommendations), 200

@app.route('/get_previous_orders/<user_id>', methods=['GET'])
def get_previous_orders(user_id):
    try:
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user_data:
            return jsonify({"error": "User not found"}), 404
        
        previous_history = user_data.get('previous_history', [])
        
        # Fetch product details for each order
        orders_with_details = []
        for order in previous_history:
            order_details = {'order_id': order['order_id'], 'items': [],'date':order['date']}
            for item in order['items']:
                product_id = ObjectId(item['product_id'])
                product = mongo.db.products.find_one({'_id': product_id})
                if product:
                    product_info = {
                        'name': product.get('name'),
                        'image': product.get('image'),
                        'price': product.get('discount_price'),
                        'quantity': item['quantity']
                    }
                    order_details['items'].append(product_info)
            orders_with_details.append(order_details)
        
        return jsonify(orders_with_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/checkout/<user_id>', methods=['POST'])
def checkout(user_id):
    # print(user_id)
    try:
        # Retrieve the user
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Generate a new order ID
        order_id = str(ObjectId())

        # Retrieve cart items from the database
        cart_items = user.get('cart', [])

        # Create the order record
        order_record = {
            'order_id': order_id,
            'items': cart_items,
            'date': datetime.datetime.now()
        }

        # Add to previous history
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$push': {'previous_history': order_record}}
        )

        # Clear the cart
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'cart': []}}
        )

        # Process each cart item for rewards
        for item in cart_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)  # Default quantity to 1 if not specified

            # Retrieve the product details
            product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
            if product:
                sub_category = product.get('sub_category')
                if sub_category:
                    # Retrieve category details
                    category = mongo.db.categories.find_one({'sub_category': sub_category})

                    if category:
                        # Update rewards based on the quantity of the product
                        category_id = str(category['_id'])
                        for _ in range(0,quantity):
                            update_rewards_logic(user_id, category_id, 1)

        return jsonify({"message": "Purchase successful!"}), 200

    except Exception as e:
        print(f"Error during checkout: {e}")
        return jsonify({"error": "An error occurred during checkout"}), 500


## Cart Operations

@app.route('/add_to_cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    # print(user_id)
    product_id = request.json.get('product_id')
    
    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Check if the user exists
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    
    # Check if the product exists
    product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    category = mongo.db.categories.find_one({'sub_category':product['sub_category']})

    #x -> 0.8
    update_rewards_logic(user_id, str(category['_id']), 0.8)

    # Update cart
    cart = user_data.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            mongo.db.users.update_one(
                {'_id': ObjectId(user_id), 'cart.product_id': product_id},
                {'$inc': {'cart.$.quantity': 1}}
            )
            return jsonify({"message": "Product quantity updated"}), 200

    # Add new product to the cart
    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$push': {'cart': {'product_id': product_id, 'quantity': 1}}}
    )

    return jsonify({"message": "Product added to cart"}), 200


@app.route('/remove_from_cart/<user_id>', methods=['POST'])
def remove_from_cart(user_id):
    product_id = request.json.get('product_id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Check if the user exists
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    # Update cart
    cart = user_data.get('cart', [])
    for item in cart:
        if item['product_id'] == product_id:
            print(item['quantity'])
            if item['quantity'] > 1:
                mongo.db.users.update_one(
                    {'_id': ObjectId(user_id), 'cart.product_id': product_id},
                    {'$inc': {'cart.$.quantity': -1}}
                )
            else:
                print("entered")
                mongo.db.users.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$pull': {'cart': {'product_id': product_id}}}
                )
                print("entered")
            return jsonify({"message": "Product removed from cart"}), 200

    return jsonify({"error": "Product not in cart"}), 404


@app.route('/get_cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_data and 'cart' in user_data:
        cart_products = []
        for item in user_data['cart']:
            product = mongo.db.products.find_one({'_id': ObjectId(item['product_id'])})
            if product:
                product['quantity'] = item['quantity']
                product['_id'] = str(product['_id'])
                cart_products.append(product)
        return jsonify(cart_products)
    else:
        return jsonify({"error": "User not found or cart is empty"}), 404



if __name__ == '__main__':
    app.run(debug=True)


# # Endpoint to get product data
# @app.route('/get_product_data/<product_id>', methods=['GET'])
# def get_product_data(product_id):
#     product_data = mongo.db.products.find_one({'productid': product_id})
#     if product_data:
#         return jsonify(serialize_doc(product_data))
#     else:
#         return jsonify({"error": "Product not found"}), 404

# @app.route('/rewards/<user_id>/<category>', methods=['GET'])
# def get_rewards(user_id, category):
#     rewards_data = mongo.db.rewards.find_one({"user_id": user_id}, {f"{category}": 1})
#     if rewards_data and category in rewards_data:
#         alpha = rewards_data[category][0]
#         beta = rewards_data[category][1]
#         return jsonify(rewards_data[category]), 200
#     else:
#         return jsonify({"error": "User or category not found"}), 404


# @app.route('/rewards/<user_id>/<category>', methods=['PUT'])
# def update_rewards(user_id, category):
#     alpha = request.json.get('alpha')
#     beta = request.json.get('beta')

#     if alpha is None or beta is None:
#         return jsonify({"error": "Both alpha and beta are required"}), 400

#     update_result = mongo.db.rewards.update_one(
#         {"user_id": user_id},
#         {"$set": {f"{category}.alpha": alpha, f"{category}.beta": beta}},
#         upsert=True
#     )

#     if update_result.modified_count > 0 or update_result.upserted_id is not None:
#         return jsonify({"message": "Rewards updated successfully"}), 200
#     else:
#         return jsonify({"error": "Failed to update rewards"}), 400


##checkout past
# @app.route('/checkout/<user_id>', methods=['POST'])
# def checkout(user_id):
#     print(user_id)
#     try:
#         # Retrieve the user
#         user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
#         if not user:
#             return jsonify({"error": "User not found"}), 404

#         # Generate a new order ID
#         order_id = str(ObjectId())

#         # Retrieve cart items from the database
#         cart_items = user.get('cart', [])

#         # Create the order record
#         order_record = {
#             'order_id': order_id,
#             'items': cart_items,
#             'date': datetime.datetime.now()
#         }

#         # Add to previous history
#         mongo.db.users.update_one(
#             {'_id': ObjectId(user_id)},
#             {'$push': {'previous_history': order_record}}
#         )

#         # Clear the cart
#         mongo.db.users.update_one(
#             {'_id': ObjectId(user_id)},
#             {'$set': {'cart': []}}
#         )

#         return jsonify({"message": "Purchase successful!"}), 200

#     except Exception as e:
#         print(f"Error during checkout: {e}")
#         return jsonify({"error": "An error occurred during checkout"}), 500