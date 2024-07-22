# 베이스 이미지로 python 3.12.4 사용
FROM python:3.12.4-slim

# 작업 디렉토리 설정
WORKDIR /code

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 프로젝트의 requirements.txt 파일을 복사하고 의존성 설치
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 프로젝트 소스 코드를 복사
COPY . /code/

# 환경 변수 설정 (필요한 경우)
ENV PYTHONUNBUFFERED 1

# 애플리케이션 시작 명령어
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "AglaiaLabBE.wsgi:application"]