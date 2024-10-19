import 'dart:convert'; // JSON 처리 라이브러리
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart'; // 시간 형식을 위해 필요
import 'package:shared_preferences/shared_preferences.dart';
import 'dami_profile.dart'; // DamiProfile 페이지 import
import 'friend.dart'; // Friend 모델 import

class ChatPage extends StatefulWidget {
  final String character;
  final String profileImage;
  final Function toggleTheme; // 매개변수 추가
  final bool isDarkMode; // 매개변수 추가
  final Friend friend; // Friend 매개변수 추가

  ChatPage({
    required this.character,
    required this.profileImage,
    required this.toggleTheme,
    required this.isDarkMode,
    required this.friend, // Friend 매개변수 추가
  });

  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> with TickerProviderStateMixin {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  final String _apiUrl = 'https://3i8lrr8hcj.execute-api.eu-north-1.amazonaws.com/dami/gpt';
  final ScrollController _scrollController = ScrollController();
  String _searchQuery = '';
  bool _isSearching = false;
  bool _isLoading = false;

  late AnimationController _animationController;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _loadMessages();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    )..repeat();
    _animation = Tween(begin: 0.0, end: 1.0).animate(_animationController);
  }

  @override
  void dispose() {
    _animationController.dispose();
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      final time = DateFormat('HH:mm').format(DateTime.now().toLocal()); // 시간을 형식화
      setState(() {
        _messages.add({
          'sender': 'user',
          'text': _controller.text,
          'time': time,
        });
        _isLoading = true;
      });
      _saveMessages();
      _fetchReply(_controller.text);
      _controller.clear();
      _scrollToBottom();
    }
  }

  Future<void> _fetchReply(String message) async {
    final url = Uri.parse(_apiUrl);
    final headers = {
      'Content-Type': 'application/json; charset=UTF-8',
    };
    final body = jsonEncode({
      'user_input': message,
    });

    try {
      final response = await http.post(url, headers: headers, body: body);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print("API 응답 데이터: $data"); // API 응답 데이터 출력 (디버깅용)

        // data['body']는 평범한 문자열로
        final reply = data['body'];
        final time = DateFormat('HH:mm').format(DateTime.now().toLocal()); // 시간을 형식화

        setState(() {
          _messages.add({
            'sender': 'gpt',
            'text': reply,
            'time': time,
          });
          _isLoading = false;
        });
        _saveMessages();
        _scrollToBottom();
      } else {
        setState(() {
          _messages.add({'sender': 'gpt', 'text': 'Error: Unable to fetch reply.', 'time': ''});
          _isLoading = false;
        });
        print('Failed to load response: ${response.body}');
      }
    } catch (e) {
      setState(() {
        _messages.add({'sender': 'gpt', 'text': 'Error: Unable to fetch reply.', 'time': ''});
        _isLoading = false;
      });
      print('Error: $e');
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 100),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _startSearch() {
    ModalRoute.of(context)
        ?.addLocalHistoryEntry(LocalHistoryEntry(onRemove: _stopSearch));

    setState(() {
      _isSearching = true;
    });
  }

  void _stopSearch() {
    setState(() {
      _isSearching = false;
      _searchQuery = '';
    });
  }

  void _updateSearchQuery(String newQuery) {
    setState(() {
      _searchQuery = newQuery;
    });
  }

  Future<void> _saveMessages() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String messagesJson = jsonEncode(_messages);
    prefs.setString('chat_messages', messagesJson);
  }

  Future<void> _loadMessages() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? messagesJson = prefs.getString('chat_messages');
    if (messagesJson != null) {
      setState(() {
        _messages.addAll(List<Map<String, dynamic>>.from(jsonDecode(messagesJson)));
      });
      // 마지막 대화가 보이도록 스크롤 위치 설정
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _scrollToBottom();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final filteredMessages = _searchQuery.isEmpty
        ? _messages
        : _messages.where((message) {
      return message['text']
          .toLowerCase()
          .contains(_searchQuery.toLowerCase());
    }).toList();

    return Scaffold(
      appBar: AppBar(
        title: _isSearching
            ? TextField(
          onChanged: _updateSearchQuery,
          autofocus: true,
          decoration: InputDecoration(
            hintText: '검색...',
            hintStyle: TextStyle(
              fontFamily: 'PretendardRegular',
            ),
          ),
          style: TextStyle(
            fontFamily: 'PretendardRegular',
          ),
        )
            : Text(
          '${widget.character}',
          style: TextStyle(
            fontFamily: 'PretendardSemiBold',
          ),
        ),
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (context) => DamiProfile(
                  toggleTheme: widget.toggleTheme, // 매개변수 전달
                  isDarkMode: widget.isDarkMode, // 매개변수 전달
                  friend: widget.friend, // friend 매개변수 전달
                ),
              ),
            );
          },
        ),
        actions: [
          if (!_isSearching)
            IconButton(
              icon: Icon(Icons.search),
              onPressed: _startSearch,
            )
          else
            IconButton(
              icon: Icon(Icons.close),
              onPressed: _stopSearch,
            ),
          Builder(
            builder: (context) {
              return IconButton(
                icon: Icon(Icons.menu), // 가로 막대기 3개 아이콘
                onPressed: () {
                  Scaffold.of(context).openEndDrawer(); // 오른쪽 서랍 열기
                },
              );
            },
          ),
        ],
      ),
      endDrawer: Container(
        width: MediaQuery.of(context).size.width * 0.85, // 서랍 너비 설정 (화면 너비의 85%)
        child: Drawer(
          child: ListView(
            padding: EdgeInsets.zero,
            children: <Widget>[
              SizedBox(
                height: 150, // DrawerHeader 높이 설정
                child: DrawerHeader(
                  decoration: BoxDecoration(
                    color: Colors.deepPurple[200],
                  ),
                  child: Text(
                    '채팅방 서랍',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 24,
                      fontFamily: 'PretendardSemiBold',
                    ),
                  ),

                ),
              ),
              ListTile(
                leading: Icon(Icons.image),
                title: Text(
                  '사진',
                  style: TextStyle(
                    fontFamily: 'PretendardRegular',
                  ),
                ),
                onTap: () {
                  // 채팅방 1으로 이동
                },
              ),
              ListTile(
                leading: Icon(Icons.event),
                title: Text(
                  '이벤트',
                  style: TextStyle(
                    fontFamily: 'PretendardRegular',
                  ),
                ),
                onTap: () {
                  // 채팅방 2으로 이동
                },
              ),
              // 다른 채팅방 항목 추가 가능
            ],
          ),
        ),
      ),
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                itemCount: filteredMessages.length + (_isLoading ? 1 : 0),
                itemBuilder: (context, index) {
                  if (_isLoading && index == filteredMessages.length) {
                    return Padding(
                      padding: const EdgeInsets.symmetric(vertical: 5.0, horizontal: 10.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              CircleAvatar(
                                backgroundImage: AssetImage(widget.profileImage),
                              ),
                              SizedBox(width: 8.0),
                              Text(
                                widget.character,
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontFamily: 'PretendardRegular',
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 5.0),
                          Transform.translate(
                            offset: Offset(20.0, -25.0), // Adjust the x (left/right) and y (up/down) values
                            child: AnimatedBuilder(
                              animation: _animationController,
                              builder: (context, child) {
                                return Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: List.generate(3, (index) {
                                    return Padding(
                                      padding: const EdgeInsets.symmetric(horizontal: 2.0),
                                      child: Opacity(
                                        opacity: (index + 1) / 3 * _animation.value,
                                        child: Text(
                                          '.',
                                          style: TextStyle(
                                            fontSize: 50.0,
                                            color: Colors.grey,
                                          ),
                                        ),
                                      ),
                                    );
                                  }),
                                );
                              },
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  final message = filteredMessages[index];
                  final isUserMessage = message['sender'] == 'user';
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 5.0, horizontal: 10.0),
                    child: Column(
                      crossAxisAlignment: isUserMessage ? CrossAxisAlignment.end : CrossAxisAlignment.start,
                      children: [
                        if (!isUserMessage)
                          Row(
                            children: [
                              CircleAvatar(
                                backgroundImage: AssetImage(widget.profileImage),
                              ),
                              SizedBox(width: 8.0),
                              Text(
                                widget.character,
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontFamily: 'PretendardRegular',
                                ),
                              ),
                            ],
                          ),
                        SizedBox(height: 5.0),
                        Container(
                          decoration: BoxDecoration(
                            color: isUserMessage ? Colors.deepPurple[300] : Colors.grey[800], // 말풍선 색상 뒤에 숫자는 올라갈수록 진해짐
                            borderRadius: BorderRadius.circular(12),
                          ),
                          padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                          child: Text(
                            message['text'] ?? '',
                            style: TextStyle(
                              color: Colors.white,
                              fontFamily: 'PretendardRegular',
                            ),
                          ),
                        ),
                        SizedBox(height: 5.0),
                        Text(
                          message['time'],
                          style: TextStyle(
                            color: Colors.grey,
                            fontSize: 12,
                            fontFamily: 'PretendardRegular',
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      decoration: InputDecoration(
                        hintText: '메세지를 입력하세요.',
                        border: OutlineInputBorder(),
                        hintStyle: TextStyle(
                          fontFamily: 'PretendardRegular',
                        ),
                      ),
                      style: TextStyle(
                        fontFamily: 'PretendardRegular',
                      ),
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  IconButton(
                    icon: Icon(Icons.send, color: Colors.purple[300]),
                    onPressed: _sendMessage,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
