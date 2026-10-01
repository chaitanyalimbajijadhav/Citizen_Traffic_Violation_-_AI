# Citizen Traffic Violation App

## Project name
Citizen Traffic Violation Reporting App

## Purpose
This Flutter application is the citizen-facing mobile frontend for the AI-based smart traffic violation reporting system. It provides a lightweight foundation for Sprint 1, including login, home dashboard, report shell, navigation, API abstraction, and mock-mode behavior.

## Flutter / Dart
- Flutter SDK: latest stable
- Dart SDK: included with Flutter

## Install dependencies
```bash
flutter pub get
```

## Run app
```bash
flutter run
```

## Run tests
```bash
flutter test
```

## Analyze code
```bash
flutter analyze
```

## Build debug APK
```bash
flutter build apk --debug
```

## Sprint 1 implemented features
- Login screen with validation and password visibility toggle
- Mock login flow
- Home/dashboard screen with welcome area and recent reports
- Report screen shell with violation category and required fields
- Login → Home → Report navigation using named routes
- API service abstraction with mock mode
- Basic widget tests for app launch, validation, and navigation
- Clean traffic-safety visual identity consistent with the provided UI direction

## Mock API mode
This app intentionally uses a mock API mode in Sprint 1 so UI development does not depend on the backend being available.

Mock login example:
- Email / mobile: citizen@example.com
- Password: 123456

The mock layer is kept separate from the real API structure and is designed to be replaced in later sprints by a FastAPI-backed service.

## Known limitations
- No real authentication backend yet
- No JWT persistence
- No camera or gallery upload integration
- No GPS implementation
- No AI/OCR or rule-engine integration
- No real notifications or reporting backend

## Future Sprint features
- Real FastAPI authentication
- JWT storage and protected routes
- Evidence uploads and GPS capture
- Violation AI/OCR integration
- Rule-engine decision support
- Real report tracking and notifications

## Notes
This is a Sprint 1 foundation project and intentionally stays lightweight. It is designed to be easy to extend for future backend integration without adding unnecessary dependencies or complexity.
