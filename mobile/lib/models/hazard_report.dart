import 'dart:io';

class HazardReport {
  final int? id;
  final String title;
  final String description;
  final String hazardType;
  final double latitude;
  final double longitude;
  final String? address;
  final List<String> mediaUrls;
  final List<File>? mediaFiles;
  final DateTime? createdAt;
  final int? upvotes;
  final bool? isVerified;

  HazardReport({
    this.id,
    required this.title,
    required this.description,
    required this.hazardType,
    required this.latitude,
    required this.longitude,
    this.address,
    this.mediaUrls = const [],
    this.mediaFiles,
    this.createdAt,
    this.upvotes,
    this.isVerified,
  });

  factory HazardReport.fromJson(Map<String, dynamic> json) {
    return HazardReport(
      id: json['id'] as int?,
      title: json['title'] ?? 'No Title',
      description: json['description'] ?? '',
      hazardType: json['hazard_type'] ?? 'Other',
      latitude: (json['latitude'] as num?)?.toDouble() ?? 0.0,
      longitude: (json['longitude'] as num?)?.toDouble() ?? 0.0,
      address: json['address'] as String?,
      mediaUrls: (json['media_urls'] as List<dynamic>?)
          ?.map((e) => e.toString()).toList() ?? [],
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
      upvotes: json['upvotes'] as int?,
      isVerified: json['is_verified'] as bool?,
    );
  }
}

enum HazardType {
  flood('flood', '🌊 Flood', 'Water-related hazards'),
  infrastructure('infrastructure', '🌳 Infrastructure', 'Road, building issues'),
  weather('weather', '⛈️ Weather', 'Storm, wind damage'),
  fire('fire', '🔥 Fire', 'Fire incidents'),
  earthquake('earthquake', '🌍 Earthquake', 'Seismic activity'),
  other('other', '⚠️ Other', 'Other hazards');

  const HazardType(this.value, this.displayName, this.description);

  final String value;
  final String displayName;
  final String description;
}

class HazardReportResponse {
  final bool success;
  final String message;
  final int? reportId;
  final double? trustScore;
  final double? estimatedSeverity;

  HazardReportResponse({
    required this.success,
    required this.message,
    this.reportId,
    this.trustScore,
    this.estimatedSeverity,
  });

  factory HazardReportResponse.fromJson(Map<String, dynamic> json) {
    return HazardReportResponse(
      success: json['success'] as bool,
      message: json['message'] as String,
      reportId: json['report_id'] as int?,
      trustScore: (json['trust_score'] as num?)?.toDouble(),
      estimatedSeverity: (json['estimated_severity'] as num?)?.toDouble(),
    );
  }
}
