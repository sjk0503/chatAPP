# Database
## 선택한 DB
> DB는 AWS의 RDS(MySQL)로 구축하였다.
### 선택 이유
> AWS 프리티어 내에서 테스트하기 위함 -> 추후 속도 개선을 위해 변경할 가능성 있음
## ERD
<img width="813" alt="스크린샷 2024-06-08 오후 9 51 19" src="https://github.com/sjk0503/chatAPP/assets/108213769/d8973dc3-cfda-425b-81d3-5157cccfa4ac">

## 진행 상황
+ Lambda 함수와 DB 연동, 테스트 완료
+ 각 테이블 생성 완료
+ 회원가입 시, thread id를 발급하여 db에 저장하기 테스트 완료
+ 대화 내용 실시간 저장 테스트 완료

## 예정 상황
+ 현재 dami 캐릭터 db만 구현한 상태이므로, 다른 캐릭터 구현 시 다른 테이블 생성 예정
