import 'package:flutter/material.dart';

class MainPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('All Products'),
        actions: [
          IconButton(
            icon: Icon(Icons.shopping_cart),
            onPressed: () {
              Navigator.pushNamed(context, '/cart');
            },
          ),
          IconButton(
            icon: Icon(Icons.receipt), // Orders icon
            onPressed: () {
              Navigator.pushNamed(
                  context, '/history'); // Navigate to Orders page
            },
          ),
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
        child: LayoutBuilder(
          builder: (context, constraints) {
            int crossAxisCount = (constraints.maxWidth > 1200)
                ? 4
                : (constraints.maxWidth > 800)
                    ? 3
                    : 2;
            return GridView.builder(
              itemCount: 20, // Placeholder for number of products
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: crossAxisCount,
                childAspectRatio: 3 / 4,
                crossAxisSpacing: 20,
                mainAxisSpacing: 20,
              ),
              itemBuilder: (ctx, i) => Card(
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
                      child: Text('Product $i'),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8.0),
                      child: Text('\$${(i + 1) * 10}',
                          style: TextStyle(fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
