import 'package:flutter/material.dart';

class ReportScreen extends StatelessWidget {
  const ReportScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Report Traffic Violation'),
      ),

      body: Padding(
        padding: const EdgeInsets.all(20),

        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,

          children: [

            const Text(
              'Submit Traffic Violation',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 25),

            Container(
              height: 180,
              decoration: BoxDecoration(
                border: Border.all(),
                borderRadius: BorderRadius.circular(12),
              ),

              child: const Center(
                child: Icon(
                  Icons.camera_alt,
                  size: 70,
                ),
              ),
            ),

            const SizedBox(height: 20),

            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.camera_alt),
              label: const Text('Capture Photo / Video'),
            ),

            const SizedBox(height: 10),

            OutlinedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.location_on),
              label: const Text('Get Current Location'),
            ),

            const SizedBox(height: 10),

            const TextField(
              maxLines: 3,
              decoration: InputDecoration(
                labelText: 'Description',
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: () {},
              child: const Text('SUBMIT REPORT'),
            ),
          ],
        ),
      ),
    );
  }
}