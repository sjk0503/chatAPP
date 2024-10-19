import 'package:flutter/material.dart';
import 'dart:io'; // File을 사용하기 위해 필요
import 'dart:convert'; // JSON 인코딩을 위해 필요
import 'package:http/http.dart' as http; // 서버 통신을 위해 필요
import 'customize_ai_summary_page.dart'; // 6번 페이지 import

class CustomizeAIPromptPage extends StatefulWidget {
  final String characterName;
  final File? characterImage;
  final List<String> selectedCategories;
  final String shortDescription;
  final String detailedDescription; // 상세 소개 추가
  final Function toggleTheme;
  final bool isDarkMode;

  CustomizeAIPromptPage({
    required this.characterName,
    required this.characterImage,
    required this.selectedCategories,
    required this.shortDescription,
    required this.detailedDescription, // 상세 소개 추가
    required this.toggleTheme,
    required this.isDarkMode,
  });

  @override
  _CustomizeAIPromptPageState createState() => _CustomizeAIPromptPageState();
}

class _CustomizeAIPromptPageState extends State<CustomizeAIPromptPage> {
  final TextEditingController _promptController = TextEditingController();
  bool _isSearchingLatestInfo = false;
  bool _isUpdatingUserInfo = false;

  Future<void> _sendDataToServer() async {
    // 서버로 보낼 데이터를 준비합니다.
    Map<String, dynamic> data = {
      'characterName': widget.characterName,
      'selectedCategories': widget.selectedCategories,
      'shortDescription': widget.shortDescription,
      'detailedDescription': widget.detailedDescription, // 상세 소개 추가
      'prompt': _promptController.text,
      'isSearchingLatestInfo': _isSearchingLatestInfo,
      'isUpdatingUserInfo': _isUpdatingUserInfo,
    };

    if (widget.characterImage != null) {
      List<int> imageBytes = widget.characterImage!.readAsBytesSync();
      String base64Image = base64Encode(imageBytes);
      data['characterImage'] = base64Image;
    }

    try {
      // 서버로 데이터를 전송합니다 (create_ID API).
      final response = await http.post(
        Uri.parse('https://3i8lrr8hcj.execute-api.eu-north-1.amazonaws.com/dami/creat_ID'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      );

      if (response.statusCode == 200) {
        // 서버 전송이 성공하면 캐릭터 요약 페이지로 이동합니다.
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => CustomizeAISummaryPage(
              characterName: widget.characterName,
              characterImage: widget.characterImage,
              selectedCategories: widget.selectedCategories,
              shortDescription: widget.shortDescription,
              detailedDescription: widget.detailedDescription, // 상세 소개 전달
              prompt: _promptController.text, // 프롬프트 전달
              toggleTheme: widget.toggleTheme,
              isDarkMode: widget.isDarkMode,
            ),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('캐릭터 생성 실패: 서버 오류 발생')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('캐릭터 생성 실패: $e')),
      );
    }
  }

