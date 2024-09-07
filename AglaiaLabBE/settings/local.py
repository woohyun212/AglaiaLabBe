from .base import *

ALLOWED_HOSTS = ['*']

# SSH Tunnel Setting

SSH_ADDRESS = env('EC2_ENDPOINT')
SSH_USERNAME = env('EC2_USERNAME')
PATH_TO_SSH_PRIVATE_KEY = env('EC2_SSH_KEY')
LOCAL_DB_ENDPOINT_ON_THE_SERVER = env('DB_HOST')  # RDS_ENDPOINT
LOCAL_DB_PORT_ON_THE_SERVER = int(env('DB_PORT'))

from sshtunnel import SSHTunnelForwarder

# SSH 터널 설정 (EC2 인스턴스를 통해 RDS에 접근)
server = SSHTunnelForwarder(
    (SSH_ADDRESS, 22),  # EC2 주소 및 SSH 포트
    ssh_username=SSH_USERNAME,  # EC2의 SSH 유저명
    ssh_pkey=PATH_TO_SSH_PRIVATE_KEY,  # PEM 키 파일 경로
    remote_bind_address=(LOCAL_DB_ENDPOINT_ON_THE_SERVER, LOCAL_DB_PORT_ON_THE_SERVER),  # RDS's Endpoint and ports
)
server.start()

# 로컬에서 할당된 포트 확인 (보통 5432가 사용되지만 다를 수 있음)
print(f"Local bind port: {server.local_bind_port}")

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'PORT': server.local_bind_port,
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
    },
}
