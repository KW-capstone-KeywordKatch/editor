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
CMD ["python3", "katch.py", "execute"]