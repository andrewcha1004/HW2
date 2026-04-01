# Age Prediction MLOps API

이 프로젝트는 홈 서버를 활용하여 아주 간단한 MLOps 파이프라인의 기초를 다지기 위한 얼굴 인식 및 나이 예측 API입니다. `FastAPI` 기반으로 구성되어 빠르며, `DeepFace` 모듈을 통해 이미지에서 사용자의 얼굴을 분석합니다. API 라우팅과 모델 추론 로직을 분리하여 확장 가능하고 유지보수가 쉬운 아키텍처를 도입했습니다.

## 📂 프로젝트 구조

```text
age-prediction-project/
├── main.py             # FastAPI 서버 애플리케이션 (API 라우팅, 에러 핸들링 등)
├── ml_model.py         # AI 모델 모듈 (이미지 디코딩 및 DeepFace 추론 로직 분리)
├── requirements.txt    # 실행에 필요한 파이썬 패키지 목록
└── .gitignore          # Git 업로드 시 무시할 캐시 파일 및 가상환경 세팅 정의
```

## 🚀 시작하기 (How to Run)

1. **폴더로 이동**
   ```bash
   cd /home/andrew/Desktop/andtiwooram2/age-prediction-project
   ```

2. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac 환경
   # Windows의 경우: venv\Scripts\activate
   ```

3. **필수 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
   > 💡 처음 API를 사용할 때, DeepFace가 내부적으로 모델 가중치를 자동으로 다운로드하므로 첫 응답 시 약간의 시간이 소요될 수 있습니다.

4. **API 서버 실행**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **테스트 해보기**
   서버가 정상적으로 구동되었다면 브라우저를 열고 API 문서용 UI에 접속하세요.
   해당 화면의 `/predict/age` 영역에서 사용자 이미지를 직접 업로드하고 나이 추론 결과를 테스트해 볼 수 있습니다.
   * **API 테스트 URL (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🏗 추후 발전 방향 (MLOps Roadmap)

이 프로젝트 형태에서 벗어나 더 견고한 파이프라인으로 구성하고 싶다면 다음과 같은 작업을 진행할 수 있습니다.
* **도커라이징(Dockerizing)**: 서버 컴퓨터 환경에 종속성을 없애기 위한 `Dockerfile`, `docker-compose.yaml` 세팅
* **추론 속도 최적화**: GPU 활용 추가 및 ONNX 모델 변환
* **모니터링 추가**: 실시간 얼굴 식별 성공률이나 서버 상태 모니터링을 위한 로그 연동
