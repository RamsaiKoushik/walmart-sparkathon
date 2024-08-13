import 'package:flutter/material.dart';

class CartPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Your Cart'),
        actions: [
          IconButton(
            icon: Icon(Icons.person),
            onPressed: () {
              // Navigate to user profile or show user info
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                itemCount: 5, // Placeholder for the number of cart items
                itemBuilder: (ctx, i) => ListTile(
                  leading:
                      Image.network('https://example.com/cart-product-$i.jpg'),
                  title: Text('Cart Product $i'),
                  subtitle: Text('\$${(i + 1) * 20}'),
                  trailing: IconButton(
                    icon: Icon(Icons.remove_shopping_cart),
                    onPressed: () {
                      // Handle remove from cart
                    },
                  ),
                ),
              ),
            ),
            Divider(),
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: Text(
                'You may also like',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
            Expanded(
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: 5, // Placeholder for the number of recommendations
                itemBuilder: (ctx, i) => Container(
                  width: 200,
                  margin: EdgeInsets.symmetric(horizontal: 10),
                  child: Card(
                    elevation: 3,
                    child: Column(
                      children: [
                        Expanded(
                          child: Image.network(
                              'https://example.com/recommended-product-$i.jpg',
                              fit: BoxFit.cover),
                        ),
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Text('Recommended $i'),
                        ),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 8.0),
                          child: Text('\$${(i + 1) * 15}',
                              style: TextStyle(fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
