// lib/friends_list_page.dart

import 'package:flutter/material.dart';
import 'profile_detail_page.dart';  // ProfileDetailPage로 이동
import 'friend.dart';
import 'chat_list_page.dart';  // ChatListPage 추가

class FriendsListPage extends StatefulWidget {
  @override
  _FriendsListPageState createState() => _FriendsListPageState();
}

class _FriendsListPageState extends State<FriendsListPage> with TickerProviderStateMixin {
  final List<Friend> recommendedFriends = [
    Friend('이다미', 'assets/images/profile/leedami.png', '이다미의 상태 메시지'),
    Friend('고양이', 'assets/images/profile/cat.jpg', '뭘 봐.'),
    Friend('영어쌤', 'assets/images/profile/englishteacher.jpg', '영어쌤의 상태 메시지'),
    Friend('미정1', 'assets/images/profile4.png', '미정1의 상태 메시지'),
  ];

  final List<Friend> newFriends = [
    Friend('한플리', 'assets/images/profile/music.png', '나랑 음악 들을래?'),
    Friend('김앤장', 'assets/images/profile/lawyer.jpg', '김앤장의 상태 메시지'),
    Friend('노스트라', 'assets/images/profile/tarot.jpg', '노스트라의 상태 메시지'),
  ];

  final List<Friend> popularFriends = [
    Friend('인기 친구1', 'assets/images/profile5.png', '인기 친구1의 상태 메시지'),
    Friend('인기 친구2', 'assets/images/profile6.png', '인기 친구2의 상태 메시지'),
    Friend('인기 친구3', 'assets/images/profile7.png', '인기 친구3의 상태 메시지'),
    Friend('인기 친구4', 'assets/images/profile8.png', '인기 친구4의 상태 메시지'),
  ];

  final List<Friend> rankingFriends = [
    Friend('랭킹1', 'assets/images/profile9.png', '랭킹1의 상태 메시지'),
    Friend('랭킹2', 'assets/images/profile10.png', '랭킹2의 상태 메시지'),
    Friend('랭킹3', 'assets/images/profile11.png', '랭킹3의 상태 메시지'),
  ];

  final List<Friend> moreFriends = [
    Friend('추가 친구1', 'assets/images/profile9.png', '추가 친구1의 상태 메시지'),
    Friend('추가 친구2', 'assets/images/profile10.png', '추가 친구2의 상태 메시지'),
    Friend('추가 친구3', 'assets/images/profile11.png', '추가 친구3의 상태 메시지'),
  ];

  final Map<String, List<Friend>> categoryFriends = {
    '영화': [
      Friend('영화 친구1', 'assets/images/profile9.png', '영화 친구1의 상태 메시지'),
      Friend('영화 친구2', 'assets/images/profile10.png', '영화 친구2의 상태 메시지'),
      Friend('영화 친구3', 'assets/images/profile11.png', '영화 친구3의 상태 메시지'),
    ],
    '애니메이션': [
      Friend('애니메이션 친구1', 'assets/images/profile12.png', '애니메이션 친구1의 상태 메시지'),
      Friend('애니메이션 친구2', 'assets/images/profile13.png', '애니메이션 친구2의 상태 메시지'),
    ],
    '드라마': [
      Friend('드라마 친구1', 'assets/images/profile14.png', '드라마 친구1의 상태 메시지'),
      Friend('드라마 친구2', 'assets/images/profile15.png', '드라마 친구2의 상태 메시지'),
    ],
    '회화': [
      Friend('회화 친구1', 'assets/images/profile16.png', '회화 친구1의 상태 메시지'),
      Friend('회화 친구2', 'assets/images/profile17.png', '회화 친구2의 상태 메시지'),
    ],
  };

  TextEditingController _searchController = TextEditingController();
  List<Friend> _searchResults = [];
  bool _isSearching = false;
  late TabController _mainTabController;
  late TabController _categoryTabController;

  @override
  void initState() {
    super.initState();
    _mainTabController = TabController(length: 3, vsync: this);
    _categoryTabController = TabController(length: categoryFriends.keys.length + 1, vsync: this);
    _mainTabController.addListener(_handleTabSelection);
  }

  void _handleTabSelection() {
    setState(() {
      _searchController.clear();
      _searchResults.clear();
    });
  }

  void _searchFriends(String query) {
    List<Friend> currentList;
    if (_mainTabController.index == 0) {
      currentList = recommendedFriends + newFriends;
    } else if (_mainTabController.index == 1) {
      currentList = popularFriends + rankingFriends;
    } else {
      String category = _categoryTabController.index == 0
          ? '전체'
          : categoryFriends.keys.elementAt(_categoryTabController.index - 1);
      currentList = category == '전체'
          ? categoryFriends.values.expand((friends) => friends).toList()
          : categoryFriends[category]!;
    }

    setState(() {
      _searchResults = currentList.where((friend) => friend.name.contains(query)).toList();
    });
  }

  @override
  void dispose() {
    _mainTabController.dispose();
    _categoryTabController.dispose();
    _searchController.dispose();
    recommendedFriends.forEach((friend) => friend.infoController.dispose());
    newFriends.forEach((friend) => friend.infoController.dispose());
    popularFriends.forEach((friend) => friend.infoController.dispose());
    rankingFriends.forEach((friend) => friend.infoController.dispose());
    moreFriends.forEach((friend) => friend.infoController.dispose());
    categoryFriends.values
        .expand((friends) => friends)
        .forEach((friend) => friend.infoController.dispose());
    super.dispose();
  }

