import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'login.dart'; // 로그인 페이지 import
import 'select_genre_page.dart'; // SelectGenrePage import

class SettingPage extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;

  SettingPage({required this.toggleTheme, required this.isDarkMode});

  @override
  _SettingPageState createState() => _SettingPageState();
}

class _SettingPageState extends State<SettingPage> {
  bool _isDarkMode = false;

  @override
  void initState() {
    super.initState();
    _isDarkMode = widget.isDarkMode; // 초기 테마 상태 설정
  }

  Future<void> _clearChatHistory() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.remove('chat_messages');
  }

  void _toggleTheme() {
    setState(() {
      _isDarkMode = !_isDarkMode; // 현재 페이지의 테마 상태도 업데이트
    });
    widget.toggleTheme(); // 전체 테마를 변경하는 함수 호출
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Padding(
          padding: const EdgeInsets.only(top: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '다미절친', // 닉네임
                    style: TextStyle(
                      fontSize: 25,
                      fontFamily: 'PretendardSemiBold',
                      color: _isDarkMode ? Colors.white : Colors.black, // 테마에 맞춘 글자 색상 변경
                    ),
                  ),
                  SizedBox(height: 4.0),
                  Text(
                    '@dami123', // ID
                    style: TextStyle(
                      fontSize: 15,
                      fontFamily: 'PretendardRegular',
                      color: _isDarkMode ? Colors.white54 : Colors.black54, // 테마에 맞춘 글자 색상 변경
                    ),
                  ),
                ],
              ),
              SizedBox(
                height: 35,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(6.0),
                    ),
                    padding: EdgeInsets.symmetric(horizontal: 16),
                  ),
                  onPressed: () {
                    // 추가 정보 페이지로 이동 가능
                  },
                  child: Text(
                    '내 정보',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.white,
                      fontFamily: 'PretendardRegular',
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        backgroundColor: _isDarkMode ? Colors.black : Colors.white, // 테마에 따른 AppBar 색상 설정
        iconTheme: IconThemeData(
          color: _isDarkMode ? Colors.white : Colors.black, // 아이콘 색상 설정
        ),
      ),
      backgroundColor: _isDarkMode ? Colors.black : Colors.white, // 배경색 설정
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Divider(color: _isDarkMode ? Colors.white38 : Colors.black38),
            SizedBox(height: 20),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => SelectGenrePage(
                      toggleTheme: widget.toggleTheme,
                      isDarkMode: _isDarkMode,
                    ),
                  ),
                );
              },
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  '장르 선호도',
                  style: TextStyle(
                    fontSize: 22,
                    color: _isDarkMode ? Colors.white : Colors.black,
                    fontFamily: 'PretendardSemiBold',
                  ),
                ),
              ),
            ),
            Divider(color: _isDarkMode ? Colors.white38 : Colors.black38),
            TextButton(
              onPressed: () {
                _clearChatHistory();
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('이전 대화 기록이 삭제되었습니다.')),
                );
              },
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  '대화 기록 삭제',
                  style: TextStyle(
                    fontSize: 22,
                    color: _isDarkMode ? Colors.white : Colors.black,
                    fontFamily: 'PretendardSemiBold',
                  ),
                ),
              ),
            ),
            Divider(color: _isDarkMode ? Colors.white38 : Colors.black38),
            ListTile(
              title: Text(
                '테마 전환',
                style: TextStyle(
                  fontSize: 22,
                  color: _isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardSemiBold',
                ),
              ),
              trailing: Switch(
                value: _isDarkMode,
                onChanged: (value) {
                  _toggleTheme(); // 테마 전환 및 현재 페이지 상태 업데이트
                },
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
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(
                      builder: (context) => LoginPage(
                        toggleTheme: widget.toggleTheme,
                        isDarkMode: _isDarkMode,
                      ),
                    ),
                  );
                },
                child: Text(
                  '로그아웃',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.white,
                    fontFamily: 'PretendardRegular',
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
