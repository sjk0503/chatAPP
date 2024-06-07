import 'package:flutter/material.dart';

class Friend {
  final String name;
  final String profileImage;
  final TextEditingController infoController;

  Friend(this.name, this.profileImage, String info)
      : infoController = TextEditingController(text: info);
}
