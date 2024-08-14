import 'package:flutter/material.dart';
import 'pages/auth_page.dart';
import 'pages/main_page.dart';
import 'pages/cart_page.dart';
import 'pages/history_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Walmart Hackathon',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: AuthPage(), // Start with the AuthPage
    );
  }
}
