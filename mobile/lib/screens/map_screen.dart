import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:intl/intl.dart';
import 'package:latlong2/latlong.dart';
import 'package:synapse_citizen_app/models/hazard_report.dart';
import 'package:synapse_citizen_app/services/api_service.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  _MapScreenState createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final _apiService = ApiService();

  List<Marker> _buildMarkers(BuildContext context, List<HazardReport> reports) {
    return reports.map((report) {
      return Marker(
        width: 80.0,
        height: 80.0,
        point: LatLng(report.latitude, report.longitude),
        child: GestureDetector(
          onTap: () {
            _showReportBottomSheet(context, report);
          },
          child: Icon(
            Icons.location_pin,
            color: _getMarkerColor(report.isVerified),
            size: 40.0,
          ),
        ),
      );
    }).toList();
  }

  Color _getMarkerColor(bool? isVerified) {
    if (isVerified == true) {
      return Colors.red; // Verified
    }
    return Colors.orange; // Pending
  }

void _showReportBottomSheet(BuildContext context, HazardReport report) {
  showModalBottomSheet(
    context: context,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (context) {
      return Padding(
        padding: const EdgeInsets.all(16.0),
        child: Wrap(
          children: [
            ListTile(
              leading: report.mediaUrls.isNotEmpty // Use mediaUrls instead of imageUrl
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(8.0),
                      child: Image.network(
                        report.mediaUrls.first, // Use the first image
                        width: 60,
                        height: 60,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) =>
                            const Icon(Icons.image_not_supported, size: 50),
                      ),
                    )
                  : const Icon(Icons.image_not_supported, size: 50),
              title: Text(report.title,
                  style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(
                  '${report.hazardType} • ${report.createdAt != null ? DateFormat.jm().format(report.createdAt!) : 'No date'}'), // Handle null createdAt
            ),
            const Divider(height: 20),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Text(report.description),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Chip(
                  avatar: Icon(
                    report.isVerified == true ? Icons.verified : Icons.hourglass_empty,
                    color: Colors.white,
                  ),
                  label: Text(report.isVerified == true ? 'Verified' : 'Pending'),
                  backgroundColor: report.isVerified == true ? Colors.red : Colors.orange,
                  labelStyle: const TextStyle(color: Colors.white),
                ),
              ],
            ),
          ],
        ),
      );
    },
  );
}
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Hazard Map')),
      body: FutureBuilder<List<HazardReport>>(
        future: _apiService.getHazardReports(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No reports found.'));
          }

          final reports = snapshot.data!;

          return FlutterMap(
            options: MapOptions(
              initialCenter: const LatLng(17.6868, 83.2185), // Visakhapatnam
              initialZoom: 9.0,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.example.synapse_citizen_app',
              ),
              MarkerLayer(
                markers: _buildMarkers(context, reports),
              ),
            ],
          );
        },
      ),
    );
  }
}