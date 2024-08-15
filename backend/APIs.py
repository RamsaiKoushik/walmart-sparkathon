from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from MLModel import MultiArmedBandit
from sklearn.metrics.pairwise import cosine_similarity
from bson.objectid import ObjectId
from transformers import BertTokenizer, BertModel
from flask_cors import CORS
import torch

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:23017/Ecommerce"

CORS(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# mab = MultiArmedBandit()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
users_collection = mongo.db.users  # Collection for storing users


@app.route('/rewards/<user_id>/<category>', methods=['GET'])
def get_rewards(user_id, category):
    rewards_data = mongo.db.rewards.find_one({"user_id": user_id}, {f"{category}": 1})
    if rewards_data and category in rewards_data:
        alpha = rewards_data[category][0]
        beta = rewards_data[category][1]
        return jsonify(rewards_data[category]), 200
    else:
        return jsonify({"error": "User or category not found"}), 404


@app.route('/rewards/<user_id>/<category>', methods=['PUT'])
def update_rewards(user_id, category):
    alpha = request.json.get('alpha')
    beta = request.json.get('beta')

    if alpha is None or beta is None:
        return jsonify({"error": "Both alpha and beta are required"}), 400

    update_result = mongo.db.rewards.update_one(
        {"user_id": user_id},
        {"$set": {f"{category}.alpha": alpha, f"{category}.beta": beta}},
        upsert=True
    )

    if update_result.modified_count > 0 or update_result.upserted_id is not None:
        return jsonify({"message": "Rewards updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update rewards"}), 400


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

    return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201


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

# Function to get user data (not as an endpoint)
def get_user_data(user_id):
    return mongo.db.users.find_one({'userId': user_id})

# Endpoint to get user embeddings for recommendations
def getembedding(text):
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    return output.pooler_output

def get_user_embeddings(user_id):
    user_data = get_user_data(user_id)
    
    if not user_data or 'previous_history' not in user_data:
        return jsonify({"error": "User not found or no order history"}), 404

    # Retrieve and concatenate product descriptions
    product_descriptions = ""
    for order in user_data['previous_history']:
        for product_id in order['products']:
            product_data = mongo.db.products.find_one({'productid': product_id})
            if product_data and 'product_name' in product_data:
                product_descriptions += product_data['product_name'] + " "

    if not product_descriptions:
        return jsonify({"error": "No product descriptions found"}), 404

    # Tokenize and encode the concatenated descriptions using BERT
    # inputs = tokenizer(product_descriptions, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    # with torch.no_grad():
    #     outputs = model(**inputs)

    # Get the embedding (usually using the [CLS] token's embedding, which is the first token)
    # user_embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
    user_embedding = getembedding(product_descriptions)

    return jsonify({"user_embedding": user_embedding}), 200

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
        category_name = category.get('name')
        category_embedding = category.get('avg_embedding')
        if category_name and category_embedding:
            category_embeddings[category_name] = category_embedding

    return category_embeddings

@app.route('/get_recommendation/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    user_embedding = get_user_embeddings(user_id)
    category_embedding = get_category_embedding()
    category_similarity = {}
    for ch in category_embedding:
        category_similarity[ch] = cosine_similarity(user_embedding,category_embedding[ch])[0][0]

    sorted_dict = dict(sorted(category_similarity.items(), key=lambda item: item[1], reverse=True))

    
    i=0
    ls = []
    for item in sorted_dict:
        ls.append(item[0])
        i+=1
        if (i==5):
            break
    
    alpha_beta_similarity = {}
    for category in ls:
        rewards_data = mongo.db.rewards.find_one({"user_id": user_id}, {f"{category}": 1})
        alpha = rewards_data[category][0]
        beta = rewards_data[category][1]
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

@app.route('/add_to_cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
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
    print("enetered_dude remove!!")

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
            if item['quantity'] > 1:
                mongo.db.users.update_one(
                    {'_id': ObjectId(user_id), 'cart.product_id': product_id},
                    {'$inc': {'cart.$.quantity': -1}}
                )
            else:
                mongo.db.users.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$pull': {'cart': {'product_id': product_id}}}
                )
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