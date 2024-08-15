import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CartPage extends StatefulWidget {
  final String userId;

  CartPage({required this.userId});

  @override
  _CartPageState createState() => _CartPageState();
}

class _CartPageState extends State<CartPage> {
  List<Map<String, dynamic>> _cartItems = [];
  List<Map<String, dynamic>> _recommendations = [];

  @override
  void initState() {
    super.initState();
    _fetchCartItems();
    _fetchRecommendations();
  }

  Future<void> _fetchCartItems() async {
    final response = await http
        .get(Uri.parse('http://127.0.0.1:5000/get_cart/${widget.userId}'));
    if (response.statusCode == 200) {
      setState(() {
        _cartItems =
            List<Map<String, dynamic>>.from(json.decode(response.body));
      });
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Failed to load cart items')));
    }
  }

  Future<void> _fetchRecommendations() async {
    // final response = await http.get(
    // Uri.parse('http://127.0.0.1:5000/get_all_products/${widget.userId}'));

    //to be replaced with recommendations api
    final url = 'http://127.0.0.1:5000/get_all_products';
    final response = await http.get(Uri.parse(url));

    // print(response.statusCode);
    // print(response.body);
    if (response.statusCode == 200) {
      setState(() {
        _recommendations =
            List<Map<String, dynamic>>.from(json.decode(response.body));
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load recommendations')));
    }
  }

  Future<void> _addToCart(String productId) async {
    final url =
        'http://127.0.0.1:5000/add_to_cart/${widget.userId}'; // Replace with your backend URL
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'product_id': productId}),
      );

      final responseData = json.decode(response.body);

      if (response.statusCode == 200) {
        _fetchCartItems();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content:
              Text(responseData['error'] ?? 'Failed to add product to cart'),
        ));
      }
    } catch (error) {
      print('Error adding product to cart: $error');
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Something went wrong. Please try again later.'),
      ));
    }
  }

  Future<void> _removeFromCart(String productId) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/remove_from_cart/${widget.userId}'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'product_id': productId}),
    );

    if (response.statusCode == 200) {
      _fetchCartItems(); // Refresh cart items
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to remove item from cart')));
    }
  }

  Future<void> _purchase() async {
    final url = 'http://127.0.0.1:5000/checkout/${widget.userId}';
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
      );

      final responseData = json.decode(response.body);

      if (response.statusCode == 200) {
        // Clear cart items
        setState(() {
          _cartItems = [];
        });
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Purchase successful!'),
        ));
        _fetchCartItems(); // Refresh cart items
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(responseData['error'] ?? 'Failed to complete purchase'),
        ));
      }
    } catch (error) {
      print('Error completing purchase: $error');
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Something went wrong. Please try again later.'),
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Your Cart'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Cart Items',
                  style: Theme.of(context).textTheme.headline6,
                ),
                ElevatedButton(
                  onPressed: _purchase,
                  child: Text('Purchase'),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              children: [
                buildCartItems(),
                buildSectionTitle('You May Also Like'),
                buildRecommendations(),
              ],
            ),
          ),
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
    return _cartItems.isEmpty
        ? Center(child: Text('Your cart is empty'))
        : Column(
            children: _cartItems.map((item) {
              return ListTile(
                leading: Image.network(
                  item['image'],
                  fit: BoxFit.cover,
                  width: 50,
                  height: 50,
                ),
                title: Text(item['name']),
                subtitle: Text('Quantity: ${item['quantity']}'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      icon: Icon(Icons.remove),
                      onPressed: () {
                        _removeFromCart(item['_id']);
                      },
                    ),
                    Text('${item['quantity']}'),
                    IconButton(
                      icon: Icon(Icons.add),
                      onPressed: () {
                        _addToCart(item['_id']);
                      },
                    ),
                  ],
                ),
              );
            }).toList(),
          );
  }

  Widget buildRecommendations() {
    return SizedBox(
      height: 300,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: _recommendations.length,
        itemBuilder: (context, index) {
          final product = _recommendations[index];
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
                      product['image'],
                      fit: BoxFit.cover,
                      width: double.infinity,
                      errorBuilder: (context, error, stackTrace) {
                        return Image.asset(
                          'assets/default_image2.png',
                          fit: BoxFit.cover,
                          width: double.infinity,
                        );
                      },
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      product['name'],
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8.0),
                    child: Text(
                      product['discount_price'],
                      style:
                          TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8.0),
                    child: Text(
                      product['actual_price'],
                      style: TextStyle(
                        color: Colors.grey,
                        decoration: TextDecoration.lineThrough,
                      ),
                    ),
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
