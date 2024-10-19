import 'package:flutter/material.dart';
import 'chat_page.dart'; // ChatPage import 추가
import 'friend.dart'; // Friend 모델 import

class DamiProfile extends StatefulWidget {
  final Function toggleTheme;
  final bool isDarkMode;
  final Friend friend;

  DamiProfile({
    required this.toggleTheme,
    required this.isDarkMode,
    required this.friend,
  });

  @override
  _DamiProfileState createState() => _DamiProfileState();
}

class _DamiProfileState extends State<DamiProfile> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          '${widget.friend.name} 프로필',
          style: TextStyle(fontFamily: 'PretendardSemiBold'),
        ),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
            width: double.infinity,
            height: MediaQuery.of(context).size.height * 0.4,
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage(widget.friend.profileImage),
                fit: BoxFit.cover,
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(top: 16.0, left: 16.0, right: 16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  widget.friend.name,
                  style: TextStyle(
                    fontSize: 24,
                    fontFamily: 'PretendardSemiBold',
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  widget.friend.statusMessage,
                  style: TextStyle(
                    fontSize: 16,
                    fontFamily: 'PretendardRegular',
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
          Spacer(),
          Padding(
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
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ChatPage(
                        character: widget.friend.name,
                        profileImage: widget.friend.profileImage,
                        toggleTheme: widget.toggleTheme,
                        isDarkMode: widget.isDarkMode,
                        friend: widget.friend,
                      ),
                    ),
                  );
                },
                child: Text(
                  '채팅하기',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.white,
                    fontFamily: 'PretendardRegular',
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
