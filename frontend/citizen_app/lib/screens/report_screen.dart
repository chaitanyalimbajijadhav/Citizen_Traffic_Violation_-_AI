import 'package:flutter/material.dart';

class ReportScreen extends StatefulWidget {
  const ReportScreen({super.key});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  final TextEditingController descriptionController =
      TextEditingController();

  String? selectedViolation;

  final List<String> violationTypes = [
    'Overspeeding',
    'Signal Violation',
    'Wrong Parking',
    'Helmet Violation',
    'Seat Belt Violation',
    'Wrong Side Driving',
    'Mobile Phone While Driving',
    'Other',
  ];

  @override
  void dispose() {
    descriptionController.dispose();
    super.dispose();
  }

  void continueReport() {
    if (selectedViolation == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select a violation type'),
        ),
      );
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Report details saved for next step'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Report Violation'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Report Traffic Violation',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 8),

            Text(
              'Provide the details of the incident.',
              style: TextStyle(
                color: Colors.grey.shade600,
              ),
            ),

            const SizedBox(height: 25),

            // Violation Type
            DropdownButtonFormField<String>(
              initialValue: selectedViolation,
              decoration: InputDecoration(
                labelText: 'Violation Type',
                prefixIcon: const Icon(
                  Icons.warning_amber_outlined,
                ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              items: violationTypes.map((violation) {
                return DropdownMenuItem<String>(
                  value: violation,
                  child: Text(violation),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  selectedViolation = value;
                });
              },
            ),

            const SizedBox(height: 20),

            // Description
            TextField(
              controller: descriptionController,
              maxLines: 5,
              decoration: InputDecoration(
                labelText: 'Description',
                hintText: 'Describe what happened...',
                alignLabelWithHint: true,
                prefixIcon: const Padding(
                  padding: EdgeInsets.only(bottom: 80),
                  child: Icon(
                    Icons.description_outlined,
                  ),
                ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),

            const SizedBox(height: 25),

            // Evidence Placeholder
            Container(
              height: 150,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.grey.shade400,
                ),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.photo_camera_outlined,
                    size: 45,
                  ),
                  SizedBox(height: 10),
                  Text(
                    'Evidence will be added in the next step',
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // Location Placeholder
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Row(
                children: [
                  Icon(
                    Icons.location_on_outlined,
                  ),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Location will be captured in the next step',
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 30),

            // Continue Button
            SizedBox(
              height: 52,
              child: ElevatedButton(
                onPressed: continueReport,
                child: const Text(
                  'Continue',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}