# [Assignment 1] 에이모 - 게시판 Restfull API 개발

- 팀명 : 1팀 - 쿠티드프리온보딩

- 팀원명 : 구본욱, 이다빈, 김주현



## 적용기술
- flask
- mongodb
- JWT
- bcrypt

## 구현 방법 및 기능
- python언어를 기반으로 Flask Framework를 활용한 게시판 Restfull API 구현하기
- 유저 생성, 인가, 인증 기능 적용

- users앱
  - 회원가입을 통해 bcrypt로 비밀번호 암호화
  - 로그인을 통해 JWT Token 생성
  - 사용자별 인가를 위해 자체 내장된 데코레이터 생성 후 기능별로 jwt_required 부여
  - 로그인/회원가입 unit test 완료
  
- postings앱
  - 게시물 생성, 조회, 수정, 삭제 기능 구현
  - 게시물 상세내용 조회 기능 구현 (pagination 적용)
  - 게시물 검색 기능 구현
  - 게시물 읽힘 수 적용
  
- comments앱
  - 댓글 생성, 조회, 삭제 기능 구현
  - 대댓글 생성, 조회 기능 구현
  - 댓글, 대댓글 조회 기능 pagination 적용
  


## API Documents 

주소 : https://documenter.getpostman.com/view/17922648/UVBznUqp

