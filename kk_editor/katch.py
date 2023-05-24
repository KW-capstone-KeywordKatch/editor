#! /usr/bin/env python3
"""
플라스크 애플리케이션이 동작하기 위한 환경 구성 및 빌드 스크립트
"""

import os
import sys
import subprocess
import pty
import errno
from time import sleep

#################### Status ######################
SYNC_DEP = False
EXECUTE_APP = False
SETUP = True
INTEGRATE = False
##################################################


################## ANSI control ##################

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
    if 'setup' in argv:
        SETUP = True
    if 'sync' in argv:
        SYNC_DEP = True
    if 'execute' in argv:
        EXECUTE_APP = True

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
        _set_environ()
        _call("flask run", cwd=os.sep.join(os.getcwd().split(os.sep)[:-1]))

if __name__ == "__main__":
    try: 
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        from apis.v1 import scheduler
        scheduler.shutdown()
        _clear_line("Bye")
        exit(0)
