import 'package:flutter/material.dart';
import 'friend.dart';
import 'chat_list_page.dart';
import 'dami_profile.dart'; // DamiProfile import
import 'customize_ai_name_page.dart'; // CustomizeAINamePage import
import 'setting_page.dart'; // SettingPage import

class FriendsListPage extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;

  FriendsListPage({required this.toggleTheme, required this.isDarkMode});

  @override
  _FriendsListPageState createState() => _FriendsListPageState();
}

class _FriendsListPageState extends State<FriendsListPage> with TickerProviderStateMixin {
  final List<Friend> recommendedFriends = [
    Friend(name: '이다미', profileImage: 'assets/images/profile/leedami.png', statusMessage: '요즘 볼 영화 없지? 같이 영화 얘기할래? 너의 취향에 맞는 영화 찾아줄게. 우리 같이 즐기자!'),
    Friend(name: '고양이', profileImage: 'assets/images/profile/cat.jpg', statusMessage: '뭘 봐\n 말하는 고양이 처음 봐?'),
    Friend(name: '영어쌤', profileImage: 'assets/images/profile/englishteacher.jpg', statusMessage: '안녕! 여러분의 영어 실력을 함께 키워갈 선생님이에요. 우리 같이 즐겁게 영어 배워봐요!'),
  ];

  final List<Friend> newFriends = [
    Friend(name: '한플리', profileImage: 'assets/images/profile/music.png', statusMessage: '너 또 그 음악 듣고 있냐? 내가 세련된 음악 추천해줄게. 내 추천 믿고 들어봐. 네 귀가 호강할 거야!'),
    Friend(name: '노스트라', profileImage: 'assets/images/profile/tarot.jpg', statusMessage: '미래가 궁금해? 신비로운 타로 카드가 답을 줄 거야. 나와 함께 운명의 비밀을 밝혀보자.'),
    Friend(name: '김앤장', profileImage: 'assets/images/profile/lawyer.jpg', statusMessage: '안녕하세요. 당신의 든든한 법률 파트너입니다. 복잡한 법적 문제, 제가 깔끔하게 해결해드릴게요.'),
  ];

  final List<Friend> hotFriends = [
    Friend(name: '최아나', profileImage: 'assets/images/profile/announcer.jpg', statusMessage: '안녕하세요! 깔끔하고 정확한 뉴스 아나운서 최아나입니다. 가장 빠르고 신뢰할 수 있는 소식을 전해드릴게요.'),
    Friend(name: '임국종', profileImage: 'assets/images/profile/doctor.jpg', statusMessage: '안녕하세요, 환자분. 어디가 불편하신가요? 건강을 위해 최선을 다해 도와드리겠습니다'),
    Friend(name: '백다빈', profileImage: 'assets/images/profile/shop.jpg', statusMessage: '꼴이 그게 뭐야? 진짜 감 떨어졌네. 최신 쇼핑 트렌드? 나한테 배워.'),
  ];

  final List<Friend> popularFriends = [
    Friend(name: '이다미', profileImage: 'assets/images/profile/leedami.png', statusMessage: '요즘 볼 영화 없지? 같이 영화 얘기할래? 너의 취향에 맞는 영화 찾아줄게. 우리 같이 즐기자!'),
    Friend(name: '노스트라', profileImage: 'assets/images/profile/tarot.jpg', statusMessage: '미래가 궁금해? 신비로운 타로 카드가 답을 줄 거야. 나와 함께 운명의 비밀을 밝혀보자.'),
    Friend(name: '한플리', profileImage: 'assets/images/profile/music.png', statusMessage: '너 또 그 음악 듣고 있냐? 내가 세련된 음악 추천해줄게. 내 추천 믿고 들어봐. 네 귀가 호강할 거야!'),
    Friend(name: '고양이', profileImage: 'assets/images/profile/cat.jpg', statusMessage: '뭘 봐\n 말하는 고양이 처음 봐?'),
    Friend(name: '영어쌤', profileImage: 'assets/images/profile/englishteacher.jpg', statusMessage: '안녕! 여러분의 영어 실력을 함께 키워갈 선생님이에요 우리 같이 즐겁게 영어 배워봐요!'),
    Friend(name: '김앤장', profileImage: 'assets/images/profile/lawyer.jpg', statusMessage: '안녕하세요. 당신의 든든한 법률 파트너입니다. 복잡한 법적 문제, 제가 깔끔하게 해결해드릴게요.'),
    Friend(name: '최아나', profileImage: 'assets/images/profile/announcer.jpg', statusMessage: '안녕하세요! 깔끔하고 정확한 뉴스 아나운서 최아나입니다. 가장 빠르고 신뢰할 수 있는 소식을 전해드릴게요.'),
    Friend(name: '임국종', profileImage: 'assets/images/profile/doctor.jpg', statusMessage: '안녕하세요, 환자분. 어디가 불편하신가요? 건강을 위해 최선을 다해 도와드리겠습니다'),
    Friend(name: '백다빈', profileImage: 'assets/images/profile/shop.jpg', statusMessage: '꼴이 그게 뭐야? 진짜 감 떨어졌네. 최신 쇼핑 트렌드? 나한테 배워.'),
  ];

