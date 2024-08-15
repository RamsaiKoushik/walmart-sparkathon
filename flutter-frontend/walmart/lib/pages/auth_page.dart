import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:walmart/pages/main_page.dart';

class AuthPage extends StatefulWidget {
  @override
  _AuthPageState createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  final _formKey = GlobalKey<FormState>();
  bool _isLogin = true; // Toggle between login and signup
  String _email = '';
  String _password = '';
  String _username = ''; // Only for signup

  Future<void> _authenticate() async {
    final url = _isLogin
        ? 'http://127.0.0.1:5000/login'
        : 'http://127.0.0.1:5000/register';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': _email,
          'password': _password,
          if (!_isLogin) 'username': _username,
        }),
      );
      // print(response.toString());
      // print(response.statusCode);
      // print(response.body.toString());

      if (response.statusCode == 200 || response.statusCode == 201) {
        final responseData = json.decode(response.body);
        if (_isLogin) {
          // Navigate to the main page after successful login
          // ignore: use_build_context_synchronously

          Navigator.of(context).push(MaterialPageRoute(
            builder: (context) => MainPage(userId: responseData['user_id']),
          ));
        } else {
          // Show success message after successful signup
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text('Signup successful! Please log in.'),
          ));
          setState(() {
            _isLogin = true;
          });
        }
      } else {
        // Show error message
        final responseData = json.decode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(responseData['message'] ?? 'Authentication failed!'),
        ));
      }
    } catch (error) {
      print('Error during authentication: $error');
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Something went wrong. Please try again later.'),
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(_isLogin ? 'Login' : 'Sign Up')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              if (!_isLogin)
                TextFormField(
                  key: ValueKey('username'),
                  decoration: InputDecoration(labelText: 'Username'),
                  onChanged: (value) {
                    _username = value;
                  },
                  validator: (value) {
                    if (value!.isEmpty || value.length < 4) {
                      return 'Please enter at least 4 characters';
                    }
                    return null;
                  },
                ),
              TextFormField(
                key: ValueKey('email'),
                decoration: InputDecoration(labelText: 'Email'),
                keyboardType: TextInputType.emailAddress,
                onChanged: (value) {
                  _email = value;
                },
                validator: (value) {
                  if (value!.isEmpty) {
                    return 'Please enter a valid email address';
                  }
                  return null;
                },
              ),
              TextFormField(
                key: ValueKey('password'),
                decoration: InputDecoration(labelText: 'Password'),
                obscureText: true,
                onChanged: (value) {
                  _password = value;
                },
                validator: (value) {
                  if (value!.isEmpty || value.length < 6) {
                    return 'Password must be at least 6 characters long';
                  }
                  return null;
                },
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _authenticate();
                  }
                },
                child: Text(_isLogin ? 'Login' : 'Sign Up'),
              ),
              TextButton(
                onPressed: () {
                  setState(() {
                    _isLogin = !_isLogin;
                  });
                },
                child: Text(_isLogin
                    ? 'Create new account'
                    : 'Already have an account? Login'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
