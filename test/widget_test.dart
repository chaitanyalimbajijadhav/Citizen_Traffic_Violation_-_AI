import 'package:flutter_test/flutter_test.dart';
import 'package:traffic_citizen_app/main.dart';

void main() {
  testWidgets('Traffic Violation App smoke test',
      (WidgetTester tester) async {
    // Build the application.
    await tester.pumpWidget(const TrafficViolationApp());

    // Verify that the login screen is displayed.
    expect(find.text('Citizen Login'), findsOneWidget);
    expect(find.text('Traffic Violation Reporting'), findsOneWidget);
    expect(find.text('LOGIN'), findsOneWidget);
  });
}