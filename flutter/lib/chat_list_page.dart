import 'package:flutter/material.dart';
import 'chat_page.dart';
import 'friends_list_page.dart';
import 'friend.dart';

class ChatListPage extends StatefulWidget {
  @override
  _ChatListPageState createState() => _ChatListPageState();
}

class _ChatListPageState extends State<ChatListPage> {
  final List<Friend> chatFriends = [
    Friend('이다미', 'assets/images/profile/leedami.png', '이다미의 상태 메시지'),
    Friend('영어쌤', 'assets/images/profile/englishteacher.jpg', '영어쌤의 상태 메시지'),
    Friend('한플리', 'assets/images/profile/music.png', '나랑 음악 들을래?'),
    Friend('고양이', 'assets/images/profile/cat.jpg', '뭘 봐.'),
    Friend('노스트라', 'assets/images/profile/tarot.jpg', '노스트라의 상태 메시지'),
    Friend('김앤장', 'assets/images/profile/lawyer.jpg', '김앤장의 상태 메시지'),
    Friend('신입3', 'assets/images/profile7.png', '신입3의 상태 메시지'),
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
            subtitle: Text(friend.infoController.text),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => ChatPage(character: friend.name,profileImage: friend.profileImage,)),
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
        ],
        onTap: (index) {
          if (index == 0) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => FriendsListPage()),
            );
          }
        },
        currentIndex: 1,
      ),
    );
  }
}
