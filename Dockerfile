# Python 3.11 Slim 이미지 사용 (가볍고 빠름)
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (SQLite3 등)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 소스 코드 복사
COPY . .

# 데이터 디렉토리 권한 설정
RUN mkdir -p data && chmod 777 data

# 빌드 시점에 데이터베이스 생성 (선택사항: 이미지 크기가 커지지만 바로 실행 가능)
# 사용자의 "즉시 실행" 요구사항을 위해 빌드 타임에 마이그레이션 실행
RUN echo "Building ManualAI Database..." && python3 src/migrate.py

# 실행 명령
CMD ["python3", "src/main.py"]
