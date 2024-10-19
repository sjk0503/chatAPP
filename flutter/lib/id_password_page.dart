import 'package:flutter/material.dart';
import 'user_profile_page.dart'; // 다음 페이지 import

class IdPasswordPage extends StatefulWidget {
  final Function toggleTheme; // 테마 전환 함수 추가
  final bool isDarkMode; // 다크 모드 상태 추가

  IdPasswordPage({required this.toggleTheme, required this.isDarkMode});

  @override
  _IdPasswordPageState createState() => _IdPasswordPageState();
}

class _IdPasswordPageState extends State<IdPasswordPage> {
  bool _isPasswordVisible1 = false;
  bool _isPasswordVisible2 = false;
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _passwordController1 = TextEditingController();
  final TextEditingController _passwordController2 = TextEditingController();

  String? _idErrorText;
  String? _passwordErrorText1;
  String? _passwordErrorText2;

  bool _validateId(String id) {
    final regex = RegExp(r'^[a-z0-9]{6,12}$');
    return regex.hasMatch(id);
  }

  bool _validatePassword(String password) {
    final regex = RegExp(r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[a-z\d@$!%*?&]{8,12}$');
    return regex.hasMatch(password);
  }

  void _validateInputs() {
    setState(() {
      _idErrorText = _validateId(_idController.text)
          ? '사용가능한 아이디 입니다 :)'
          : '아이디는 소문자 영어와 숫자 조합으로 6~12자 이내여야 합니다.';
      _passwordErrorText1 = _validatePassword(_passwordController1.text)
          ? '사용가능한 비밀번호 입니다 :)'
          : '비밀번호는 소문자 영어, 숫자, 특수문자 조합으로 8~12자 이내여야 합니다.';
      _passwordErrorText2 = (_passwordController1.text == _passwordController2.text)
          ? '비밀번호가 일치합니다 :)'
          : '두 비밀번호가 일치하지 않습니다.';
    });

    if (_idErrorText == '사용가능한 아이디 입니다 :)' &&
        _passwordErrorText1 == '사용가능한 비밀번호 입니다 :)' &&
        _passwordErrorText2 == '비밀번호가 일치합니다 :)') {
      // 모든 입력이 올바르면 다음 페이지로 이동
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => UserProfilePage(
            toggleTheme: widget.toggleTheme, // toggleTheme 전달
            isDarkMode: widget.isDarkMode, // isDarkMode 전달
          ),
        ),
      );
    } else {
      // 입력이 올바르지 않으면 알림창 표시
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text('입력 오류', style: TextStyle(fontFamily: 'PretendardSemiBold')),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (_idErrorText != '사용가능한 아이디 입니다 :)')
                Text(
                  _idErrorText!,
                  style: TextStyle(color: Colors.red, fontFamily: 'PretendardRegular'),
                ),
              if (_passwordErrorText1 != '사용가능한 비밀번호 입니다 :)')
                Text(
                  _passwordErrorText1!,
                  style: TextStyle(color: Colors.red, fontFamily: 'PretendardRegular'),
                ),
              if (_passwordErrorText2 != '비밀번호가 일치합니다 :)')
                Text(
                  _passwordErrorText2!,
                  style: TextStyle(color: Colors.red, fontFamily: 'PretendardRegular'),
                ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('확인', style: TextStyle(fontFamily: 'PretendardRegular')),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('회원가입', style: TextStyle(fontFamily: 'PretendardSemiBold')),
        backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // AppBar 배경색 설정
      ),
      backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // 배경색 설정
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              LinearProgressIndicator(
                value: 0.5, // 게이지바 진행 상태
                backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
                color: Colors.deepPurple,
              ),
              SizedBox(height: 80), // 진행 상태 바와 텍스트 사이 간격 조정
              Text(
                '회원정보 입력',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: widget.isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardExtraBold',
                ),
              ),
              SizedBox(height: 30), // 텍스트와 입력 필드 사이의 간격 조정
              TextField(
                controller: _idController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '아이디',
                  labelStyle: TextStyle(
                    color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                    fontFamily: 'PretendardRegular',
                  ),
                ),
                style: TextStyle(
                  color: widget.isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardRegular',
                ),
                onChanged: (value) {
                  setState(() {
                    _idErrorText = _validateId(value)
                        ? '사용가능한 아이디 입니다 :)'
                        : '아이디는 소문자 영어와 숫자 조합으로 6~12자 이내여야 합니다.';
                  });
                },
              ),
              if (_idErrorText != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: Text(
                    _idErrorText!,
                    style: TextStyle(
                      color: _idErrorText == '사용가능한 아이디 입니다 :)' ? Colors.lightGreen : Colors.red,
                      fontFamily: 'PretendardRegular',
                    ),
                  ),
                ),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: () {
                    // 중복확인 로직 추가
                  },
                  child: Text(
                    '중복확인',
                    style: TextStyle(color: Colors.deepPurple, fontFamily: 'PretendardRegular'),
                  ),
                ),
              ),
              SizedBox(height: 20),
              TextField(
                controller: _passwordController1,
                obscureText: !_isPasswordVisible1,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '비밀번호',
                  labelStyle: TextStyle(
                    color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                    fontFamily: 'PretendardRegular',
                  ),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _isPasswordVisible1 ? Icons.visibility : Icons.visibility_off,
                      color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                    ),
                    onPressed: () {
                      setState(() {
                        _isPasswordVisible1 = !_isPasswordVisible1;
                      });
                    },
                  ),
                ),
                style: TextStyle(
                  color: widget.isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardRegular',
                ),
                onChanged: (value) {
                  setState(() {
                    _passwordErrorText1 = _validatePassword(value)
                        ? '사용가능한 비밀번호 입니다 :)'
                        : '비밀번호는 소문자 영어, 숫자, 특수문자 조합으로 8~12자 이내여야 합니다.';
                  });
                },
              ),
              if (_passwordErrorText1 != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: Text(
                    _passwordErrorText1!,
                    style: TextStyle(
                      color: _passwordErrorText1 == '사용가능한 비밀번호 입니다 :)' ? Colors.lightGreen : Colors.red,
                      fontFamily: 'PretendardRegular',
                    ),
                  ),
                ),
              SizedBox(height: 20),
              TextField(
                controller: _passwordController2,
                obscureText: !_isPasswordVisible2,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: '비밀번호 확인',
                  labelStyle: TextStyle(
                    color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                    fontFamily: 'PretendardRegular',
                  ),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _isPasswordVisible2 ? Icons.visibility : Icons.visibility_off,
                      color: widget.isDarkMode ? Colors.white38 : Colors.black38,
                    ),
                    onPressed: () {
                      setState(() {
                        _isPasswordVisible2 = !_isPasswordVisible2;
                      });
                    },
                  ),
                ),
                style: TextStyle(
                  color: widget.isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardRegular',
                ),
                onChanged: (value) {
                  setState(() {
                    _passwordErrorText2 = (_passwordController1.text == value)
                        ? '비밀번호가 일치합니다 :)'
                        : '두 비밀번호가 일치하지 않습니다.';
                  });
                },
              ),
              if (_passwordErrorText2 != null)
                Padding(
                  padding: const EdgeInsets.only(top: 8.0),
                  child: Text(
                    _passwordErrorText2!,
                    style: TextStyle(
                      color: _passwordErrorText2 == '비밀번호가 일치합니다 :)' ? Colors.lightGreen : Colors.red,
                      fontFamily: 'PretendardRegular',
                    ),
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
              backgroundColor: Colors.deepPurple, // 버튼 배경색 설정
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(6.0), // 직사각형 모양으로 변경
              ),
            ),
            onPressed: _validateInputs,
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