  void _confirmDeleteCharacter() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('캐릭터 삭제'),
          content: Text('캐릭터와 해당 정보는 복구할 수 없습니다. 삭제하시겠습니까?'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // 팝업 닫기
              },
              child: Text('취소'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // 팝업 닫기
                Navigator.pop(context); // 이전 페이지로 이동
              },
              child: Text('삭제'),
            ),
          ],
        );
      },
    );
  }

  void _nextStep() {
    if (_promptController.text.isNotEmpty) {
      _sendDataToServer(); // 서버로 데이터를 전송하고, 요약 페이지로 이동
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('프롬프트를 입력해주세요.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false, // 키보드가 올라와도 레이아웃 변화 방지
      appBar: AppBar(
        title: Text(
          'AI 캐릭터 프롬프트 작성',
          style: TextStyle(fontFamily: 'PretendardSemiBold'),
        ),
        backgroundColor: widget.isDarkMode ? Colors.black : Colors.white,
        iconTheme: IconThemeData(color: widget.isDarkMode ? Colors.white : Colors.black),
        actions: [
          IconButton(
            icon: Icon(Icons.delete),
            onPressed: _confirmDeleteCharacter, // 삭제 버튼 동작
            tooltip: '캐릭터 삭제',
          ),
        ],
      ),
      backgroundColor: widget.isDarkMode ? Colors.black : Colors.white,
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    LinearProgressIndicator(
                      value: 1.0, // 5/5 진행 상태
                      backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
                      color: Colors.deepPurple,
                    ),
                    SizedBox(height: 20),
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            '만들고 싶은 캐릭터의 구체적인 정보를\n입력해주세요!',
                            style: TextStyle(
                              fontSize: 22,
                              color: widget.isDarkMode ? Colors.white : Colors.black,
                              fontFamily: 'PretendardSemiBold',
                            ),
                          ),
                        ),
                        IconButton(
                          icon: Icon(Icons.info_outline, color: widget.isDarkMode ? Colors.white : Colors.black),
                          onPressed: () {
                            showDialog(
                              context: context,
                              builder: (BuildContext context) {
                                return AlertDialog(
                                  title: Text('프롬프트 작성 팁'),
                                  content: Text(
                                    '1. 캐릭터의 성격, 대화 스타일을 구체적으로 입력해보세요.\n'
                                        '2. 원하는 기능이나 역할을 명확하게 적어주세요.\n'
                                        '3. 예시를 포함하면 더 좋습니다.',
                                  ),
                                  actions: [
                                    TextButton(
                                      onPressed: () {
                                        Navigator.of(context).pop();
                                      },
                                      child: Text('확인'),
                                    ),
                                  ],
                                );
                              },
                            );
                          },
                        ),
                      ],
                    ),
                    SizedBox(height: 10),
                    Container(
                      padding: const EdgeInsets.all(12.0),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10.0),
                        color: widget.isDarkMode ? Colors.white12 : Colors.black12,
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              widget.characterImage != null
                                  ? CircleAvatar(
                                radius: 40,
                                backgroundImage: FileImage(widget.characterImage!),
                              )
                                  : CircleAvatar(
                                radius: 40,
                                backgroundColor: Colors.grey[300],
                                child: Icon(
                                  Icons.person,
                                  size: 40,
                                  color: Colors.grey[700],
                                ),
                              ),
                              SizedBox(width: 16),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      widget.characterName,
                                      style: TextStyle(
                                        fontSize: 22,
                                        fontWeight: FontWeight.bold,
                                        color: widget.isDarkMode ? Colors.white : Colors.black,
                                      ),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    if (widget.shortDescription.isNotEmpty)
                                      Padding(
                                        padding: const EdgeInsets.only(top: 8.0),
                                        child: Text(
                                          widget.shortDescription,
                                          style: TextStyle(
                                            color: widget.isDarkMode ? Colors.white70 : Colors.black87,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ),
                                    SizedBox(height: 8),
                                    Text(
                                      widget.selectedCategories.map((category) => '#$category').join(' '),
                                      style: TextStyle(
                                        color: widget.isDarkMode ? Colors.white70 : Colors.black87,
                                        fontSize: 14,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 20),
                    TextField(
                      controller: _promptController,
                      maxLines: 6,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: '프롬프트',
                        labelStyle: TextStyle(
                          color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                        ),
                      ),
                      style: TextStyle(
                        color: widget.isDarkMode ? Colors.white : Colors.black,
                      ),
                    ),
                    SizedBox(height: 20),
                    Row(
                      children: [
                        Checkbox(
                          value: _isSearchingLatestInfo,
                          onChanged: (bool? value) {
                            setState(() {
                              _isSearchingLatestInfo = value ?? false;
                            });
                          },
                        ),
                        SizedBox(width: 4),
                        Text(
                          '최신 정보 검색 기능',
                          style: TextStyle(
                            color: widget.isDarkMode ? Colors.white : Colors.black,
                          ),
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        Checkbox(
                          value: _isUpdatingUserInfo,
                          onChanged: (bool? value) {
                            setState(() {
                              _isUpdatingUserInfo = value ?? false;
                            });
                          },
                        ),
                        SizedBox(width: 4),
                        Text(
                          '사용자 정보 업데이트 기능',
                          style: TextStyle(
                            color: widget.isDarkMode ? Colors.white : Colors.black,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: SizedBox(
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
                  '완료',
                  style: TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
