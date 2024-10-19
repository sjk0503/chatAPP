import 'package:flutter/material.dart';
import 'signup_page.dart'; // signup_page import

class UserProfilePage extends StatefulWidget {
  final Function toggleTheme; // 테마 변경 함수 추가
  final bool isDarkMode; // 다크 모드 상태 추가

  UserProfilePage({required this.toggleTheme, required this.isDarkMode});

  @override
  _UserProfilePageState createState() => _UserProfilePageState();
}

class _UserProfilePageState extends State<UserProfilePage> {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _nicknameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();

  String? _nicknameErrorText;

  bool _validateNickname(String nickname) {
    // 닉네임 유효성 검사를 위한 정규식 (한글, 영어, 숫자 조합 중 하나로 2~8자 이내)
    final regex = RegExp(r'^[가-힣a-zA-Z0-9]{2,8}$');
    return regex.hasMatch(nickname);
  }

  void _checkNickname() {
    setState(() {
      if (_validateNickname(_nicknameController.text)) {
        _nicknameErrorText = '사용가능한 닉네임 입니다 :)';
      } else {
        _nicknameErrorText = '올바르지 않습니다.';
      }
    });
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('오류', style: TextStyle(fontFamily: 'PretendardSemiBold')),
          content: Text(message, style: TextStyle(fontFamily: 'PretendardRegular')),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('확인', style: TextStyle(fontFamily: 'PretendardRegular')),
            ),
          ],
        );
      },
    );
  }

  void _continue() {
    if (_nameController.text.isEmpty) {
      _showErrorDialog('이름을 입력해주세요.');
    } else if (!_validateNickname(_nicknameController.text)) {
      _showErrorDialog('올바르지 않은 닉네임입니다.');
    } else if (_phoneController.text.isEmpty) {
      _showErrorDialog('휴대폰 번호를 입력해주세요.');
    } else if (_emailController.text.isEmpty) {
      _showErrorDialog('이메일 주소를 입력해주세요.');
    } else {
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(
          builder: (context) => SignupPage(
            toggleTheme: widget.toggleTheme, // toggleTheme 전달
            isDarkMode: widget.isDarkMode, // isDarkMode 전달
          ),
        ),
            (Route<dynamic> route) => false,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('회원가입', style: TextStyle(fontFamily: 'PretendardSemiBold')),
        backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // 테마에 따른 색상 변경
      ),
      backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // 테마에 따른 배경색 변경
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              LinearProgressIndicator(
                value: 0.75, // 게이지 바의 진행률 설정 (0.75 = 75%)
                backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.deepPurple),
              ),
              SizedBox(height: 80),
              Text(
                '회원정보 입력',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: widget.isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardExtraBold',
                ),
              ),
              SizedBox(height: 30),
              TextField(
                controller: _nameController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '이름',
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
              TextField(
                controller: _nicknameController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '닉네임',
                  labelStyle: TextStyle(
                    color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                    fontFamily: 'PretendardRegular',
                  ),
                ),
                style: TextStyle(
                  color: widget.isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardRegular',
                ),
                onChanged: (value) => _checkNickname(),
              ),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: () {
                    _checkNickname();
                  },
                  child: Text(
                    '중복확인',
                    style: TextStyle(
                      color: Colors.deepPurple,
                      fontFamily: 'PretendardRegular',
                    ),
                  ),
                ),
              ),
              if (_nicknameErrorText != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: Text(
                    _nicknameErrorText!,
                    style: TextStyle(
                      color: _nicknameErrorText == '사용가능한 닉네임 입니다 :)'
                          ? Colors.lightGreen
                          : Colors.red,
                      fontFamily: 'PretendardRegular',
                    ),
                  ),
                ),
              SizedBox(height: 20),
              TextField(
                controller: _phoneController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '휴대폰 번호',
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
              TextField(
                controller: _emailController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '이메일 주소',
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
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SizedBox(
          width: double.infinity,
          height: 50,
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.deepPurple,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(6.0), // 직사각형 모양으로 변경
              ),
            ),
            onPressed: _continue,
            child: Text(
              '계속하기',
              style: TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'PretendardRegular'),
            ),
          ),
        ),
      ),
    );
  }
}
