import 'package:flutter/material.dart';
import 'login.dart'; // 로그인 페이지 import
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class SignupPage extends StatelessWidget {
  // 생성자에 매개변수 추가
  final Function toggleTheme;
  final bool isDarkMode;

  SignupPage({required this.toggleTheme, required this.isDarkMode});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: isDarkMode ? Colors.black : Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Container(
                height: 85.0,
                color: isDarkMode ? Colors.black : Colors.white,
                alignment: Alignment.centerLeft,
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
              ),
              // 게이지바
              LinearProgressIndicator(
                value: 1.0, // 게이지바 진행 상태 (회원가입 완료 상태이므로 100%)
                backgroundColor: isDarkMode ? Colors.white38 : Colors.black38,
                color: Colors.deepPurple,
              ),
              SizedBox(height: 170), // 게이지바와 콘텐츠 사이의 간격
              FaIcon(
                FontAwesomeIcons.checkCircle, // 여기서 solidCircleCheck 대신 checkCircle 사용
                color: Colors.deepPurple,
                size: 80,
              ),
              SizedBox(height: 20),
              Text(
                '회원가입 완료!',
                style: TextStyle(
                  fontSize: 36,
                  fontWeight: FontWeight.bold,
                  color: isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardExtraBold',
                ),
              ),
              SizedBox(height: 10),
              Text(
                '파인 프렌즈 회원이 되신 것을 환영합니다!',
                style: TextStyle(
                  fontSize: 22,
                  color: isDarkMode ? Colors.white : Colors.black,
                  fontFamily: 'PretendardSemiBold',
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 10),
              Text(
                '지금 바로 다미를 만나보세요!',
                style: TextStyle(
                  fontSize: 15,
                  color: isDarkMode ? Colors.white38 : Colors.black38,
                  fontFamily: 'PretendardRegular',
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 40), // 콘텐츠와 버튼 사이의 간격
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(6.0), // 직사각형 모양으로 변경
                    ),
                  ),
                  onPressed: () {
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(
                        builder: (context) => LoginPage(
                          toggleTheme: toggleTheme, // toggleTheme 전달
                          isDarkMode: isDarkMode, // isDarkMode 전달
                        ),
                      ),
                          (Route<dynamic> route) => false,
                    );
                  },
                  child: Text(
                    '로그인하러 가기',
                    style: TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'PretendardRegular'),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
