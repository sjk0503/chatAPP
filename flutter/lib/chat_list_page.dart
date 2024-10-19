import 'package:flutter/material.dart';
import 'chat_page.dart';
import 'friends_list_page.dart';
import 'friend.dart';
import 'setting_page.dart'; // SettingPage import 추가

class ChatListPage extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;

  ChatListPage({required this.toggleTheme, required this.isDarkMode});

  @override
  _ChatListPageState createState() => _ChatListPageState();
}

class _ChatListPageState extends State<ChatListPage> {
  final List<Friend> chatFriends = [
    Friend(name: '이다미', profileImage: 'assets/images/profile/leedami.png', statusMessage: '이다미의 상태 메시지'),
    Friend(name: '영어쌤', profileImage: 'assets/images/profile/englishteacher.jpg', statusMessage: '영어쌤의 상태 메시지'),
    Friend(name: '한플리', profileImage: 'assets/images/profile/music.png', statusMessage: '나랑 음악 들을래?'),
    Friend(name: '고양이', profileImage: 'assets/images/profile/cat.jpg', statusMessage: '뭘 봐.'),
    Friend(name: '노스트라', profileImage: 'assets/images/profile/tarot.jpg', statusMessage: '노스트라의 상태 메시지'),
    Friend(name: '김앤장', profileImage: 'assets/images/profile/lawyer.jpg', statusMessage: '김앤장의 상태 메시지'),
    Friend(name: '신입', profileImage: 'assets/images/profile7.png', statusMessage: '신입의 상태 메시지'),
  ];

  TextEditingController _searchController = TextEditingController();
  List<Friend> _searchResults = [];
  bool _isSearching = false;

  void _searchChats(String query) {
    setState(() {
      _searchResults = chatFriends.where((friend) => friend.name.contains(query)).toList();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: _isSearching
            ? TextField(
          controller: _searchController,
          decoration: InputDecoration(
            hintText: '채팅 검색',
            border: InputBorder.none,
          ),
          onChanged: _searchChats,
          autofocus: true,
        )
            : Text('채팅 목록'),
        actions: [
          IconButton(
            icon: Icon(_isSearching ? Icons.close : Icons.search),
            onPressed: () {
              setState(() {
                _isSearching = !_isSearching;
                if (!_isSearching) {
                  _searchController.clear();
                  _searchResults.clear();
                }
              });
            },
          ),
        ],
        automaticallyImplyLeading: false, // 뒤로 가기 버튼 제거
      ),
      body: ListView.builder(
        itemCount: _isSearching ? _searchResults.length : chatFriends.length,
        itemBuilder: (context, index) {
          final friend = _isSearching ? _searchResults[index] : chatFriends[index];
          return ListTile(
            leading: CircleAvatar(
              backgroundImage: AssetImage(friend.profileImage),
            ),
            title: Text(friend.name),
            subtitle: Text(friend.statusMessage), // statusMessage를 사용
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatPage(
                    character: friend.name,
                    profileImage: friend.profileImage,
                    toggleTheme: widget.toggleTheme, // 추가
                    isDarkMode: widget.isDarkMode,   // 추가
                    friend: friend, // friend 전달
                  ),
                ),
              );
            },
          );
        },
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: '친구',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.chat),
            label: '채팅',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: '설정',
          ),
        ],
        onTap: (index) {
          if (index == 0) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (context) => FriendsListPage(
                  toggleTheme: widget.toggleTheme,
                  isDarkMode: widget.isDarkMode,
                ),
              ),
            );
          } else if (index == 2) { // 설정 아이콘을 눌렀을 때 설정 페이지로 이동
            Navigator.push(
              context, // push 사용으로 변경
              MaterialPageRoute(
                builder: (context) => SettingPage(
                  toggleTheme: widget.toggleTheme,
                  isDarkMode: widget.isDarkMode,
                ),
              ),
            );
          }
        },
        currentIndex: 1,
      ),
    );
  }
}
