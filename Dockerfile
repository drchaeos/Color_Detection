# 공식 Python 이미지 사용
FROM python:3.9-slim

# 컨테이너 내의 작업 디렉토리 설정
WORKDIR /usr/src/app

# 현재 디렉토리의 내용을 컨테이너의 /usr/src/app에 복사
COPY . .

# 필요한 패키지 설치
RUN pip install -r requirements.txt

# 컨테이너의 8000 포트에 접근
EXPOSE 8000

# 컨테이너가 시작될 때 실행할 명령어 정의
CMD ["uvicorn", "color_web:app", "--host", "0.0.0.0", "--port", "8000"]
