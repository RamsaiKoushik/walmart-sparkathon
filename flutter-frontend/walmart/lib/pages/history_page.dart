import 'package:flutter/material.dart';

class HistoryPage extends StatelessWidget {
  // Example order data
  final List<Map<String, dynamic>> orders = [
    {
      'orderId': 'ORD123',
      'date': DateTime.now().subtract(Duration(days: 1)),
      'products': [
        {
          'name': 'Product 1',
          'price': 30,
          'imageUrl': 'https://example.com/order-product-1.jpg'
        },
        {
          'name': 'Product 2',
          'price': 20,
          'imageUrl': 'https://example.com/order-product-2.jpg'
        },
      ],
    },
    {
      'orderId': 'ORD122',
      'date': DateTime.now().subtract(Duration(days: 5)),
      'products': [
        {
          'name': 'Product 3',
          'price': 50,
          'imageUrl': 'https://example.com/order-product-3.jpg'
        },
      ],
    },
    {
      'orderId': 'ORD121',
      'date': DateTime.now().subtract(Duration(days: 10)),
      'products': [
        {
          'name': 'Product 4',
          'price': 25,
          'imageUrl': 'https://example.com/order-product-4.jpg'
        },
        {
          'name': 'Product 5',
          'price': 15,
          'imageUrl': 'https://example.com/order-product-5.jpg'
        },
      ],
    },
  ];

  @override
  Widget build(BuildContext context) {
    // Sort orders by date in descending order
    orders.sort((a, b) => b['date'].compareTo(a['date']));

    return Scaffold(
      appBar: AppBar(
        title: Text('Orders'),
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
        child: ListView.builder(
          itemCount: orders.length,
          itemBuilder: (ctx, i) {
            final order = orders[i];
            return Card(
              margin: EdgeInsets.symmetric(vertical: 10),
              elevation: 5,
              child: Padding(
                padding: const EdgeInsets.all(15.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Order ID: ${order['orderId']}',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 10),
                    ...order['products'].map<Widget>((product) {
                      return ListTile(
                        leading: Image.network(product['imageUrl']),
                        title: Text(product['name']),
                        subtitle: Text('Purchased on: ${order['date']}'),
                        trailing: Text('\$${product['price']}',
                            style: TextStyle(fontWeight: FontWeight.bold)),
                      );
                    }).toList(),
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
