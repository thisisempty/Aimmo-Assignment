# [Assignment 1] 에이모 - 게시판 Restfull API 개발

- 팀명 : 1팀 - 쿠티드프리온보딩

## 팀 역할분배

- 구본욱 : 게시글 CRUD 
- 이다빈 : 로그인/회원가입, 배포
- 김주현 : 댓글,대댓글 


## 적용기술
- python, flask, mongodb, JWT, bcrypt, AWS EC2, atlas

## 구현 방법 및 기능
- python언어를 기반으로 Flask Framework를 활용한 게시판 Restfull API 구현하기


## 로그인 / 회원가입

### 1. 회원가입

```POST/users/signup```
  - 회원가입을 통해 bcrypt로 비밀번호 암호화
  - email, password 유효성 검사하여 맞지 않으면 INVALID_EMAIL, INVALID_PASSWORD 반환
  
### Request
```
curl --location --request POST 'http://127.0.0.1:5000/users/signup' \
--data-raw '{
    "email" : "newhyun@naver.com",
    "password" : "avdce!!a2135",
    "nickname" : "newhyun"
}'
```

### Response
```
{
  "message": "SUCCESS"
}
```
### 2. 로그인
```GET/users/signin```
  - 로그인을 통해 JWT Token 생성
  - 같은 이메일 유저 로그인 불가
  - 로그인/회원가입 unit test 완료
  
### Request
```
curl --location --request GET 'http://127.0.0.1:5000/users/signin' \
--data-raw '{
    "email" : "newhyun@naver.com",
    "password" : "avdce!!a2135",
    "nickname" : "newhyun"
}'
```

