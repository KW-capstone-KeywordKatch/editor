# Editor component
기사를 수집하고 분석하여 주제(키워드)를 추출하는 컴포넌트

## 기능
* 14개의 언론사 홈페이지로부터 기사 수집
* 수집한 기사의 주제와 관련된 키워드 추출
* [API SPEC](https://docs.google.com/spreadsheets/d/15Bsn81Iq3FapjFeCDDqaJcVKtJk5iYT3mlrhNwuXsA4/edit#gid=0)

## 기술 스택
* Application: `Python` `Flask`
* Deployment: `AWS EC2` `Docker`
* Database: `MySQL` `AWS RDS`

## Directories
* core           
  * [crawler](https://github.com/KW-capstone-KeywordKatch/editor/tree/main/core/crawler)      
  * [analyzer](https://github.com/KW-capstone-KeywordKatch/editor/tree/main/core/analyzer)
* [server-application](https://github.com/KW-capstone-KeywordKatch/editor/tree/main/server-application)

## contributors
* [khw3754](https://github.com/khw3754)
  * crawler 모듈
* [Mingeun Park](https://github.com/mingeun2154)
  * analyzer 모듈
