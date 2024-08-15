import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HistoryPage extends StatefulWidget {
  final String userId;

  HistoryPage({required this.userId});

  @override
  _HistoryPageState createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  List<Map<String, dynamic>> _orders = [];

  @override
  void initState() {
    super.initState();
    _fetchPreviousOrders();
  }

  Future<void> _fetchPreviousOrders() async {
    final response = await http.get(Uri.parse(
        'http://127.0.0.1:5000/get_previous_orders/${widget.userId}'));
    if (response.statusCode == 200) {
      setState(() {
        _orders = List<Map<String, dynamic>>.from(json.decode(response.body));
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load previous orders')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Your Orders'),
      ),
      body: ListView.builder(
        itemCount: _orders.length,
        itemBuilder: (context, orderIndex) {
          final order = _orders[orderIndex];
          return Card(
            elevation: 5,
            margin: EdgeInsets.all(10),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Order ID: ${order['order_id']}',
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                      Text(
                        order['date'] ?? 'Date not available',
                        style: TextStyle(fontSize: 16, color: Colors.grey),
                      ),
                    ],
                  ),
                ),
                Divider(),
                Column(
                  children:
                      List.generate(order['items'].length, (productIndex) {
                    final product = order['items'][productIndex];
                    return ListTile(
                      leading: Image.network(
                        product['image'],
                        fit: BoxFit.contain,
                        width: 50,
                        height: 50,
                        errorBuilder: (context, error, stackTrace) {
                          return Image.asset(
                            'assets/default_image2.png',
                            fit: BoxFit.cover,
                            width: 50,
                            height: 50,
                          );
                        },
                      ),
                      title: Text(product['name']),
                      subtitle: Text('Quantity: ${product['quantity']}'),
                      trailing: Text('\$${product['price']}'),
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
