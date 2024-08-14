import 'package:flutter/material.dart';

class CartPage extends StatelessWidget {
  final String userId;

  CartPage({required this.userId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Your Cart'),
      ),
      body: ListView(
        children: [
          buildSectionTitle('Cart Items'),
          buildCartItems(),
          buildSectionTitle('You May Also Like'),
          buildRecommendations(),
        ],
      ),
    );
  }

  Widget buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Text(
        title,
        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget buildCartItems() {
    return Column(
      children: List.generate(3, (index) {
        return ListTile(
          leading: Icon(Icons.shopping_cart),
          title: Text('Cart Item $index'),
          subtitle: Text('\$${(index + 1) * 20}'),
        );
      }),
    );
  }

  Widget buildRecommendations() {
    return SizedBox(
      height: 300,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: 10, // Placeholder for number of recommendations
        itemBuilder: (context, index) {
          return Container(
            width: 200,
            margin: EdgeInsets.all(10),
            child: Card(
              elevation: 5,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Image.network(
                      'https://m.media-amazon.com/images/I/61UUaPVRTbL._AC_UL320_.jpg', // Example product image URL
                      fit: BoxFit.contain,
                      width: double.infinity,
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text('Recommended Product $index'),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8.0),
                    child: Text('\$${(index + 1) * 10}',
                        style: TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
