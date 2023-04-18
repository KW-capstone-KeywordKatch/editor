#! /usr/bin/env python3
"""
플라스크 애플리케이션이 동작하기 위한 환경 구성 및 빌드 스크립트
"""

import os
import sys
import subprocess

#################### Status ######################
SYNC_DEP = False
EXECUTE_APP = False
INTEGRATE = False
##################################################

################## ANSI control ##################
# 한 줄을 비우고 커서를 맨 앞으로 이동
def _clear_line(msg):
    print("\033[2K\r" + msg)

# 터미널에 출력되는 텍스트 색 설정
def _print_with_color(color, msg):
    """
    color - "green", "red"
    """
    if color == 'green':
        print("\033[32m", end='')
        print(msg)
        print("\033[0m", end='')
    elif color == 'red':
        print("\033[31m", end='')
        print(msg)
        print("\033[0m", end='')

##################################################

def _call(cmd, silent=False):
    return subprocess.call(cmd, shell=True)


# 플라스크 애플리케이션 실행을 위한 환경 변수 설정
def _set_environ():
    os.environ["FLASK_APP"] = "kk-editor"
    os.environ["FLASK_DEBUG"] = "1"
    os.environ["FLASK_RUN_PORT"] = "8000"


# 파이썬 가상 환경 진입
def _enter_venv():
    _print_with_color('green', 'enter to virtual environment\n')
    _call("pipenv shell")


# 가상환경을 구성하는 패키지 설치
def _fetch_dependencies():
    _call("pipenv install")


# 명령어 파싱, 상태 설정
def _parse(argv):
    global SYNC_DEP
    global EXECUTE_APP
    if 'sync' in argv:
        SYNC_DEP = True
    if 'execute' in argv:
        EXECUTE_APP = True


def main(argv):
    _parse(argv)
    # 의존성 설치 및 가상환경 진입
    if SYNC_DEP:
        print("fetch dependencies... ")
        _fetch_dependencies()
        _enter_venv()
    # 플라스크 애플리케이션 실행
    if EXECUTE_APP:
        _set_environ()
        # 프로젝트 루트 디렉토리에서 실행되도록 보장되어야 한다.
        os.chdir("..")
        print(os.getcwd())
        _call("flask run")

if __name__ == "__main__":
    try: 
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        _clear_line("Bye")
        exit(0)
