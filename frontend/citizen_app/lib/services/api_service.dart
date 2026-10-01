class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';

  Future<void> login(
    String email,
    String password,
  ) async {
    // FastAPI login integration will be implemented in a later sprint.
  }

  Future<void> createReport(
    Map<String, dynamic> reportData,
  ) async {
    // Report API integration will be implemented in a later sprint.
  }
}