### Response
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTg4NjI2MywianRpIjoiZjBhMWU3NjEtMWYzOS00YzM3LWEwZDctZmU4YjI1ODczZGI3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYxODE4ZmM1YWE5ZWFjNjc4Mjc5NjcyOCIsIm5iZiI6MTYzNTg4NjI2MywiZXhwIjoxNjM2NDkxMDYzfQ.godXBLO-K8Lk3Kz8FwdgiwBxiFn1KVgKFIcqA1uQ6uI"
}
```

## 게시글 관리

### 1. 게시글 생성
```POST/post/```
  - 사용자별 인가를 위해 자체 내장된 데코레이터 생성 후 기능별로 jwt_required 부여
  - post_id와 일치하는 게시글이 없으면 POST_DOES_NOT_EXIST ERROR 반환
  - 보내진 정보를 기반으로 게시글 생성

### Request
```
curl --location --request POST 'http://127.0.0.1:5000/post' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTg4NjI2MywianRpIjoiZjBhMWU3NjEtMWYzOS00YzM3LWEwZDctZmU4YjI1ODczZGI3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYxODE4ZmM1YWE5ZWFjNjc4Mjc5NjcyOCIsIm5iZiI6MTYzNTg4NjI2MywiZXhwIjoxNjM2NDkxMDYzfQ.godXBLO-K8Lk3Kz8FwdgiwBxiFn1KVgKFIcqA1uQ6uI' \
--data-raw '{
    "user" : "61818fc5aa9eac6782796728",
    "title" : "title1",
    "body" : "content1",
    "category" : "제목1"
}'
```
### Response
```
{
  "message": "SUCCESS",
  "post_id": "6181a6fa68bb29d23b840bde"
}
```

### 2. 게시글 목록 조회
```GET/post/<post_id>?search-word="검색어"``` 
  - 검색어에 해당하는 게시글 반환
  - 주어진 조건에 해당하는 게시글 목록 조회
  
### Response
```
[
  {
    "category": "제목1",
    "title": "post1",
    "body": "content1",
    "user": "juju@naver.com",
    "read_user": 0,
    "updated_at": "2021-11-02 11:08:48.993000"
  }
]
```

### 3. 게시글 상세 조회
```GET/post/<post_id>```
  - post_id에 해당하는 게시글 조회
  - 게시물 읽힘수 적용

### Response
```
{
  "category": "제목1",
  "title": "title1",
  "body": "content1",
  "user": "newhyun@naver.com",
  "read_user": 1,
  "updated_at": "2021-11-02 21:00:42.075000"
}
```
### 4. 게시글 수정
```PUT/post/<post_id>```
  - jwt_required에서 받은 user와 게시글 작성자의 user_id와 비교하여 다르면 error 반환
  - post_id, user_id가 올바르면 body에서 받은 정보를 기반으로 수정

### Response

```
curl --location --request PUT 'http://127.0.0.1:5000/post/6181a9b968bb29d23b840bdf' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTg4NjI2MywianRpIjoiZjBhMWU3NjEtMWYzOS00YzM3LWEwZDctZmU4YjI1ODczZGI3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYxODE4ZmM1YWE5ZWFjNjc4Mjc5NjcyOCIsIm5iZiI6MTYzNTg4NjI2MywiZXhwIjoxNjM2NDkxMDYzfQ.godXBLO-K8Lk3Kz8FwdgiwBxiFn1KVgKFIcqA1uQ6uI' \
--data-raw '{
    "title" : "title1",
    "body"  : "content1"
}'
```

### 5. 게시글 삭제
```DELETE/post/<post_id>```
  - post_id에 해당하는 게시글이 존재하지 않으면 POST-DOES-NOT-EXIST error 반환
  - post_id,user_id가 올바르면 게시글 삭제
  - post_id가 전달되지 않으면 error반환

## 댓글 / 대댓글

### 1. 댓글 생성
```POST/comment/```
  - jwt_required로 유저확인
  - comment_id가 1이라면 1에 대한 댓글 생성
  
### Request
```
curl --location --request POST 'http://127.0.0.1:5000/comment' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTg4NjI2MywianRpIjoiZjBhMWU3NjEtMWYzOS00YzM3LWEwZDctZmU4YjI1ODczZGI3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYxODE4ZmM1YWE5ZWFjNjc4Mjc5NjcyOCIsIm5iZiI6MTYzNTg4NjI2MywiZXhwIjoxNjM2NDkxMDYzfQ.godXBLO-K8Lk3Kz8FwdgiwBxiFn1KVgKFIcqA1uQ6uI' \
--data-raw '{
    "user" : "61818fc5aa9eac6782796728",
    "post" : "6181a9b968bb29d23b840bdf",
    "body" : "댓글1"
}'
```
  
### Response
```
{
  "message": "SUCCESS",
  "comment_id": "6181aeda68bb29d23b840be0"
}
```
### 2. 댓글 조회
```GET/comment/<comment_id>?offset=0&limit=5```
  - 댓글 리스트 반환
  - 페이지 네이션 적용
  - 게시물 없을시 에러 반환
 
  
### Request 
```
curl --location --request GET 'http://127.0.0.1:5000/comment/6181aeda68bb29d23b840be0' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTg4NjI2MywianRpIjoiZjBhMWU3NjEtMWYzOS00YzM3LWEwZDctZmU4YjI1ODczZGI3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYxODE4ZmM1YWE5ZWFjNjc4Mjc5NjcyOCIsIm5iZiI6MTYzNTg4NjI2MywiZXhwIjoxNjM2NDkxMDYzfQ.godXBLO-K8Lk3Kz8FwdgiwBxiFn1KVgKFIcqA1uQ6uI'
```
### Response
```
[
  {
    "post": "title1",
    "body": "댓글1",
    "user": "newhyun@naver.com",
    "updated_at": "2021-11-02 21:34:18.323000"
  }
]
```
  
### 3. 댓글 삭제
```DELETE/comment/<comment_id>```
  - jwt_required로 유저확인
  - comment_id와 댓글을 쓴 user_id가 같은지 확인 후 통과 시 삭제
  
  
### 4. 대댓글 생성
```POST/reply/```
  - jwt_required로 유저확인
  - comment_id가 1이라면 1에 대한 댓글의 대댓글 생성
  
### Request
```
curl --location --request POST 'http://127.0.0.1:5000/reply' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYzNTg4NjI2MywianRpIjoiZjBhMWU3NjEtMWYzOS00YzM3LWEwZDctZmU4YjI1ODczZGI3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYxODE4ZmM1YWE5ZWFjNjc4Mjc5NjcyOCIsIm5iZiI6MTYzNTg4NjI2MywiZXhwIjoxNjM2NDkxMDYzfQ.godXBLO-K8Lk3Kz8FwdgiwBxiFn1KVgKFIcqA1uQ6uI' \
--data-raw '{
     "user" : "61818fc5aa9eac6782796728",
     "comment" : "6181af1a68bb29d23b840be1",
     "body" : "reply please1"
}'
```

### Response
```
{
  "message": "SUCCESS",
  "reply_id": "6181af3a68bb29d23b840be2"
}
```

### 5. 대댓글 조회
```GET/reply/<comment_id>```
  - 대댓글 리스트 반환
  - 페이지 네이션 적용
  - comment_id가 1이라면 1에 대한 댓글의 대댓글 조회
### Response
```
[
  {
    "user": "newhyun@naver.com",
    "comment": "댓글1",
    "body": "reply please1",
    "updated_at": "2021-11-02 21:35:54.896000"
  }
]
```

### 6. 대댓글 삭제
```DELETE/reply/<comment_id>```
  - jwt_required로 유저확인
  - user_id와 댓글을 쓴 유저가 같은지 확인 후 통과시 삭제



## API Documents 

주소 : https://documenter.getpostman.com/view/17922648/UVBznUqp

