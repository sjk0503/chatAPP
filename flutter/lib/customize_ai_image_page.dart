import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'customize_ai_category_page.dart'; // 3번 페이지 import

class CustomizeAIImagePage extends StatefulWidget {
  final String characterName;
  final Function toggleTheme;
  final bool isDarkMode;

  CustomizeAIImagePage({
    required this.characterName,
    required this.toggleTheme,
    required this.isDarkMode,
  });

  @override
  _CustomizeAIImagePageState createState() => _CustomizeAIImagePageState();
}

class _CustomizeAIImagePageState extends State<CustomizeAIImagePage> {
  File? _image;

  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  void _nextStep() {
    if (_image != null) {
      // 3번 페이지로 이동
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => CustomizeAICategoryPage(
            characterName: widget.characterName, // 1번 페이지에서 등록한 이름 전달
            characterImage: _image, // 2번 페이지에서 등록한 이미지 전달
            toggleTheme: widget.toggleTheme,
            isDarkMode: widget.isDarkMode,
          ),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('프로필 사진을 업로드해 주세요!')),
      );
    }
  }

  void _showDeleteDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('캐릭터 삭제'),
          content: Text('삭제된 캐릭터와 캐릭터 정보는 복구할 수 없습니다. 계속하시겠습니까?'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // 다이얼로그 닫기
              },
              child: Text('취소'),
            ),
            TextButton(
              onPressed: () {
                Navigator.popUntil(context, (route) => route.isFirst); // 친구 목록으로 이동
              },
              child: Text('삭제'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    // 이름이 길면 ...으로 표시
    String shortenedName = widget.characterName.length > 8
        ? '${widget.characterName.substring(0, 8)}...'
        : widget.characterName;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'AI 캐릭터 커스터마이징',
          style: TextStyle(fontFamily: 'PretendardSemiBold'),
        ),
        backgroundColor: widget.isDarkMode ? Colors.black : Colors.white,
        iconTheme: IconThemeData(color: widget.isDarkMode ? Colors.white : Colors.black),
        actions: [
          IconButton(
            icon: Icon(Icons.delete),
            onPressed: _showDeleteDialog,
            tooltip: '캐릭터 삭제',
          ),
        ],
      ),
      backgroundColor: widget.isDarkMode ? Colors.black : Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 게이지바 추가 (전체의 2/5)
            LinearProgressIndicator(
              value: 0.4, // 2/5 진행 상태
              backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
              color: Colors.deepPurple,
            ),
            SizedBox(height: 20), // 간격 조정
            Text(
              '$shortenedName 프로필 사진을 업로드하세요!', // 이름 추가
              style: TextStyle(
                fontSize: 22,
                color: widget.isDarkMode ? Colors.white : Colors.black,
                fontFamily: 'PretendardSemiBold',
              ),
            ),
            SizedBox(height: 20),
            GestureDetector(
              onTap: _pickImage,
              child: Center(
                child: _image != null
                    ? Column(
                  children: [
                    CircleAvatar(
                      radius: 60,
                      backgroundImage: FileImage(_image!),
                    ),
                    SizedBox(height: 10),
                    Text(
                      widget.characterName, // 이름 추가
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: widget.isDarkMode ? Colors.white : Colors.black,
                      ),
                    ),
                  ],
                )
                    : Column(
                  children: [
                    CircleAvatar(
                      radius: 60,
                      backgroundColor: Colors.grey[300],
                      child: Icon(
                        Icons.add_a_photo,
                        size: 40,
                        color: Colors.grey[700],
                      ),
                    ),
                    SizedBox(height: 10),
                    Text(
                      widget.characterName, // 이름 추가
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: widget.isDarkMode ? Colors.white : Colors.black,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            Spacer(),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.deepPurple,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(6.0),
                  ),
                ),
                onPressed: _nextStep, // 3번 페이지로 넘어가는 로직
                child: Text(
                  '다음',
                  style: TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'PretendardRegular'),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
