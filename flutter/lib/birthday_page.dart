import 'package:flutter/material.dart';
import 'id_password_page.dart'; // 다음 페이지 import
import 'package:flutter/cupertino.dart';

class BirthdayPage extends StatefulWidget {
  final Function toggleTheme; // 테마 전환 함수 추가
  final bool isDarkMode; // 다크 모드 상태 추가

  BirthdayPage({required this.toggleTheme, required this.isDarkMode});

  @override
  _BirthdayPageState createState() => _BirthdayPageState();
}

class _BirthdayPageState extends State<BirthdayPage> {
  int? _selectedYear;
  int? _selectedMonth;
  int? _selectedDay;

  final List<int> years = List<int>.generate(125, (i) => 2024 - i);
  final List<int> months = List<int>.generate(12, (i) => 1 + i);
  final List<int> days = List<int>.generate(31, (i) => 1 + i);

  Future<void> _selectYear(BuildContext context) async {
    await showModalBottomSheet(
      context: context,
      builder: (BuildContext builder) {
        return Container(
          height: MediaQuery.of(context).copyWith().size.height / 3,
          child: CupertinoPicker(
            itemExtent: 32.0,
            onSelectedItemChanged: (int index) {
              setState(() {
                _selectedYear = years[index];
              });
            },
            children: years.map((int year) {
              return Center(child: Text('$year', style: TextStyle(fontFamily: 'PretendardRegular')));
            }).toList(),
          ),
        );
      },
    );
  }

  Future<void> _selectMonth(BuildContext context) async {
    await showModalBottomSheet(
      context: context,
      builder: (BuildContext builder) {
        return Container(
          height: MediaQuery.of(context).copyWith().size.height / 3,
          child: CupertinoPicker(
            itemExtent: 32.0,
            onSelectedItemChanged: (int index) {
              setState(() {
                _selectedMonth = months[index];
              });
            },
            children: months.map((int month) {
              return Center(child: Text('$month', style: TextStyle(fontFamily: 'PretendardRegular')));
            }).toList(),
          ),
        );
      },
    );
  }

  Future<void> _selectDay(BuildContext context) async {
    await showModalBottomSheet(
      context: context,
      builder: (BuildContext builder) {
        return Container(
          height: MediaQuery.of(context).copyWith().size.height / 3,
          child: CupertinoPicker(
            itemExtent: 32.0,
            onSelectedItemChanged: (int index) {
              setState(() {
                _selectedDay = days[index];
              });
            },
            children: days.map((int day) {
              return Center(child: Text('$day', style: TextStyle(fontFamily: 'PretendardRegular')));
            }).toList(),
          ),
        );
      },
    );
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
    if (_selectedYear == null) {
      _showErrorDialog('년도를 선택해주세요.');
    } else if (_selectedMonth == null) {
      _showErrorDialog('월을 선택해주세요.');
    } else if (_selectedDay == null) {
      _showErrorDialog('일을 선택해주세요.');
    } else {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => IdPasswordPage(
            toggleTheme: widget.toggleTheme, // toggleTheme 전달
            isDarkMode: widget.isDarkMode, // isDarkMode 전달
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('회원가입', style: TextStyle(fontFamily: 'PretendardSemiBold')),
        leading: IconButton(
          icon: Icon(Icons.close), // 뒤로가기 버튼을 X 모양으로 변경
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // AppBar 배경색 설정
      ),
      backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // 배경색 설정
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            LinearProgressIndicator(
              value: 0.25, // 게이지 바의 진행률 설정 (0.25 = 25%)
              backgroundColor: widget.isDarkMode ? Colors.white24 : Colors.black26,
              valueColor: AlwaysStoppedAnimation<Color>(Colors.deepPurple),
            ),
            SizedBox(height: 100),
            Text(
              '생년월일을 입력해주세요.',
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: widget.isDarkMode ? Colors.white : Colors.black,
                fontFamily: 'PretendardExtraBold',
              ),
            ),
            SizedBox(height: 20), // 텍스트와 입력 필드 사이의 간격 조정
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Expanded(
                  child: GestureDetector(
                    onTap: () => _selectYear(context),
                    child: AbsorbPointer(
                      child: TextField(
                        controller: TextEditingController(
                          text: _selectedYear == null ? '' : _selectedYear.toString(),
                        ),
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: '년',
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
                    ),
                  ),
                ),
                SizedBox(width: 10),
                Expanded(
                  child: GestureDetector(
                    onTap: () => _selectMonth(context),
                    child: AbsorbPointer(
                      child: TextField(
                        controller: TextEditingController(
                          text: _selectedMonth == null
                              ? ''
                              : _selectedMonth.toString().padLeft(2, '0'),
                        ),
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: '월',
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
                    ),
                  ),
                ),
                SizedBox(width: 10),
                Expanded(
                  child: GestureDetector(
                    onTap: () => _selectDay(context),
                    child: AbsorbPointer(
                      child: TextField(
                        controller: TextEditingController(
                          text: _selectedDay == null
                              ? ''
                              : _selectedDay.toString().padLeft(2, '0'),
                        ),
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: '일',
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
                    ),
                  ),
                ),
              ],
            ),
            Spacer(), // 나머지 공간을 차지하도록 설정
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.deepPurple, // 버튼 배경색 설정
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
          ],
        ),
      ),
    );
  }
}
