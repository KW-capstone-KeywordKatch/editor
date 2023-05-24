# base image
FROM python:3.11

# 디렉토리 생성
WORKDIR /editor

# package install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all files
COPY . .

COPY kk_editor/Pipfile kk_editor/Pipfile.lock ./

RUN pip install pipenv && \
    pipenv install --system --deploy

WORKDIR kk_editor
RUN chmod +x katch.py
RUN exit && pipenv shell
# 실행
EXPOSE 8000
#CMD ["pipenv", "run", "katch.py", "execute"]
CMD ["python3", "katch.py", "execute"]

## 지금 그냥 editor 디렉토리애서 실행하니까 안되는걸 확인했고 그래서 kk_editor로 들어가서 실행하는 걸 시도중