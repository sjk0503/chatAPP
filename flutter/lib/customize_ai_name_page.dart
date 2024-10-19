import 'package:flutter/material.dart';
import 'customize_ai_image_page.dart'; // 이미지 업로드 페이지 import

class CustomizeAINamePage extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;

  CustomizeAINamePage({required this.toggleTheme, required this.isDarkMode});

  @override
  _CustomizeAINamePageState createState() => _CustomizeAINamePageState();
}

class _CustomizeAINamePageState extends State<CustomizeAINamePage> {
  final TextEditingController _characterNameController = TextEditingController();
  int _currentCharacterCount = 0;
  final int _maxCharacterCount = 16; // 최대 글자 수

  @override
  void initState() {
    super.initState();
    _characterNameController.addListener(() {
      setState(() {
        _currentCharacterCount = _characterNameController.text.length;
      });
    });
  }

  @override
  void dispose() {
    _characterNameController.dispose();
    super.dispose();
  }

  void _nextStep() {
    if (_characterNameController.text.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => CustomizeAIImagePage(
            characterName: _characterNameController.text,
            toggleTheme: widget.toggleTheme,
            isDarkMode: widget.isDarkMode,
          ),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('캐릭터 이름을 입력해 주세요!')),
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
            // 게이지바 추가 (전체의 1/5)
            LinearProgressIndicator(
              value: 0.2, // 1/5 진행 상태
              backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
              color: Colors.deepPurple,
            ),
            SizedBox(height: 20), // 간격 조정
            Text(
              '제작할 캐릭터의 이름을 알려주세요!',
              style: TextStyle(
                fontSize: 22,
                color: widget.isDarkMode ? Colors.white : Colors.black,
                fontFamily: 'PretendardSemiBold',
              ),
            ),
            SizedBox(height: 20),
            TextField(
              controller: _characterNameController,
              decoration: InputDecoration(
                hintText: '캐릭터 이름 입력',
                border: OutlineInputBorder(),
                counterText: "", // 여기에서 기본 글자수 표기(counterText)를 숨김
              ),
              maxLength: _maxCharacterCount, // 최대 글자 수 제한
            ),
            // 좌측에 글자수 표기
            Text(
              '$_currentCharacterCount/$_maxCharacterCount', // 현재 글자 수 / 최대 글자 수
              style: TextStyle(
                fontSize: 14,
                color: widget.isDarkMode ? Colors.white54 : Colors.black54,
              ),
            ),
            SizedBox(height: 10),
            Text(
              '저작권 침해 / 비윤리적 캐릭터는 삭제될 수 있습니다.',
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey, // 회색 글씨로 안내문구 표시
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
                onPressed: _nextStep,
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
