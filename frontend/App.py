import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f7f7f7;
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #0071dc;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        margin-top: 10px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #005bb5;
    }
    .product-card {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .product-card img {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .product-card h3 {
        color: #333;
        font-size: 18px;
        margin: 0;
    }
    .product-card p {
        color: #666;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Sample product data
products = [
    {
        "name": "Samsung 55\" 4K UHD TV",
        "image_url": "https://via.placeholder.com/150",
        "price": "$349.99"
    },
    {
        "name": "Apple iPhone 12",
        "image_url": "https://via.placeholder.com/150",
        "price": "$799.99"
    },
    {
        "name": "Sony WH-1000XM4 Headphones",
        "image_url": "https://via.placeholder.com/150",
        "price": "$299.99"
    },
    {
        "name": "Nintendo Switch",
        "image_url": "https://via.placeholder.com/150",
        "price": "$299.99"
    }
]

# Streamlit app
st.title("Recommended Products")

# Display products in a grid
cols = st.columns(2)  # Adjust the number of columns as needed

for index, product in enumerate(products):
    with cols[index % len(cols)]:
        st.markdown(f"""
            <div class="product-card">
                <img src="{product['image_url']}" alt="{product['name']}" />
                <h3>{product['name']}</h3>
                <p>{product['price']}</p>
            </div>
        """, unsafe_allow_html=True)
        st.button('Add to Cart', key=f'button_{index}')
