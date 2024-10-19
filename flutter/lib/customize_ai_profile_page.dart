import 'package:flutter/material.dart';
import 'dart:io'; // File을 사용하기 위해 필요
import 'customize_ai_prompt_page.dart'; // CustomizeAIPromptPage import
import 'friends_list_page.dart'; // 친구 목록 페이지를 위한 import

class CustomizeAIProfilePage extends StatefulWidget {
  final String characterName;
  final File? characterImage;
  final List<String> selectedCategories;
  final Function toggleTheme;
  final bool isDarkMode;

  CustomizeAIProfilePage({
    required this.characterName,
    required this.characterImage,
    required this.selectedCategories,
    required this.toggleTheme,
    required this.isDarkMode,
  });

  @override
  _CustomizeAIProfilePageState createState() => _CustomizeAIProfilePageState();
}

class _CustomizeAIProfilePageState extends State<CustomizeAIProfilePage> {
  final TextEditingController _shortDescriptionController = TextEditingController();
  final TextEditingController _detailedDescriptionController = TextEditingController();
  String _shortDescription = '';
  int _charCount = 0; // 글자 수 카운트 변수

  // "을/를" 문법에 맞는 조사 선택
  String _getPostfixForObjectMarker(String name) {
    final lastChar = name.runes.last; // 마지막 글자의 유니코드 값
    final isLastCharHasBatchim = (lastChar - 44032) % 28 != 0; // 받침 여부 계산
    return isLastCharHasBatchim ? '을' : '를'; // 받침이 있으면 "을", 없으면 "를"
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
                Navigator.pushAndRemoveUntil(
                  context,
                  MaterialPageRoute(
                    builder: (context) => FriendsListPage(
                      toggleTheme: widget.toggleTheme,
                      isDarkMode: widget.isDarkMode,
                    ),
                  ),
                      (Route<dynamic> route) => false, // 친구 목록 페이지로 이동
                );
              },
              child: Text('삭제'),
            ),
          ],
        );
      },
    );
  }

  void _nextStep() {
    if (_shortDescription.isNotEmpty && _detailedDescriptionController.text.isNotEmpty) {
      // 다음 페이지로 이동, 상세 정보 전달
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => CustomizeAIPromptPage(
            characterName: widget.characterName,
            characterImage: widget.characterImage,
            selectedCategories: widget.selectedCategories,
            shortDescription: _shortDescription, // 짧은 소개 전달
            detailedDescription: _detailedDescriptionController.text, // 상세 정보 전달
            toggleTheme: widget.toggleTheme,
            isDarkMode: widget.isDarkMode,
          ),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('짧은 소개와 상세 정보를 모두 입력해주세요.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    String objectMarker = _getPostfixForObjectMarker(widget.characterName);

    return Scaffold(
      resizeToAvoidBottomInset: false, // 키보드가 올라와도 레이아웃 변화 방지
      appBar: AppBar(
        title: Text(
          'AI 캐릭터 프로필 작성',
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
                    // 상단 진행 게이지 추가 (전체 4/5)
                    LinearProgressIndicator(
                      value: 0.8, // 4/5 진행 상태
                      backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
                      color: Colors.deepPurple,
                    ),
                    SizedBox(height: 20),
                    // 상단 안내 문구 (2줄로 표시)
                    Text(
                      '${widget.characterName}$objectMarker 소개할 짧은 소개와\n상세정보를 입력해주세요!',
                      style: TextStyle(
                        fontSize: 22,
                        color: widget.isDarkMode ? Colors.white : Colors.black,
                        fontFamily: 'PretendardSemiBold',
                      ),
                    ),
                    SizedBox(height: 20),
                    // "캐릭터와 대화하기 전에 먼저 보이게 될 거예요." 문구 추가 (프로필 박스 위로 이동)
                    Text(
                      '캐릭터와 대화하기 전에 먼저 보이게 될 거예요.',
                      style: TextStyle(
                        color: Colors.grey,
                        fontSize: 14,
                        fontFamily: 'PretendardRegular',
                      ),
                    ),
                    SizedBox(height: 10),
                    // 프로필 이미지와 이름, 카테고리, 짧은 소개
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
                                      overflow: TextOverflow.ellipsis, // 이름이 길어지면 줄임표 처리
                                    ),
                                    if (_shortDescription.isNotEmpty) // 짧은 소개가 있을 때만 표시
                                      Padding(
                                        padding: const EdgeInsets.only(top: 8.0),
                                        child: Text(
                                          _shortDescription,
                                          style: TextStyle(
                                            color: widget.isDarkMode ? Colors.white70 : Colors.black87,
                                            fontSize: 14,
                                            fontFamily: 'PretendardRegular',
                                          ),
                                        ),
                                      ),
                                    SizedBox(height: 8),
                                    Text(
                                      widget.selectedCategories.map((category) => '#$category').join(' '),
                                      style: TextStyle(
                                        color: widget.isDarkMode ? Colors.white70 : Colors.black87,
                                        fontSize: 14,
                                        fontFamily: 'PretendardRegular',
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
                    // 짧은 소개 입력 및 글자 수 카운팅
                    TextField(
                      controller: _shortDescriptionController,
                      maxLength: 40, // 글자수 제한
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: '짧은 소개',
                        labelStyle: TextStyle(
                          color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                          fontFamily: 'PretendardRegular',
                        ),
                        counterText: '${_charCount}/40', // 글자 수 카운팅 표시
                      ),
                      style: TextStyle(
                        color: widget.isDarkMode ? Colors.white : Colors.black,
                        fontFamily: 'PretendardRegular',
                      ),
                      onChanged: (value) {
                        setState(() {
                          _shortDescription = value;
                          _charCount = value.length; // 글자 수 업데이트
                        });
                      },
                    ),
                    SizedBox(height: 20),
                    // 상세 정보 입력
                    TextField(
                      controller: _detailedDescriptionController,
                      maxLines: 6, // 상세 정보는 여러 줄 입력 가능
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: '상세 정보',
                        labelStyle: TextStyle(
                          color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                          fontFamily: 'PretendardRegular',
                        ),
                      ),
                      style: TextStyle(
                        color: widget.isDarkMode ? Colors.white : Colors.black,
                        fontFamily: 'PretendardRegular',
                      ),
                    ),
                    SizedBox(height: 20),
                  ],
                ),
              ),
            ),
          ),
          // 다음 버튼 고정 (하단에 고정)
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
                onPressed: _nextStep, // 다음 단계로 이동
                child: Text(
                  '다음',
                  style: TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'PretendardRegular'),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
