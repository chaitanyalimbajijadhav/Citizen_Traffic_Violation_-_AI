// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:citizen_app/main.dart';
import 'package:citizen_app/screens/home_screen.dart';
import 'package:citizen_app/screens/login_screen.dart';
import 'package:citizen_app/screens/report_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('App launches and login screen appears', (WidgetTester tester) async {
    await tester.pumpWidget(const CitizenApp());

    expect(find.byType(LoginScreen), findsOneWidget);
    expect(find.text('Citizen Traffic Report'), findsOneWidget);
  });

  testWidgets('Empty login validation works', (WidgetTester tester) async {
    await tester.pumpWidget(const CitizenApp());

    await tester.tap(find.text('Login'));
    await tester.pump();

    expect(find.text('Please enter mobile number or email'), findsOneWidget);
    expect(find.text('Please enter password'), findsOneWidget);
  });

  testWidgets('Login with mock credentials navigates to Home', (WidgetTester tester) async {
    await tester.pumpWidget(const CitizenApp());

    await tester.enterText(find.byType(TextFormField).at(0), 'citizen@example.com');
    await tester.enterText(find.byType(TextFormField).at(1), '123456');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();

    expect(find.byType(HomeScreen), findsOneWidget);
    expect(find.text('Welcome,'), findsOneWidget);
  });

  testWidgets('Home screen to report navigation works', (WidgetTester tester) async {
    await tester.pumpWidget(const CitizenApp());

    await tester.enterText(find.byType(TextFormField).at(0), 'citizen@example.com');
    await tester.enterText(find.byType(TextFormField).at(1), '123456');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Report Violation'));
    await tester.pumpAndSettle();

    expect(find.byType(ReportScreen), findsOneWidget);
    expect(find.text('Violation Details'), findsOneWidget);
  });
}
