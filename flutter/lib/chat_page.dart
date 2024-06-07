import 'dart:convert';
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
  final String _apiKey = 'OPENAI_API_KEY'; // 여기에 OpenAI API 키를 입력.

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
    }
  }

  Future<void> _fetchReply(String message) async {
    final url = Uri.parse('https://api.openai.com/v1/chat/completions');
    final headers = {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer $_apiKey',
    };
    final body = jsonEncode({
      'model': 'gpt-3.5-turbo',
      'messages': [
        {'role': 'system', 'content': 'You are chatting with a user.'},
        {'role': 'user', 'content': message},
      ],
    });

    try {
      final response = await http.post(url, headers: headers, body: body);

      if (response.statusCode == 200) {
        final data = jsonDecode(utf8.decode(response.bodyBytes));
        final reply = data['choices'][0]['message']['content'];
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
