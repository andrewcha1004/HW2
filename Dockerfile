# Python 3.10 슬림 이미지를 사용하여 이미지 크기를 최소화합니다.
FROM python:3.10-slim

# 파이썬 환경 변수 설정
# PYTHONDONTWRITEBYTECODE: 파이썬이 .pyc 파일을 쓰지 않도록 하여 용량 절약
# PYTHONUNBUFFERED: 파이썬 로그가 버퍼링 없이 즉시 출력되도록 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# OpenCV 의존성 설치 (DeepFace가 의존성으로 설치하는 opencv-python 실행을 위한 필수 시스템 라이브러리)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libxcb1 \
    libxext6 \
    libsm6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 매니저 파일 복사 (캐시 활용을 위해 로직 코드보다 먼저 복사)
COPY requirements.txt .

# 의존성 패키지 설치
# --no-cache-dir: pip 캐시를 저장하지 않아 최종 이미지 용량 절약
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션의 나머지 코드를 복사 (이 부분이 변경되어도 위의 패키지 설치 레이어는 캐시됨)
COPY . .

# FastAPI 기본 포트 노출
EXPOSE 8000

# 컨테이너 실행 시 uvicorn을 사용하여 서버 구동
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
