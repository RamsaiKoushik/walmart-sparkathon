import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:walmart/pages/detailed_page.dart';

class ProductSection extends StatelessWidget {
  final List<dynamic> products;
  final String userId;

  ProductSection({required this.products, required this.userId});

  Future<void> _trackProductView(
      BuildContext context, String userId, String productId) async {
    final url = 'http://127.0.0.1:5000/update_rewards/$userId/$productId';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'delta': 0.6}), // Adjust the payload if needed
      );

      if (response.statusCode == 200) {
        print('Rewards updated successfully');
      } else {
        print('Failed to update rewards: ${response.statusCode}');
      }
    } catch (e) {
      print('Error during HTTP request: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 300,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: products.length,
        itemBuilder: (context, index) {
          final product = products[index];
          final productId = product['_id'];
          final actualPrice = product['actual_price'];
          final discountPrice = product['discount_price'];

          return GestureDetector(
            onTap: () async {
              // Make API call to track product view
              await _trackProductView(context, userId, productId);

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
                        height: 120,
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
                          onPressed: () =>
                              _addToCart(context, productId, userId),
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

  Future<void> _addToCart(
      BuildContext context, String productId, String userId) async {
    final url =
        'http://127.0.0.1:5000/add_to_cart/${userId}'; // Replace with your backend URL

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
