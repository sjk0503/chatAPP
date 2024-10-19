import 'package:flutter/material.dart';
import 'dart:io';

class CustomizeAISummaryPage extends StatelessWidget {
  final String characterName;
  final File? characterImage;
  final List<String> selectedCategories;
  final String shortDescription;
  final String detailedDescription; // 추가된 상세 소개
  final String prompt;
  final Function toggleTheme;
  final bool isDarkMode;

  CustomizeAISummaryPage({
    required this.characterName,
    required this.characterImage,
    required this.selectedCategories,
    required this.shortDescription,
    required this.detailedDescription, // 상세 소개 전달 받음
    required this.prompt,
    required this.toggleTheme,
    required this.isDarkMode,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'AI 캐릭터 요약',
          style: TextStyle(fontFamily: 'PretendardSemiBold'),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CircleAvatar(
                      radius: 60,
                      backgroundImage: characterImage != null ? FileImage(characterImage!) : null,
                      backgroundColor: characterImage == null ? Colors.grey[300] : Colors.transparent,
                      child: characterImage == null
                          ? Icon(Icons.person, size: 60, color: Colors.grey[700])
                          : null,
                    ),
                    SizedBox(height: 20),
                    Text(
                      characterName,
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(height: 10),
                    if (shortDescription.isNotEmpty)
                      Text(
                        shortDescription,
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.grey,
                        ),
                      ),
                    SizedBox(height: 10),
                    if (detailedDescription.isNotEmpty) // 상세 정보가 있을 때만 표시
                      Text(
                        detailedDescription,
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.black87,
                        ),
                      ),
                    SizedBox(height: 20),
                    Text(
                      selectedCategories.map((category) => '#$category').join(' '),
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.black54,
                      ),
                    ),
                    SizedBox(height: 20),
                    Text(
                      '캐릭터가 성공적으로 생성되었습니다!',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.popUntil(context, (route) => route.isFirst); // 친구 리스트로 돌아가기
                },
                child: Text('친구 목록으로 돌아가기'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
