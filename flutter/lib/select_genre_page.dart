import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'dami_profile.dart'; // DamiProfile import
import 'friends_list_page.dart'; // FriendsListPage import

class SelectGenrePage extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;

  SelectGenrePage({required this.toggleTheme, required this.isDarkMode});

  @override
  _SelectGenrePageState createState() => _SelectGenrePageState();
}

class _SelectGenrePageState extends State<SelectGenrePage> {
  final List<Map<String, dynamic>> genres = [
    {'name': '액션', 'icon': Icons.local_fire_department},
    {'name': '코미디', 'icon': Icons.sentiment_satisfied},
    {'name': '드라마', 'icon': Icons.theater_comedy},
    {'name': '판타지', 'icon': Icons.auto_awesome},
    {'name': '공포', 'icon': Icons.bug_report},
    {'name': '미스터리', 'icon': Icons.search},
    {'name': '로맨스', 'icon': Icons.favorite},
    {'name': 'SF', 'icon': Icons.science},
    {'name': '스릴러', 'icon': Icons.flash_on},
    {'name': '오컬트', 'icon': Icons.west},
    {'name': '어드벤처', 'icon': Icons.explore},
    {'name': '애니메이션', 'icon': Icons.animation},
  ];

  final Map<String, double> ratings = {};

  @override
  void initState() {
    super.initState();
    // 초기값 설정
    genres.forEach((genre) {
      ratings[genre['name']] = 0.0;
    });
  }

  void _savePreferences() {
    bool allRated = ratings.values.every((rating) => rating > 0);

    if (allRated) {
      // 모든 장르에 점수를 주었을 때
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => FriendsListPage(
            toggleTheme: widget.toggleTheme,
            isDarkMode: widget.isDarkMode,
          ),
        ),
      );
    } else {
      // 점수를 주지 않은 장르가 있을 때
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text(
              '알림',
              style: TextStyle(fontFamily: 'PretendardSemiBold'),
            ),
            content: Text(
              '점수를 주지 않은 장르는 0점으로 저장됩니다. 그래도 계속하시겠습니까?',
              style: TextStyle(fontFamily: 'PretendardRegular'),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: Text(
                  '돌아가기',
                  style: TextStyle(fontFamily: 'PretendardRegular'),
                ),
              ),
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop(); // 팝업 닫기
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => FriendsListPage(
                        toggleTheme: widget.toggleTheme,
                        isDarkMode: widget.isDarkMode,
                      ),
                    ),
                  );
                },
                child: Text(
                  '계속하기',
                  style: TextStyle(fontFamily: 'PretendardRegular'),
                ),
              ),
            ],
          );
        },
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '장르에 대해 별점을 남겨주세요!',
          style: TextStyle(fontFamily: 'PretendardExtraBold', fontSize: 18),
        ),
        backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // 테마에 따라 AppBar 색상 변경
        iconTheme: IconThemeData(color: widget.isDarkMode ? Colors.white : Colors.black), // 뒤로가기 버튼 색상 변경
        titleTextStyle: TextStyle(color: widget.isDarkMode ? Colors.white : Colors.black), // 제목 텍스트 색상 변경
      ),
      backgroundColor: widget.isDarkMode ? Colors.black : Colors.white, // 테마에 따라 배경색 변경
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView.builder(
          itemCount: genres.length,
          itemBuilder: (context, index) {
            return Card(
              color: widget.isDarkMode ? Colors.grey[900] : Colors.white, // 테마에 따라 카드 색상 변경
              child: ListTile(
                leading: Icon(genres[index]['icon'], color: widget.isDarkMode ? Colors.white : Colors.black),
                title: Text(
                  genres[index]['name'],
                  style: TextStyle(color: widget.isDarkMode ? Colors.white : Colors.black, fontFamily: 'PretendardRegular', fontSize: 18),
                ),
                trailing: RatingBar.builder(
                  initialRating: ratings[genres[index]['name']]!,
                  minRating: 0,
                  direction: Axis.horizontal,
                  allowHalfRating: true,
                  itemCount: 5,
                  itemSize: 34.0,
                  itemPadding: EdgeInsets.symmetric(horizontal: 4.0),
                  itemBuilder: (context, _) => Icon(
                    Icons.star,
                    color: Colors.amber,
                  ),
                  onRatingUpdate: (rating) {
                    setState(() {
                      ratings[genres[index]['name']] = rating;
                    });
                  },
                ),
              ),
            );
          },
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
                borderRadius: BorderRadius.circular(6.0),
              ),
            ),
            onPressed: _savePreferences,
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
