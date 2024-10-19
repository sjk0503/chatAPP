// lib/friend.dart
import 'package:flutter/material.dart';

class Friend {
  final String name;
  final String profileImage;
  final String statusMessage; // 상태 메시지 필드 추가

  Friend({
    required this.name,
    required this.profileImage,
    required this.statusMessage,
  });
}
