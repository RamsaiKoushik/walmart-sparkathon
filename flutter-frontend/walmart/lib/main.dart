import 'package:flutter/material.dart';
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
      home: MainPage(), // Set MainPage as the default home screen
      routes: {
        '/cart': (context) => CartPage(),
        '/history': (context) => HistoryPage(),
      },
    );
  }
}
