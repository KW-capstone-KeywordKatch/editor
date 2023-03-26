## crawler

웹에서 기사를 수집하는 모듈

### 실행 전 읽기 바람 ###

./create_dir 를 실행해  ~/articles 디렉토리를 만든 후

rssCrawl.py 의 file_path 조정 후
python3 main.py 실행하면 됨.

EC2에서 필요한 모듈 pip install 다운로드 편의를 위해 
module_install 을 만들었으나 로컬 환경에서는 불필요한 것까지 다운로드 될 수 있으니 주의. 
필요한 것만 골라서 install 바람.


기사 모두 삭제하고 싶을 때 ./clear_articles 실행.