  final List<Friend> rankingFriends = [
    Friend(name: '백다빈', profileImage: 'assets/images/profile/shop.jpg', statusMessage: '꼴이 그게 뭐야? 진짜 감 떨어졌네. 최신 쇼핑 트렌드? 나한테 배워.'),
    Friend(name: '고양이', profileImage: 'assets/images/profile/cat.jpg', statusMessage: '뭘 봐\n 말하는 고양이 처음 봐?'),
    Friend(name: '최아나', profileImage: 'assets/images/profile/announcer.jpg', statusMessage: '안녕하세요! 깔끔하고 정확한 뉴스 아나운서 최아나입니다. 가장 빠르고 신뢰할 수 있는 소식을 전해드릴게요.'),
    Friend(name: '임국종', profileImage: 'assets/images/profile/doctor.jpg', statusMessage: '안녕하세요, 환자분. 어디가 불편하신가요? 건강을 위해 최선을 다해 도와드리겠습니다'),
  ];

  final Map<String, List<Friend>> categoryFriends = {
    '엔터': [
      Friend(name: '이다미', profileImage: 'assets/images/profile/leedami.png', statusMessage: '요즘 볼 영화 없지? 같이 영화 얘기할래? 너의 취향에 맞는 영화 찾아줄게. 우리 같이 즐기자!'),
      Friend(name: '한플리', profileImage: 'assets/images/profile/music.png', statusMessage: '너 또 그 음악 듣고 있냐? 내가 세련된 음악 추천해줄게. 내 추천 믿고 들어봐. 네 귀가 호강할 거야!'),
      Friend(name: '백다빈', profileImage: 'assets/images/profile/shop.jpg', statusMessage: '꼴이 그게 뭐야? 진짜 감 떨어졌네. 최신 쇼핑 트렌드? 나한테 배워.'),
    ],
    '일상생활': [
      Friend(name: '김앤장', profileImage: 'assets/images/profile/lawyer.jpg', statusMessage: '안녕하세요. 당신의 든든한 법률 파트너입니다. 복잡한 법적 문제, 제가 깔끔하게 해결해드릴게요.'),
      Friend(name: '최아나', profileImage: 'assets/images/profile/announcer.jpg', statusMessage: '안녕하세요! 깔끔하고 정확한 뉴스 아나운서 최아나입니다. 가장 빠르고 신뢰할 수 있는 소식을 전해드릴게요.'),
      Friend(name: '임국종', profileImage: 'assets/images/profile/doctor.jpg', statusMessage: '안녕하세요, 환자분. 어디가 불편하신가요? 건강을 위해 최선을 다해 도와드리겠습니다'),
    ],
    '타로 사주 운세': [
      Friend(name: '노스트라', profileImage: 'assets/images/profile/tarot.jpg', statusMessage: '미래가 궁금해? 신비로운 타로 카드가 답을 줄 거야. 나와 함께 운명의 비밀을 밝혀보자.'),
    ],
    '회화': [
      Friend(name: '영어쌤', profileImage: 'assets/images/profile/englishteacher.jpg', statusMessage: '안녕! 여러분의 영어 실력을 함께 키워갈 선생님이에요. 우리 같이 즐겁게 영어 배워봐요!'),
    ],
    '동물': [
      Friend(name: '고양이', profileImage: 'assets/images/profile/cat.jpg', statusMessage: '뭘 봐\n 말하는 고양이 처음 봐?'),
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
      currentList = recommendedFriends + newFriends + hotFriends;
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
            style: _getNameStyle(),
          ),
          subtitle: Text(
            friend.statusMessage,
            style: _getInfoStyle(),
          ),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => DamiProfile(
                  toggleTheme: widget.toggleTheme,
                  isDarkMode: widget.isDarkMode,
                  friend: friend, // friend 정보를 전달
                ),
              ),
            ).then((_) => setState(() {})); // 테마 변경 후 상태 갱신
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
                  Tab(text: '추천'),
                  Tab(text: '랭킹'),
                  Tab(text: '카테고리'),
                ],
              ),
              TabBar(
                controller: _categoryTabController,
                isScrollable: true,
                tabs: [
                  Tab(text: '전체'),
                  ...categoryFriends.keys
                      .map((category) => Tab(text: category))
                      .toList(),
                ],
              ),
            ],
          ),
        )
            : TabBar(
          controller: _mainTabController,
          tabs: [
            Tab(text: '추천'),
            Tab(text: '인기순'),
            Tab(text: '카테고리'),
          ],
        ),
      ),
      body: Stack(
        children: [
          _isSearching
              ? _buildSearchResults()
              : _mainTabController.index == 2
              ? TabBarView(
            controller: _categoryTabController,
            children: [
              _buildCategoryFriendsList(
                categoryFriends.values
                    .expand((friends) => friends)
                    .toList(),
              ),
              ...categoryFriends.keys.map((category) {
                return _buildCategoryFriendsList(
                    categoryFriends[category]!);
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
                    _buildHorizontalFriendList(
                        recommendedFriends, '오늘의 추천 친구'),
                    _buildHorizontalFriendList(
                        newFriends, '신입 인사드립니다. (꾸벅)'),
                    _buildHorizontalFriendList(
                        hotFriends, '요즘 뜨는 친구'),
                  ],
                ),
              ),
              SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildHorizontalFriendList(
                        popularFriends, '인기순 친구'),
                    _buildHorizontalFriendList(
                        rankingFriends, '지금 뜨는 랭킹 캐릭터'),
                  ],
                ),
              ),
              Center(child: Text('카테고리를 선택하세요')),
            ],
          ),
          Positioned(
            bottom: 16,
            right: 16,
            child: FloatingActionButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => CustomizeAINamePage(
                      toggleTheme: widget.toggleTheme,
                      isDarkMode: widget.isDarkMode,
                    ),
                  ),
                ).then((_) => setState(() {})); // 테마 변경 후 상태 갱신
              },
              child: Icon(Icons.edit),
              backgroundColor: Colors.deepPurple[200],
            ),
          ),
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
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: '설정',
          ),
        ],
        onTap: (index) {
          if (index == 1) {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ChatListPage(
                  toggleTheme: widget.toggleTheme,
                  isDarkMode: widget.isDarkMode,
                ),
              ),
            ).then((_) => setState(() {})); // 테마 변경 후 상태 갱신
          } else if (index == 2) {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => SettingPage(
                  toggleTheme: widget.toggleTheme,
                  isDarkMode: widget.isDarkMode,
                ),
              ),
            ).then((_) => setState(() {})); // 테마 변경 후 상태 갱신
          }
        },
        currentIndex: 0,
      ),
    );
  }

  TextStyle _getTitleStyle() {
    return TextStyle(
      fontSize: 20,
      fontWeight: FontWeight.bold,
      color: widget.isDarkMode ? Colors.white : Colors.black,
    );
  }

  TextStyle _getNameStyle() {
    return TextStyle(
      fontSize: 18,
      fontWeight: FontWeight.bold,
      color: widget.isDarkMode ? Colors.white : Colors.black,
    );
  }

  TextStyle _getInfoStyle() {
    return TextStyle(
      fontSize: 14,
      color: widget.isDarkMode ? Colors.grey : Colors.black54,
    );
  }

  Widget _buildHorizontalFriendList(List<Friend> friends, String title) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Text(
            title,
            style: _getTitleStyle(),
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
                      builder: (context) => DamiProfile(
                        friend: friends[index],
                        toggleTheme: widget.toggleTheme,
                        isDarkMode: widget.isDarkMode,
                      ),
                    ),
                  ).then((_) => setState(() {})); // 테마 변경 후 상태 갱신
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
                        style: _getNameStyle(),
                      ),
                      SizedBox(height: 4.0),
                      Text(
                        friends[index].statusMessage,
                        maxLines: 2, // 상태메세지 2줄
                        overflow: TextOverflow.ellipsis, // 2줄 넘기면 줄임표로 마무리
                        textAlign: TextAlign.center,
                        style: _getInfoStyle(),
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
            style: _getNameStyle(),
          ),
          subtitle: Text(
            friend.statusMessage,
            maxLines: 1, // 상태메세지를 1줄로 제한
            overflow: TextOverflow.ellipsis, // 넘치면 줄임표로 마무리
            style: _getInfoStyle(),
          ),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => DamiProfile(
                  friend: friend,
                  toggleTheme: widget.toggleTheme,
                  isDarkMode: widget.isDarkMode,
                ),
              ),
            ).then((_) => setState(() {})); // 테마 변경 후 상태 갱신
          },
        ),
      )
          .toList(),
    );
  }
}
