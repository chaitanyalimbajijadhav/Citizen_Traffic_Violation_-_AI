import 'package:flutter_test/flutter_test.dart';
import 'package:citizen_app/main.dart';

void main() {
  testWidgets(
    'Citizen app loads login screen',
    (WidgetTester tester) async {
      await tester.pumpWidget(
        const SmartTrafficApp(),
      );

      expect(
        find.text('Smart Traffic Citizen'),
        findsOneWidget,
      );

      expect(
        find.text('Citizen Login'),
        findsOneWidget,
      );

      expect(
        find.text('Email Address'),
        findsOneWidget,
      );

      expect(
        find.text('Password'),
        findsOneWidget,
      );

      expect(
        find.text('Login'),
        findsOneWidget,
      );
    },
  );
}