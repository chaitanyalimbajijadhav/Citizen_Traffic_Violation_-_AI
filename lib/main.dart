import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const TrafficViolationApp());
}

class TrafficViolationApp extends StatelessWidget {
  const TrafficViolationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Traffic Violation Reporting',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
        ),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}