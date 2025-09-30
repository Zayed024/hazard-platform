import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:logger/logger.dart';
import '../models/hazard_report.dart';

class ApiService {
  static const String _baseUrl = 'http://10.0.2.2:8000/api'; // Android emulator
  // Use 'http://localhost:8000/api' for iOS simulator
  // Use your actual IP for physical devices
  
  final Logger _logger = Logger();
  
  Future<HazardReportResponse> submitHazardReport(HazardReport report) async {
    try {
      _logger.i('Submitting hazard report: ${report.title}');

      var uri = Uri.parse('$_baseUrl/hazards/report');
      var request = http.MultipartRequest('POST', uri);

      // Add form fields
      request.fields['title'] = report.title;
      request.fields['description'] = report.description;
      request.fields['hazard_type'] = report.hazardType;
      request.fields['latitude'] = report.latitude.toString();
      request.fields['longitude'] = report.longitude.toString();
      if (report.address != null) {
        request.fields['address'] = report.address!;
      }

      // Add images if any
      for (var imageFile in report.mediaFiles ?? []) {
        var stream = http.ByteStream(imageFile.openRead());
        var length = await imageFile.length();
        var multipartFile = http.MultipartFile('images', stream, length,
            filename: imageFile.path.split('/').last);
        request.files.add(multipartFile);
      }

      var streamedResponse = await request.send().timeout(const Duration(seconds: 30));
      var response = await http.Response.fromStream(streamedResponse);

      _logger.d('Response status: ${response.statusCode}');
      _logger.d('Response body: ${response.body}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        final responseData = json.decode(response.body);
        return HazardReportResponse.fromJson(responseData);
      } else {
        throw ApiException(
          'Failed to submit report: ${response.statusCode}',
          response.statusCode,
        );
      }
    } on SocketException {
      throw ApiException(
        'No internet connection. Please check your network and try again.',
        0,
      );
    } on http.ClientException {
      throw ApiException(
        'Connection failed. Please check if the server is running.',
        0,
      );
    } catch (e) {
      _logger.e('Error submitting report: $e');
      if (e is ApiException) rethrow;
      throw ApiException('Unexpected error: $e', 0);
    }
  }

  Future<List<Map<String, dynamic>>> getNearbyHazards(
    double lat, 
    double lon, {
    int radius = 5000,
  }) async {
    try {
      _logger.i('Fetching nearby hazards for location: $lat, $lon');
      
      final response = await http.get(
        Uri.parse('$_baseUrl/hazards/nearby?lat=$lat&lon=$lon&radius=$radius'),
        headers: {
          'Accept': 'application/json',
        },
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        return List<Map<String, dynamic>>.from(responseData['hazards']);
      } else {
        throw ApiException(
          'Failed to fetch nearby hazards: ${response.statusCode}',
          response.statusCode,
        );
      }
    } on SocketException {
      throw ApiException(
        'No internet connection. Please check your network and try again.',
        0,
      );
    } catch (e) {
      _logger.e('Error fetching nearby hazards: $e');
      if (e is ApiException) rethrow;
      throw ApiException('Failed to fetch nearby hazards: $e', 0);
    }
  }

  Future<Map<String, dynamic>> getDashboardAnalytics() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/hazards/analytics/dashboard'),
        headers: {
          'Accept': 'application/json',
        },
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw ApiException(
          'Failed to fetch analytics: ${response.statusCode}',
          response.statusCode,
        );
      }
    } catch (e) {
      _logger.e('Error fetching analytics: $e');
      if (e is ApiException) rethrow;
      throw ApiException('Failed to fetch analytics: $e', 0);
    }
  }

  Future<bool> checkServerHealth() async {
    try {
      final response = await http.get(
        Uri.parse('${_baseUrl.replaceAll('/api', '')}/health'),
        headers: {'Accept': 'application/json'},
      ).timeout(const Duration(seconds: 10));

      return response.statusCode == 200;
    } catch (e) {
      _logger.w('Server health check failed: $e');
      return false;
    }
  }

  Future<List<HazardReport>> getHazardReports() async {
    try {
      _logger.i('Fetching all hazard reports');
      final response = await http.get(
        Uri.parse('$_baseUrl/hazards/reports/'),
        headers: {'Accept': 'application/json'},
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final List<dynamic> responseData = json.decode(response.body);
        return responseData.map((data) => HazardReport.fromJson(data)).toList();
      } else {
        throw ApiException(
          'Failed to fetch hazard reports: ${response.statusCode}',
          response.statusCode,
        );
      }
    } on SocketException {
      throw ApiException(
        'No internet connection. Please check your network and try again.',
        0,
      );
    } catch (e) {
      _logger.e('Error fetching hazard reports: $e');
      if (e is ApiException) rethrow;
      throw ApiException('Failed to fetch hazard reports: $e', 0);
    }
  }
}

class ApiException implements Exception {
  final String message;
  final int statusCode;

  ApiException(this.message, this.statusCode);

  @override
  String toString() => 'ApiException: $message (Status: $statusCode)';
}