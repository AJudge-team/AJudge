# A-Judge [![Build Status](https://travis-ci.org/AJudge-team/AJudge.svg?branch=master)](https://travis-ci.org/AJudge-team/AJudge)

## Abstract
---
A-Judge는 Open-source Online Judge Platform이다.

A-Judge는 온라인 저지에서 필요한 소스 코드의 컴파일, 실행, 채점, 그리고 결과를 제공한다. 따라서, A-Judge를 사용한다면 누구나 쉽게 채점 모듈을 추가하고 채점 사이트를 구축할 수 있다.

온라인 저지 서비스를 제공하는 곳의 예로, BOJ (https://www.acmicpc.net/), algospot (https://algospot.com/), Lavida Online Judge (http://lavida.us/)등이 있다.

## Usecase
---
1. 유저가 소스 코드를 작성하고 이를 APP Server에 제출한다.
1. APP Server가 유저의 요청을 받고, 이를 분석해서 Judge Context를 채운다.
1. Judge Context를 Controller에게 넘긴다.
1. Controller가 Judge Context를 분석해서, Runtime Context를 채운다.
1. Controller가 Runtime Context를 해당 언어의 Runner에게 제공한다.
1. Runner는 Sandbox를 생성하고, Sandbox에게 Runtime Context를 제공한다.
1. Sandbox는 Runtime Context에 따라 소스 코드를 실행하고 실행 결과를 Runner에게 다시 반환한다.
1. Runner는 Sandbox로부터 받은 결과를 Controller에게 제공한다.
1. Controller는 Validator를 이용해 채점후 결과를 Judge Service를 통해 APP Server로 반환한다.
1. APP Server가 결과를 가공하여 유저에게 표시한다.

A-Judge는 3~9 Usecase 를 담당하는 Open-source Online Judge Platform이다.

## demonstration
---
[영상]()

## ThirdParty Libraries
---
(docker) (https://github.com/docker/docker)
(docker-py) (https://github.com/docker/docker-py)
(pyenv) (https://github.com/yyuu/pyenv)
(requests) (https://github.com/kennethreitz/requests)
(six) (https://github.com/JioCloud/python-six/blob/master/setup.py)
(websocket-client) (https://github.com/liris/websocket-client)

## License
---
MIT
