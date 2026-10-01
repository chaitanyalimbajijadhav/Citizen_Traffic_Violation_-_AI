import 'package:flutter/material.dart';

class MyReportsScreen extends StatelessWidget {
  const MyReportsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Reports'),
      ),
      body: const Center(
        child: Text(
          'My Reports\nComing in next implementation.',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}