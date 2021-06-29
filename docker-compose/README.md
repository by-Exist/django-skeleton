# Environment

- 각 환경에서 지켜야 하는 지침

## 파일명 형식

- docker-compose.{Environment}.yml

## Development - dev

- 개발중인 서비스 빌드된 이미지 X
- 외부 서비스 X
- env 파일 O

## Stage - stage

- 개발중인 서비스 빌드된 이미지 X
- 외부 서비스 O
- env 파일 O

## Production - prod

- 서비스 빌드 이미지 O
- 외부 서비스 O
- env 파일 X
