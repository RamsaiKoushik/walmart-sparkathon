function viewProduct(productId) {
    // Redirect to product page with product ID
    window.location.href = `product.html?id=${productId}`;
}

window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    if (productId) {
        // Load product details based on productId
        const productTitle = document.getElementById('product-title');
        const productImage = document.getElementById('product-image');
        const productDescription = document.getElementById('product-description');
        const productPrice = document.getElementById('product-price');

        // Example product data
        const products = {
            'product1': {
                title: 'Product 1',
                image: 'images/product1.jpeg',
                description: 'Description for Product 1',
                price: '$29.99'
            },
            'product2': {
                title: 'Product 2',
                image: 'images/product2.jpeg',
                description: 'Description for Product 2',
                price: '$19.99'
            }
        };

        const product = products[productId];
        if (product) {
            productTitle.textContent = product.title;
            productImage.src = product.image;
            productDescription.textContent = product.description;
            productPrice.textContent = product.price;
        }
    }
};
