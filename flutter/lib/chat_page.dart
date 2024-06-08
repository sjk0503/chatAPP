import 'dart:convert'; // JSON 처리 라이브러리
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart'; // 시간 형식을 위해 필요
import 'chat_list_page.dart';

class ChatPage extends StatefulWidget {
  final String character;
  final String profileImage;

  ChatPage({required this.character, required this.profileImage});

  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  final String _apiUrl = 'https://rdsi2vxj2h.execute-api.ap-northeast-2.amazonaws.com/jarvis/gptAPI';
  final ScrollController _scrollController = ScrollController();

  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      final time = DateFormat('HH:mm').format(
        DateTime.now().toUtc().add(Duration(hours: 9)).toLocal(), // 한국 시간(KST)으로 변환
      ); // 시간을 형식화
      setState(() {
        _messages.add({
          'sender': 'user',
          'text': _controller.text,
          'time': time,
        });
      });
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
        final time = DateFormat('HH:mm').format(
          DateTime.now().toUtc().add(Duration(hours: 9)).toLocal(), // 한국 시간(KST)으로 변환
        ); // 시간을 형식화

        setState(() {
          _messages.add({
            'sender': 'gpt',
            'text': reply,
            'time': time,
          });
        });
        _scrollToBottom();
      } else {
        setState(() {
          _messages.add({'sender': 'gpt', 'text': 'Error: Unable to fetch reply.', 'time': ''});
        });
        print('Failed to load response: ${response.body}');
      }
    } catch (e) {
      setState(() {
        _messages.add({'sender': 'gpt', 'text': 'Error: Unable to fetch reply.', 'time': ''});
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

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => ChatListPage()),
        );
        return false;
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text('${widget.character}'),
        ),
        body: Column(
          children: [
            Expanded(
              child: ListView.builder(
                controller: _scrollController,
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  final message = _messages[index];
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
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                        SizedBox(height: 5.0),
                        Container(
                          decoration: BoxDecoration(
                            color: isUserMessage ? Colors.purple[900] : Colors.grey[900], // 말풍선 색상 뒤에 숫자는 올라갈수록 진해짐
                            borderRadius: BorderRadius.circular(12),
                          ),
                          padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                          child: Text(
                            message['text'] ?? '',
                            style: TextStyle(color: Colors.white),
                          ),
                        ),
                        SizedBox(height: 5.0),
                        Text(
                          message['time'],
                          style: TextStyle(color: Colors.grey, fontSize: 12),
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
                      ),
                    ),
                  ),
                  IconButton(
                    icon: Icon(Icons.send),
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
