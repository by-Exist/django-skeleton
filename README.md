# Django-Skeleton

## [ Example Site ]

- [API Example - Swagger](https://exampleapp.kro.kr/v1/schema/swagger/)

## [ Description ]

- drf로 서비스를 개발할 때 필요한 기본 설정들에 대한 레포지토리입니다.

## [ Structure ]

Root directory

ㄴ backend : django 기반 Web Application Server

ㄴ frontend : 미정

ㄴ nginx : Nginx 기반 Web Server (Proxy)

ㄴ docker-compose : 개발, 테스트, 배포 단계에서 사용될 docker-compose 파일들

ㄴ env : docker-compose에서 활용되는 환경변수 파일들

nginx, backend, frontend는 각자 자신의 Dockerfile을 지닙니다.

## [ Look Up ]

### [Destribution.md](./Destribution.md)

- 배포 시 진행할 일반적인 단계가 기록되어 있습니다.

### [backend/utils/drf_custom/README.md](./backend/utils/drf_custom/README.md)

- drf에 추가적인 기능을 부여하기 위해 만든 유틸 설명서입니다.
