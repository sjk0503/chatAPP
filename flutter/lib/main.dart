import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'login.dart'; // 로그인 페이지 import
import 'setting_page.dart'; // setting_page import

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool _isDarkMode = false; // 기본 테마 모드를 설정

  void _toggleTheme() {
    setState(() {
      _isDarkMode = !_isDarkMode; // 테마 모드를 변경
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chat App',
      theme: _isDarkMode ? _darkTheme : _lightTheme, // 테마 설정
      home: HomePage(
        toggleTheme: _toggleTheme, // 테마 변경 함수 전달
        isDarkMode: _isDarkMode, // 현재 테마 모드 전달
      ),
      locale: Locale('ko'), // 한국어로 설정
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ],
      supportedLocales: [
        const Locale('en', 'US'), // 영어
        const Locale('ko', 'KR'), // 한국어
      ],
    );
  }

  // 라이트 테마
  final ThemeData _lightTheme = ThemeData(
    brightness: Brightness.light,
    primarySwatch: Colors.purple,
    scaffoldBackgroundColor: Colors.white, // Scaffold의 기본 배경색을 명시적으로 설정
    colorScheme: ColorScheme.light(
      background: Colors.white, // 기본 배경색 설정
    ),
    textTheme: TextTheme(
      bodyLarge: TextStyle(color: Colors.black), // bodyText1을 bodyLarge로 수정
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.purple, // primary 대신 backgroundColor 사용
        foregroundColor: Colors.white, // 버튼의 텍스트 색상 설정
      ),
    ),
  );

  // 다크 테마
  final ThemeData _darkTheme = ThemeData(
    brightness: Brightness.dark,
    primarySwatch: Colors.purple,
    scaffoldBackgroundColor: Color(0xFF121212), // Scaffold의 기본 배경색을 약간 밝은 검은색으로 설정
    colorScheme: ColorScheme.dark(
      background: Color(0xFF121212), // 기본 배경색 설정
    ),
    textTheme: TextTheme(
      bodyLarge: TextStyle(color: Colors.white), // bodyText1을 bodyLarge로 수정
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.purple, // primary 대신 backgroundColor 사용
        foregroundColor: Colors.white, // 버튼의 텍스트 색상 설정
      ),
    ),
  );
}

class HomePage extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;

  HomePage({required this.toggleTheme, required this.isDarkMode});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  void initState() {
    super.initState();
    _navigateToLogin();
  }

  _navigateToLogin() async {
    await Future.delayed(Duration(seconds: 3), () {}); // 로딩 시간 추가
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => LoginPage(
          toggleTheme: widget.toggleTheme,
          isDarkMode: widget.isDarkMode,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: widget.isDarkMode ? Color(0xFF121212) : Colors.white, // 테마에 따라 Scaffold 배경색 변경
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset('assets/images/logo4.png'),
            SizedBox(height: 20),
            CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Colors.purple), // 프로그래스바 색상 설정
            ),
          ],
        ),
      ),
    );
  }
}
