import 'package:flutter/material.dart';

class HistoryPage extends StatelessWidget {
  final String userId;

  HistoryPage({required this.userId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Your Orders'),
      ),
      body: ListView.builder(
        itemCount: 5, // Placeholder for number of orders
        itemBuilder: (context, orderIndex) {
          return Card(
            elevation: 5,
            margin: EdgeInsets.all(10),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    'Order ID: ${orderIndex + 1001}',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
                Divider(),
                Column(
                  children: List.generate(3, (productIndex) {
                    return ListTile(
                      leading: Icon(Icons.shopping_bag),
                      title: Text('Product ${productIndex + 1}'),
                      subtitle: Text('\$${(productIndex + 1) * 30}'),
                    );
                  }),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
