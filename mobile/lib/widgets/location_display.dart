import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

class LocationDisplay extends StatelessWidget {
  final Position? position;
  final String? address;
  final bool isLoading;
  final VoidCallback onRefresh;

  const LocationDisplay({
    super.key,
    required this.position,
    required this.address,
    required this.isLoading,
    required this.onRefresh,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.location_on, 
                  color: position != null ? Colors.green : Colors.grey,
                  size: 24,
                ),
                const SizedBox(width: 8),
                Text(
                  'Location',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Spacer(),
                if (!isLoading)
                  IconButton(
                    onPressed: onRefresh,
                    icon: const Icon(Icons.refresh),
                    tooltip: 'Refresh location',
                  ),
              ],
            ),
            
            const SizedBox(height: 12),
            
            if (isLoading) ...[
              const Row(
                children: [
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                  SizedBox(width: 12),
                  Text('Getting current location...'),
                ],
              ),
            ] else if (position != null) ...[
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.green.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.green.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.check_circle, 
                             color: Colors.green.shade600, size: 16),
                        const SizedBox(width: 6),
                        Text(
                          'Location acquired',
                          style: TextStyle(
                            color: Colors.green.shade800,
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 8),
                    
                    Text(
                      'Lat: ${position!.latitude.toStringAsFixed(6)}',
                      style: TextStyle(
                        color: Colors.green.shade700,
                        fontSize: 13,
                        fontFamily: 'monospace',
                      ),
                    ),
                    
                    Text(
                      'Lon: ${position!.longitude.toStringAsFixed(6)}',
                      style: TextStyle(
                        color: Colors.green.shade700,
                        fontSize: 13,
                        fontFamily: 'monospace',
                      ),
                    ),
                    
                    if (address != null) ...[
                      const SizedBox(height: 6),
                      Text(
                        'Accuracy: ±${position!.accuracy.toStringAsFixed(0)}m',
                        style: TextStyle(
                          color: Colors.green.shade600,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ] else ...[
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.red.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.red.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.error_outline, 
                             color: Colors.red.shade600, size: 16),
                        const SizedBox(width: 6),
                        Text(
                          'Location not available',
                          style: TextStyle(
                            color: Colors.red.shade800,
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 6),
                    
                    Text(
                      'Please enable location services and grant permission',
                      style: TextStyle(
                        color: Colors.red.shade600,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}