import 'package:flutter/material.dart';
import 'chat_page.dart';
import 'friend.dart';

class ProfileDetailPage extends StatelessWidget {
  final Friend friend;

  ProfileDetailPage({required this.friend});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(friend.name),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.asset(
            friend.profileImage,
            width: double.infinity,
            height: MediaQuery.of(context).size.height / 2,
            fit: BoxFit.cover,
          ),
          SizedBox(height: 16.0),
          Text(
            friend.name,
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 8.0),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Text(
              friend.infoController.text,
              style: TextStyle(fontSize: 16, color: Colors.grey),
              textAlign: TextAlign.center,
            ),
          ),
          Spacer(),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ElevatedButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ChatPage(character: friend.name, profileImage: friend.profileImage,),
                  ),
                );
              },
              child: Text('채팅 시작하기'),
            ),
          ),
        ],
      ),
    );
  }
}
