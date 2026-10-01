class ApiService {
  static const bool mockMode = true;

  Future<Map<String, dynamic>> login({
    required String identifier,
    required String password,
  }) async {
    await Future.delayed(const Duration(milliseconds: 600));

    if (!mockMode) {
      throw UnimplementedError('Real authentication is not enabled in Sprint 1');
    }

    final normalizedIdentifier = identifier.trim();
    final normalizedPassword = password.trim();

    if (normalizedIdentifier.isEmpty || normalizedPassword.isEmpty) {
      throw const FormatException('Please enter valid credentials.');
    }

    final isValidMockLogin =
        normalizedIdentifier.toLowerCase() == 'citizen@example.com' ||
            normalizedIdentifier == '9999999999' ||
            normalizedIdentifier.length >= 4;

    if (!isValidMockLogin || normalizedPassword.length < 3) {
      throw const FormatException('Invalid mock login credentials.');
    }

    return {
      'access_token': 'mock-access-token-${DateTime.now().millisecondsSinceEpoch}',
      'token_type': 'bearer',
    };
  }

  Future<Map<String, dynamic>> createReport({
    required String description,
    required double latitude,
    required double longitude,
    String? category,
    String? evidence,
  }) async {
    await Future.delayed(const Duration(milliseconds: 700));

    if (!mockMode) {
      throw UnimplementedError('Real report API is not enabled in Sprint 1');
    }

    if (description.trim().isEmpty) {
      throw const FormatException('Description is required.');
    }

    final reportId = 'REP-${DateTime.now().millisecondsSinceEpoch % 100000}';

    return {
      'report_id': reportId,
      'status': 'SUBMITTED',
      'description': description,
      'latitude': latitude,
      'longitude': longitude,
      'category': category ?? 'Other',
      'evidence': evidence ?? 'Mock evidence placeholder',
      'created_at': DateTime.now().toIso8601String(),
    };
  }

  Future<Map<String, dynamic>> getReports() async {
    await Future.delayed(const Duration(milliseconds: 300));

    if (!mockMode) {
      throw UnimplementedError('Real reports API is not enabled in Sprint 1');
    }

    final reports = [
      {
        'report_id': 'REP-001',
        'description': 'No Helmet',
        'latitude': 17.65,
        'longitude': 75.9,
        'status': 'Under Review',
        'created_at': '2026-10-01T09:00:00.000Z',
      },
      {
        'report_id': 'REP-002',
        'description': 'Red Light Violation',
        'latitude': 17.66,
        'longitude': 75.91,
        'status': 'Resolved',
        'created_at': '2026-09-28T08:45:00.000Z',
      },
    ];

    return {
      'items': reports,
      'total': reports.length,
    };
  }

  Future<Map<String, dynamic>> getReport(String reportId) async {
    await Future.delayed(const Duration(milliseconds: 250));

    if (!mockMode) {
      throw UnimplementedError('Real report detail API is not enabled in Sprint 1');
    }

    final reports = await getReports();
    final items = List<Map<String, dynamic>>.from(reports['items'] as List);
    final match = items.firstWhere(
      (report) => report['report_id'] == reportId,
      orElse: () => {
        'report_id': reportId,
        'description': 'Mock report details',
        'latitude': 17.65,
        'longitude': 75.9,
        'status': 'Submitted',
        'created_at': DateTime.now().toIso8601String(),
      },
    );

    return match;
  }
}
