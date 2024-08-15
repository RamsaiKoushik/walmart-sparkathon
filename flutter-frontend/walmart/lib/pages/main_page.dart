import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:walmart/pages/detailed_page.dart';
import 'dart:convert';
import 'cart_page.dart';
import 'history_page.dart';
import 'auth_page.dart';

class MainPage extends StatefulWidget {
  final String userId;

  MainPage({required this.userId});

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  List<dynamic> _products = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchProducts();
  }

  Future<void> _fetchProducts() async {
    final url = 'http://127.0.0.1:5000/get_all_products';

    try {
      final response = await http.get(Uri.parse(url));
      final responseData = json.decode(response.body);

      if (response.statusCode == 200) {
        setState(() {
          _products = responseData;
          _isLoading = false;
        });
      } else {
        throw Exception('Failed to load products');
      }
    } catch (error) {
      setState(() {
        _isLoading = false;
      });
      print(error);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Failed to load products: $error'),
      ));
    }
  }

  // Future<void> _fetchProducts() async {
  //   final url = 'http://127.0.0.1:5000/get_recommendation/${widget.userId}';

  //   try {
  //     final response = await http.get(Uri.parse(url));
  //     final responseData = json.decode(response.body);

  //     if (response.statusCode == 200) {
  //       setState(() {
  //         _products = responseData;
  //         _isLoading = false;
  //       });
  //     } else {
  //       throw Exception('Failed to load products');
  //     }
  //   } catch (error) {
  //     setState(() {
  //       _isLoading = false;
  //     });
  //     print(error);
  //     ScaffoldMessenger.of(context).showSnackBar(SnackBar(
  //       content: Text('Failed to load products: $error'),
  //     ));
  //   }
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 20, 136, 213),
        title: Text('All Products'),
        actions: [
          IconButton(
            icon: Icon(Icons.shopping_cart),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => CartPage(userId: widget.userId),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.receipt),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => HistoryPage(userId: widget.userId),
                ),
              );
            },
          ),
          ProfileIcon(userId: widget.userId),
        ],
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : ListView(
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
        itemCount: _products.length,
        itemBuilder: (context, index) {
          final product = _products[index];
          final productId = product['_id']; // Use the MongoDB product ID
          final actualPrice = product['actual_price'];
          final discountPrice = product['discount_price'];

          return GestureDetector(
            onTap: () async {
              // Make API call to track product view
              await _trackProductView(widget.userId, productId);

              // Navigate to product details page
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ProductDetailPage(productId: productId),
                ),
              );
            },
            child: Container(
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
                        fit: BoxFit.contain,
                        width: double.infinity,
                        height: 120, // Fixed height for the image
                        errorBuilder: (context, error, stackTrace) {
                          return Image.asset(
                            'assets/default_image2.png',
                            fit: BoxFit.contain,
                            width: double.infinity,
                            height: 120,
                          );
                        },
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(
                        product['name'],
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                            fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 8.0),
                      child: Row(
                        children: [
                          Text(
                            actualPrice,
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey,
                              decoration: TextDecoration.lineThrough,
                            ),
                          ),
                          SizedBox(width: 8),
                          Text(
                            discountPrice,
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.red,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Center(
                        child: ElevatedButton(
                          onPressed: () => _addToCart(context, productId),
                          child: Text('Add to Cart'),
                        ),
                      ),
                    )
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Future<void> _trackProductView(String userId, String productId) async {
    final url = 'http://127.0.0.1:5000/update_rewards/$userId/$productId';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'delta': 0.6}), // Convert body to JSON string
      );

      print('Status Code: ${response.statusCode}');
      print('Response Body: ${response.body}');

      if (response.statusCode == 200) {
        // Success
        print('Rewards updated successfully');
      } else {
        // Handle error
        print('Failed to update rewards: ${response.statusCode}');
      }
    } catch (e) {
      // Handle exceptions
      print('Error during HTTP request: $e');
    }
  }

  Future<void> _addToCart(BuildContext context, String productId) async {
    final url =
        'http://127.0.0.1:5000/add_to_cart/${widget.userId}'; // Replace with your backend URL
    print(widget.userId);
    print(widget.userId.toString());
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'product_id': productId}),
      );

      final responseData = json.decode(response.body);

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(responseData['message'] ?? 'Product added to cart'),
        ));
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
}

class ProfileIcon extends StatelessWidget {
  final String userId;

  ProfileIcon({required this.userId});

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<String>(
      onSelected: (value) {
        if (value == 'logout') {
          _logout(context);
        }
      },
      itemBuilder: (BuildContext context) => [
        PopupMenuItem<String>(
          value: 'username',
          child: Text('Username: $userId'),
        ),
        PopupMenuItem<String>(
          value: 'logout',
          child: Text('Logout'),
        ),
      ],
      icon: Icon(Icons.person),
    );
  }

  void _logout(BuildContext context) {
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (context) => AuthPage()),
      (Route<dynamic> route) => false,
    );
  }
}
