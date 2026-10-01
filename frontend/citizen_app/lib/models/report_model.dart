class ReportModel {
  final String reportId;
  final String description;
  final double latitude;
  final double longitude;
  final String status;
  final DateTime createdAt;

  const ReportModel({
    required this.reportId,
    required this.description,
    required this.latitude,
    required this.longitude,
    required this.status,
    required this.createdAt,
  });

  factory ReportModel.fromMap(Map<String, dynamic> map) {
    return ReportModel(
      reportId: map['report_id']?.toString() ?? 'UNKNOWN',
      description: map['description']?.toString() ?? '',
      latitude: (map['latitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (map['longitude'] as num?)?.toDouble() ?? 0.0,
      status: map['status']?.toString() ?? 'SUBMITTED',
      createdAt: map['created_at'] != null
          ? DateTime.tryParse(map['created_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
    );
  }
}
