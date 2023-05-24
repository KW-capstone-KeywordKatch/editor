#! /usr/bin/env python3

"""
플라스크 애플리케이션이 동작하기 위한 환경 구성 및 빌드 스크립트
"""

import os
import sys
import subprocess

'''------------------- Status -------------------'''
SYNC_DEP = False            # 의존성(패키지) 설치
EXECUTE_APP = False         # 앱 실행
SETUP = True
INTEGRATE = False
CONTAINER = False
PROD = True

'''----------------- ANSI Control ----------------'''

GREET_VENV = r"""
 __     ___      _               _                   _                                      _
 \ \   / (_)_ __| |_ _   _  __ _| |   ___ _ ____   _(_)_ __ ___  _ __  _ __ ___   ___ _ __ | |_
  \ \ / /| | '__| __| | | |/ _` | |  / _ \ '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __|
   \ V / | | |  | |_| |_| | (_| | | |  __/ | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_
    \_/  |_|_|   \__|\__,_|\__,_|_|  \___|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__|

"""

GREET_APP = r"""
  _  ___  __                   _ _ _
 | |/ / |/ /           ___  __| (_) |_ ___  _ __
 | ' /| ' /   _____   / _ \/ _` | | __/ _ \| '__|
 | . \| . \  |_____| |  __/ (_| | | || (_) | |
 |_|\_\_|\_\          \___|\__,_|_|\__\___/|_|
"""

GREET_DOCKER = r"""
  ____             _
 |  _ \  ___   ___| | _____ _ __
 | | | |/ _ \ / __| |/ / _ \ '__|
 | |_| | (_) | (__|   <  __/ |
 |____/ \___/ \___|_|\_\___|_|
"""


# 한 줄을 비우고 커서를 맨 앞으로 이동
def _clear_line(msg):
    print("\033[2K\r" + msg)

# 터미널에 출력되는 텍스트 색 설정
def _print_with_color(color, msg, clear=False):
    """
    color - "green", "red"
    """
    if clear:
        print("\033[2J\033[H", end='')
    if color == 'green':
        print("\033[32m", end='')
        print(msg)
        print("\033[0m")
    elif color == 'red':
        print("\033[31m", end='')
        print(msg)
        print("\033[0m")
    elif color == 'blue':
        print("\033[34;1m", end='')
        print(msg)
        print("\033[0m")

##################################################

def _call(cmd, cwd=None):
    return subprocess.call(cmd, shell=True, cwd=cwd)


# 플라스크 애플리케이션 실행을 위한 환경 변수 설정
def _set_environ():
    os.environ["FLASK_APP"] = "kk_editor"
    os.environ["FLASK_DEBUG"] = "0"
    os.environ["FLASK_RUN_PORT"] = "8000"
    os.environ["FLASK_RUN_HOST"] = "0.0.0.0"


# 가상환경을 구성하는 패키지 설치
def _sync_dependencies():
    _call("pipenv sync")


# 명령어 파싱, 상태 설정
def _parse(argv):
    global SYNC_DEP
    global EXECUTE_APP
    global SETUP
    global INTEGRATE
    global PROD
    global CONTAINER
    if 'setup' in argv:
        SETUP = True
    if 'sync' in argv:
        SYNC_DEP = True
    if 'execute' in argv:
        EXECUTE_APP = True
    if 'integrate' in argv:
        INTEGRATE = True
    if 'local' in argv:
        PROD = False
    if 'container' in argv:
        CONTAINER = True

def main(argv):
    _parse(argv)
    # import 경로 추가
    if SETUP:
        p = os.path.dirname(__file__)
        sys.path.append(p)
        sys.path.append(os.path.sep.join(p.split(os.path.sep)[:-1]))
    # 의존성 설치
    if SYNC_DEP:
        print("sync dependencies... ")
        _sync_dependencies()
    # 플라스크 애플리케이션 실행
    if EXECUTE_APP:
        _print_with_color('blue', GREET_APP, clear=True)
        if CONTAINER:
            _print_with_color('blue', GREET_DOCKER)
        sys.stdout.flush()
        # 환경변수 설정
        _set_environ()
        print(os.getcwd())
        # container 내부에서 실행
        if CONTAINER:
            _call("flask run --host=0.0.0.0", cwd=os.sep.join(os.getcwd().split(os.sep)[:-1]))
        else:
            # 배포환경이 아닌 로컬 환경에서 실행
            if not PROD:
                _call("docker container run -v /Users/mingeun/logs:/app/kk_editor/logs -p 8000:8000 local/editor:latest")
            # 배포환경에서 실행
            else:
                _call("flask run --host='0.0.0.0'", cwd=os.sep.join(os.getcwd().split(os.sep)[:-1]))
    if INTEGRATE:
        if PROD:
            # 도커 이미지 빌드 -> 허브에 업로드
            _call("docker image build --no-cache -t mingeun2154/editor:latest .")
            _call("docker image push mingeun2154/editor:latest")
        # local 
        else:
            _call("docker image build --no-cache -t local/editor:latest .")

if __name__ == "__main__":
    try: 
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        from apis.v1 import scheduler
        scheduler.shutdown()
        _clear_line("Bye")
        exit(0)
