import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'birthday_page.dart'; // SignupPage import
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'select_genre_page.dart'; // SelectGenrePage import

class LoginPage extends StatelessWidget {
  final GoogleSignIn _googleSignIn = GoogleSignIn();

  // LoginPage의 생성자에 toggleTheme와 isDarkMode를 추가
  final Function toggleTheme;
  final bool isDarkMode;

  LoginPage({required this.toggleTheme, required this.isDarkMode});

  Future<void> _handleSignIn(BuildContext context) async {
    try {
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      if (googleUser == null) {
        // 사용자가 로그인하지 않고 취소한 경우
        return;
      }
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;

      // googleAuth.accessToken과 googleAuth.idToken을 사용하여 서버 측에서 추가 인증 로직을 수행할 수 있습니다.

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => SelectGenrePage(
            toggleTheme: toggleTheme, // toggleTheme 전달
            isDarkMode: isDarkMode, // isDarkMode 전달
          ),
        ),
      );
    } catch (error) {
      print(error);
    }
  }

  @override
  Widget build(BuildContext context) {
    // 테마 데이터를 가져와서 사용
    final ThemeData theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor, // 테마에 따라 배경색 변경
      resizeToAvoidBottomInset: false, // 키보드가 올라와도 화면이 올라가지 않도록 설정
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Fine Friends',
                  style: theme.textTheme.displayLarge?.copyWith(
                    fontSize: 50,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'DancingScript',
                    color: theme.colorScheme.onBackground, // 글자색 테마에 맞춰 설정
                  ),
                ),
                SizedBox(height: 20),
                _buildTextField(
                  context,
                  labelText: '아이디',
                ),
                SizedBox(height: 20),
                _buildTextField(
                  context,
                  labelText: '비밀번호',
                  obscureText: true,
                ),
                SizedBox(height: 20),
                SizedBox(
                  width: double.infinity,
                  height: 50.0,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: theme.colorScheme.primary, // 버튼 색상을 테마에 맞게 설정
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(6.0),
                      ),
                    ),
                    onPressed: () {
                      Navigator.pushAndRemoveUntil(
                        context,
                        MaterialPageRoute(
                          builder: (context) => SelectGenrePage(
                            toggleTheme: toggleTheme,
                            isDarkMode: isDarkMode,
                          ),
                        ),
                            (Route<dynamic> route) => false,
                      );
                    },
                    child: Text(
                      '로그인',
                      style: theme.textTheme.labelLarge?.copyWith(
                        color: theme.colorScheme.onPrimary, // 버튼 텍스트 색상 테마에 맞춰 설정
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    TextButton(
                      onPressed: () {
                        // 아이디 찾기 로직 추가
                      },
                      child: Text(
                        '아이디 찾기',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: theme.colorScheme.onBackground, // 텍스트 색상 테마에 맞게 설정
                        ),
                      ),
                    ),
                    TextButton(
                      onPressed: () {
                        // 비밀번호 찾기 로직 추가
                      },
                      child: Text(
                        '비밀번호 찾기',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: theme.colorScheme.onBackground, // 텍스트 색상 테마에 맞게 설정
                        ),
                      ),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => BirthdayPage(
                              toggleTheme: toggleTheme,
                              isDarkMode: isDarkMode,
                            ),
                          ),
                        );
                      },
                      child: Text(
                        '회원가입',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: theme.colorScheme.onBackground, // 텍스트 색상 테마에 맞게 설정
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 10),
                SizedBox(height: 15),
                Row(
                  children: <Widget>[
                    Expanded(child: Divider(color: theme.dividerColor)),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 10),
                      child: Text(
                        'SNS 로그인',
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: theme.colorScheme.onBackground, // 텍스트 색상 테마에 맞게 설정
                        ),
                      ),
                    ),
                    Expanded(child: Divider(color: theme.dividerColor)),
                  ],
                ),
                SizedBox(height: 30),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildGoogleButton(context),
                    _buildNaverButton(context),
                    _buildKakaoButton(context),
                    _buildAppleButton(context),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(BuildContext context,
      {required String labelText, bool obscureText = false}) {
    final ThemeData theme = Theme.of(context);

    return TextField(
      decoration: InputDecoration(
        border: OutlineInputBorder(),
        labelText: labelText,
        labelStyle: theme.textTheme.bodyLarge?.copyWith(
          color: theme.textTheme.bodyLarge?.color?.withOpacity(0.6),
        ),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(
            color: theme.textTheme.bodyLarge?.color ?? Colors.black,
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(
            color: Colors.deepPurple,
          ),
        ),
      ),
      obscureText: obscureText,
      style: theme.textTheme.bodyLarge,
    );
  }

  Widget _buildGoogleButton(BuildContext context) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        minimumSize: Size(50, 50),
        shape: CircleBorder(),
      ),
      child: Image.asset(
        'assets/images/googleW.png',
        width: 45,
        height: 45,
        fit: BoxFit.contain,
      ),
      onPressed: () {
        _handleSignIn(context);
      },
    );
  }

  Widget _buildNaverButton(BuildContext context) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Color(0xFF03C75A),
        minimumSize: Size(50, 50),
        shape: CircleBorder(),
      ),
      child: Image.asset(
        'assets/images/naverG.png',
        width: 45,
        height: 45,
        fit: BoxFit.contain,
      ),
      onPressed: () {
        // 네이버 로그인 로직 추가
      },
    );
  }

  Widget _buildKakaoButton(BuildContext context) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Color(0xFFFFE812),
        minimumSize: Size(50, 50),
        shape: CircleBorder(),
      ),
      child: Image.asset(
        'assets/images/kakaoY.png',
        width: 35,
        height: 35,
        fit: BoxFit.contain,
      ),
      onPressed: () {
        // 카카오 로그인 로직 추가
      },
    );
  }

  Widget _buildAppleButton(BuildContext context) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        minimumSize: Size(50, 50),
        shape: CircleBorder(),
      ),
      child: Image.asset(
        'assets/images/appleW.png',
        width: 50,
        height: 50,
        fit: BoxFit.contain,
      ),
      onPressed: () {
        // 애플 로그인 로직 추가
      },
    );
  }
}
