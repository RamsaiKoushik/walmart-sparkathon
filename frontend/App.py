import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f7f7f7;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
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
        color: #000;
        font-size: 18px;
        margin: 0;
    }
    .product-card p {
        color: #000;
        font-size: 14px;
    }
    .stars img {
        width: 20px;
        height: 20px;
        margin-right: 2px;
    }
    .product-details {
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-left: 20px; /* Add margin to move content to the right */
    }
    .product-details h1, .product-details h2, .product-details h3, .product-details h4, .product-details h5, .product-details h6, .product-details p {
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# Sample product data
products = [
    {
        "name": "Samsung 55\" 4K UHD TV",
        "image_url": "https://via.placeholder.com/150",
        "price": "$349.99",
        "description": "Experience stunning picture quality with the Samsung 55\" 4K UHD TV, featuring dynamic crystal color and a sleek design.",
        "rating": 4,
        "category": "Electronics",
        "subcategory": "Television"
    },
    {
        "name": "Apple iPhone 12",
        "image_url": "https://th.bing.com/th/id/OIP.0H_GXDBmj8t95s1KzMU5GAHaL5?w=124&h=199&c=7&r=0&o=5&dpr=1.5&pid=1.7",
        "price": "$799.99",
        "description": "iPhone 12 features 5G speed, A14 Bionic chip, and a Super Retina XDR display for an unmatched mobile experience.",
        "rating": 5,
        "category": "Electronics",
        "subcategory": "Smartphones"
    },
    {
        "name": "Sony WH-1000XM4 Headphones",
        "image_url": "https://via.placeholder.com/150",
        "price": "$299.99",
        "description": "Sony WH-1000XM4 headphones provide industry-leading noise cancellation, premium sound quality, and all-day comfort.",
        "rating": 4,
        "category": "Electronics",
        "subcategory": "Headphones"
    },
    {
        "name": "Nintendo Switch",
        "image_url": "https://via.placeholder.com/150",
        "price": "$299.99",
        "description": "Enjoy gaming on the go with the Nintendo Switch, featuring a versatile design that lets you play at home or on the move.",
        "rating": 4,
        "category": "Gaming",
        "subcategory": "Consoles"
    }
]

# Handle query parameters to check if a specific product is selected
query_params = st.experimental_get_query_params()
selected_product = query_params.get("product", None)

if selected_product:
    # Display product details page
    product = next((p for p in products if p["name"] == selected_product[0]), None)
    if product:
        # Use columns with adjusted width to move details further to the right
        col1, col2 = st.columns([1, 3])  # Adjust the column ratio as needed
        
        with col1:
            st.image(product['image_url'], width=300)
        
        with col2:
            st.markdown(f"""
                <div class="product-details">
                    <h1>{product['name']}</h1>
                    <div class='stars'>{''.join(['<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Plain_Yellow_Star.png/1024px-Plain_Yellow_Star.png" alt="star" />' for _ in range(product['rating'])])}</div>
                    <h2>Category: {product['category']}</h2>
                    <h3>Subcategory: {product['subcategory']}</h3>
                    <p>{product['description']}</p>
                    <h2>{product['price']}</h2>
                </div>
            """, unsafe_allow_html=True)

            # "Buy Now" and "Add to Cart" buttons
            col1b, col2b = st.columns(2)
            with col1b:
                st.button('Buy Now', key=f'buy_{product["name"]}')
            with col2b:
                st.button('Add to Cart', key=f'cart_{product["name"]}')
else:
    # Display product listing
    st.title("Recommended Products")

    # Adjust number of columns to display more products per row
    cols = st.columns(4)  # Adjust the number of columns to show more products per row

    for index, product in enumerate(products):
        with cols[index % len(cols)]:
            st.markdown(f"""
                <div class="product-card">
                    <a href="/?product={product['name']}">
                        <img src="{product['image_url']}" alt="{product['name']}" />
                        <h3>{product['name']}</h3>
                        <p>{product['price']}</p>
                    </a>
                </div>
            """, unsafe_allow_html=True)
            st.button('Add to Cart', key=f'button_{index}')