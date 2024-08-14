from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from MLModel import MultiArmedBandit
from sklearn.metrics.pairwise import cosine_similarity
from bson.objectid import ObjectId
from transformers import BertTokenizer, BertModel
import torch

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/yourdbname"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

mab = MultiArmedBandit()
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
        "password": hashed_password
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
        category_similarity[ch] = cosine_similarity(user_embedding,category_embedding[ch])
    
    

# Endpoint to get product data
@app.route('/get_product_data/<product_id>', methods=['GET'])
def get_product_data(product_id):
    product_data = mongo.db.products.find_one({'productid': product_id})
    if product_data:
        return jsonify(serialize_doc(product_data))
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint to get all products in a user's cart
@app.route('/get_cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    user_data = mongo.db.users.find_one({'userId': user_id})
    if user_data and 'cart' in user_data:
        cart_products = []
        for product_id in user_data['cart']:
            product = mongo.db.products.find_one({'productid': product_id})
            if product:
                cart_products.append(serialize_doc(product))
        return jsonify(cart_products)
    else:
        return jsonify({"error": "User not found or cart is empty"}), 404

# Endpoint to get previous order history
@app.route('/get_order_history/<user_id>', methods=['GET'])
def get_order_history(user_id):
    user_data = mongo.db.users.find_one({'userId': user_id})
    if user_data and 'previous_history' in user_data:
        detailed_order_history = []
        for order in user_data['previous_history']:
            detailed_order = {
                "order_id": order.get('order_id'),
                "date_of_purchase": order.get('date_of_purchase'),
                "products": []
            }
            for product_id in order.get('products', []):
                product = mongo.db.products.find_one({'productid': product_id})
                if product:
                    detailed_order['products'].append(serialize_doc(product))
            detailed_order_history.append(detailed_order)
        return jsonify(detailed_order_history)
    else:
        return jsonify({"error": "User not found or no order history"}), 404


if __name__ == '__main__':
    app.run(debug=True)
