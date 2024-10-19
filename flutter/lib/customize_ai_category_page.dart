import 'package:flutter/material.dart';
import 'dart:io'; // File을 사용하기 위해 필요
import 'customize_ai_profile_page.dart'; // 4번째 페이지 import
import 'friends_list_page.dart'; // 친구 목록 페이지 import

class CustomizeAICategoryPage extends StatefulWidget {
  final String characterName;
  final File? characterImage;
  final Function toggleTheme;
  final bool isDarkMode;

  CustomizeAICategoryPage({
    required this.characterName,
    required this.characterImage,
    required this.toggleTheme,
    required this.isDarkMode,
  });

  @override
  _CustomizeAICategoryPageState createState() => _CustomizeAICategoryPageState();
}

class _CustomizeAICategoryPageState extends State<CustomizeAICategoryPage> {
  List<String> selectedCategories = [];
  final List<Map<String, dynamic>> categories = [
    {'name': '로맨스', 'icon': Icons.favorite},
    {'name': '상황극', 'icon': Icons.theater_comedy},
    {'name': '힐링', 'icon': Icons.spa},
    {'name': '유머', 'icon': Icons.emoji_emotions},
    {'name': '셀럽', 'icon': Icons.star},
    {'name': '영화/드라마', 'icon': Icons.movie},
    {'name': '소설/웹툰', 'icon': Icons.book},
    {'name': '게임/애니메이션', 'icon': Icons.gamepad},
    {'name': '음악', 'icon': Icons.music_note},
    {'name': '스포츠', 'icon': Icons.sports},
    {'name': '여행', 'icon': Icons.flight},
    {'name': '기타', 'icon': Icons.more_horiz},
  ];

  void _toggleCategory(String category) {
    setState(() {
      if (selectedCategories.contains(category)) {
        selectedCategories.remove(category);
      } else if (selectedCategories.length < 3) {
        selectedCategories.add(category);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('카테고리는 최대 3개까지 선택 가능합니다.')),
        );
      }
    });
  }

  void _nextStep() {
    if (selectedCategories.isNotEmpty) {
      // 최소 한 개의 카테고리가 선택되면 다음 단계로 이동
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => CustomizeAIProfilePage(
            characterName: widget.characterName,
            characterImage: widget.characterImage,
            selectedCategories: selectedCategories, // 선택한 카테고리 전달
            toggleTheme: widget.toggleTheme,
            isDarkMode: widget.isDarkMode,
          ),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('최소 한 개의 카테고리를 선택해야 합니다.')),
      );
    }
  }

  void _showDeleteDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(
            '캐릭터 삭제',
            style: TextStyle(fontFamily: 'PretendardSemiBold'),
          ),
          content: Text(
            '캐릭터를 삭제하시겠습니까?\n삭제된 캐릭터와 정보는 복구할 수 없습니다.',
            style: TextStyle(fontFamily: 'PretendardRegular'),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text('취소', style: TextStyle(fontFamily: 'PretendardRegular')),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (context) => FriendsListPage(
                      toggleTheme: widget.toggleTheme,
                      isDarkMode: widget.isDarkMode,
                    ),
                  ),
                );
              },
              child: Text('삭제', style: TextStyle(fontFamily: 'PretendardRegular')),
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
          'AI 캐릭터 카테고리 선택',
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
            // 상단 진행 게이지 추가 (전체 3/5)
            LinearProgressIndicator(
              value: 0.6, // 3/5 진행 상태
              backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
              color: Colors.deepPurple,
            ),
            SizedBox(height: 20),
            // 상단 캐릭터 정보 (이미지 + 이름 + 선택된 카테고리)
            Container(
              padding: const EdgeInsets.all(12.0),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10.0),
                color: widget.isDarkMode ? Colors.white12 : Colors.black12,
              ),
              child: Row(
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
                        SizedBox(height: 8),
                        Text(
                          selectedCategories.map((category) => '#$category').join(' '),
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
            ),
            SizedBox(height: 20),
            // 카테고리 선택 버튼들
            Text(
              '카테고리를 선택하세요 (최대 3개)',
              style: TextStyle(
                fontSize: 18,
                color: widget.isDarkMode ? Colors.white : Colors.black,
              ),
            ),
            SizedBox(height: 10),
            Expanded(
              child: GridView.builder(
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2, // 한 줄에 2개씩 배치
                  mainAxisSpacing: 10, // 세로 간격 최소화
                  crossAxisSpacing: 8, // 가로 간격 최소화
                  childAspectRatio: 3.5, // 가로:세로 비율 설정, 세로 길이 줄이기
                ),
                itemCount: categories.length,
                itemBuilder: (context, index) {
                  final categoryData = categories[index];
                  String category = categoryData['name'];
                  IconData icon = categoryData['icon'];

                  return GestureDetector(
                    onTap: () => _toggleCategory(category),
                    child: Container(
                      decoration: BoxDecoration(
                        color: selectedCategories.contains(category)
                            ? Colors.deepPurple
                            : (widget.isDarkMode ? Colors.white12 : Colors.grey[300]), // 다크 모드에서는 프로필 박스와 동일
                        borderRadius: BorderRadius.circular(10.0),
                      ),
                      child: Center(
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(icon,
                                size: 20,
                                color: selectedCategories.contains(category)
                                    ? Colors.white
                                    : (widget.isDarkMode ? Colors.white : Colors.black)),
                            SizedBox(width: 8),
                            Text(
                              category,
                              style: TextStyle(
                                color: selectedCategories.contains(category)
                                    ? Colors.white
                                    : (widget.isDarkMode ? Colors.white : Colors.black),
                                fontSize: 16,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
            // 다음 버튼 추가
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
                onPressed: _nextStep, // 카테고리가 선택되었을 때만 이동
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