  Widget _buildSearchResults() {
    return ListView.builder(
      itemCount: _searchResults.length,
      itemBuilder: (context, index) {
        final friend = _searchResults[index];
        return ListTile(
          leading: CircleAvatar(
            backgroundImage: AssetImage(friend.profileImage),
            radius: 25,
          ),
          title: Text(
            friend.name,
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          subtitle: Text(friend.infoController.text),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ProfileDetailPage(friend: friend),
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false, // 뒤로 가기 버튼 제거
        title: _isSearching
            ? TextField(
          controller: _searchController,
          decoration: InputDecoration(
            hintText: '친구 검색',
            border: InputBorder.none,
          ),
          onChanged: _searchFriends,
          autofocus: true,
        )
            : Text('친구 목록'),
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
        bottom: _mainTabController.index == 2
            ? PreferredSize(
          preferredSize: Size.fromHeight(kToolbarHeight * 2),
          child: Column(
            children: [
              TabBar(
                controller: _mainTabController,
                tabs: [
                  Tab(text: '추천 친구'),
                  Tab(text: '인기순 친구'),
                  Tab(text: '카테고리'),
                ],
              ),
              TabBar(
                controller: _categoryTabController,
                isScrollable: true,
                tabs: [
                  Tab(text: '전체'),
                  ...categoryFriends.keys.map((category) => Tab(text: category)).toList(),
                ],
              ),
            ],
          ),
        )
            : TabBar(
          controller: _mainTabController,
          tabs: [
            Tab(text: '추천 친구'),
            Tab(text: '인기순 친구'),
            Tab(text: '카테고리'),
          ],
        ),
      ),
      body: _isSearching
          ? _buildSearchResults()
          : _mainTabController.index == 2
          ? TabBarView(
        controller: _categoryTabController,
        children: [
          _buildCategoryFriendsList(
            categoryFriends.values.expand((friends) => friends).toList(),
          ),
          ...categoryFriends.keys.map((category) {
            return _buildCategoryFriendsList(categoryFriends[category]!);
          }).toList(),
        ],
      )
          : TabBarView(
        controller: _mainTabController,
        children: [
          SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildHorizontalFriendList(recommendedFriends, '오늘의 추천 친구'),
                _buildHorizontalFriendList(newFriends, '신입 인사드립니다. (꾸벅)'),
                _buildHorizontalFriendList(recommendedFriends, '요즘 뜨는 친구'),
              ],
            ),
          ),
          SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildHorizontalFriendList(popularFriends, '인기순 친구'),
                _buildHorizontalFriendList(rankingFriends, '지금 뜨는 랭킹 캐릭터'),
              ],
            ),
          ),
          Center(child: Text('카테고리를 선택하세요')),
        ],
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
          if (index == 1) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => ChatListPage()),
            );
          }
        },
        currentIndex: 0,
      ),
    );
  }

  TextStyle titleStyle = TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white);
  TextStyle nameStyle = TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white);
  TextStyle infoStyle = TextStyle(fontSize: 14, color: Colors.grey);

  Widget _buildHorizontalFriendList(List<Friend> friends, String title) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text(
            title,
            style: titleStyle,
          ),
        ),
        Container(
          height: 250, // 높이를 적절히 조절
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: friends.length,
            itemBuilder: (context, index) {
              return GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ProfileDetailPage(friend: friends[index]), // ProfileDetailPage로 이동
                    ),
                  );
                },
                child: Container(
                  width: 150, // 너비를 적절히 조절
                  margin: EdgeInsets.symmetric(horizontal: 8.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(16.0), // 둥근 모서리 정도를 조절
                        child: Image.asset(
                          friends[index].profileImage,
                          width: 150, // 너비를 조절하여 이미지를 더 크게
                          height: 150, // 높이를 조절하여 이미지를 더 크게
                          fit: BoxFit.cover,
                        ),
                      ),
                      SizedBox(height: 8.0),
                      Text(
                        friends[index].name,
                        overflow: TextOverflow.ellipsis,
                        textAlign: TextAlign.center,
                        style: nameStyle,
                      ),
                      SizedBox(height: 4.0),
                      Text(
                        friends[index].infoController.text,
                        overflow: TextOverflow.ellipsis,
                        textAlign: TextAlign.center,
                        style: infoStyle,
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildCategoryFriendsList(List<Friend> friends) {
    return ListView(
      children: friends
          .map(
            (friend) => ListTile(
          leading: CircleAvatar(
            backgroundImage: AssetImage(friend.profileImage),
            radius: 25, // 카테고리 친구들의 프로필 이미지를 동그랗게 유지
          ),
          title: Text(
            friend.name,
            style: nameStyle,
          ),
          subtitle: Text(
            friend.infoController.text,
            style: infoStyle,
          ),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ProfileDetailPage(friend: friend), // ProfileDetailPage로 이동
              ),
            );
          },
        ),
      )
          .toList(),
    );
  }
}
