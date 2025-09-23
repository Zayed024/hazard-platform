import 'dart:io';

class HazardReport {
  final String title;
  final String description;
  final String hazardType;
  final double latitude;
  final double longitude;
  final String? address;
  final List<String> mediaUrls;
  final List<File>? mediaFiles;
  final DateTime timestamp;

  HazardReport({
    required this.title,
    required this.description,
    required this.hazardType,
    required this.latitude,
    required this.longitude,
    this.address,
    this.mediaUrls = const [],
    this.mediaFiles,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'description': description,
      'hazard_type': hazardType,
      'latitude': latitude,
      'longitude': longitude,
      'address': address,
      'media_urls': mediaUrls,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  factory HazardReport.fromJson(Map<String, dynamic> json) {
    return HazardReport(
      title: json['title'] as String,
      description: json['description'] as String,
      hazardType: json['hazard_type'] as String,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      address: json['address'] as String?,
      mediaUrls: (json['media_urls'] as List<dynamic>?)
          ?.map((e) => e.toString()).toList() ?? [],
      timestamp: DateTime.parse(json['timestamp'] as String),
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
