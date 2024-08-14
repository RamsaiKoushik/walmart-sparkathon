import 'package:flutter/material.dart';
import 'cart_page.dart';
import 'history_page.dart';

class MainPage extends StatelessWidget {
  final String userId;

  MainPage({required this.userId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('All Products'),
        actions: [
          IconButton(
            icon: Icon(Icons.shopping_cart),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => CartPage(userId: userId),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.receipt), // Orders icon
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => HistoryPage(userId: userId),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.person),
            onPressed: () {
              // Navigate to user profile or show user info
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('User ID: $userId')),
              );
            },
          ),
        ],
      ),
      body: ListView(
        children: [
          buildSectionTitle('All Products'),
          buildProductSection(context),
          buildSectionTitle('You May Like'),
          buildProductSection(context),
          buildSectionTitle('Recommended for You'),
          buildProductSection(context),
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

  Widget buildProductSection(BuildContext context) {
    return SizedBox(
      height: 300,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: 10, // Placeholder for number of products
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
                    child: Text('Product $index'),
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
