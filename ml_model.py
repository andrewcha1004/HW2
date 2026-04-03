import cv2
import numpy as np
from deepface import DeepFace

class AgePredictionModel:
    def __init__(self):
        # 초기화 시점에 모델을 로드하여 Warm-up 할 수 있는 공간입니다.
        # DeepFace 모듈은 기본적으로 최초 호출 시 가중치를 다운로드 및 캐싱합니다.
        print("Initializing Age Prediction Model...")

    def predict(self, image_bytes: bytes) -> list:
        # 1. 전달받은 이미지 바이트 데이터를 numpy array로 변환
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # 2. OpenCV를 사용하여 이미지 디코딩
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("이미지를 디코딩할 수 없습니다. 형식을 확인해주세요.")
        
        # 3. DeepFace를 이용한 나이 및 성별 예측
        try:
            # enforce_detection=True: 얼굴이 없으면 예외 발생
            # actions=['age', 'gender']: 나이와 성별 예측 (MLOps 요구사항)
            results = DeepFace.analyze(img_path=img, actions=['age', 'gender'], enforce_detection=True)
            
            # 여러 명의 얼굴이 검출될 수 있으므로 항상 리스트 형태로 정규화
            if not isinstance(results, list):
                results = [results]
                
            predictions = []
            for face in results:
                # dominant_gender 값을 추출 (예: 'Man', 'Woman')
                gender = face.get('dominant_gender', 'Unknown')
                predictions.append({
                    "age": face.get('age'),
                    "gender": gender,
                    "region": face.get('region') # 사진 상의 얼굴 위치 좌표
                })
            return predictions
            
        except ValueError as e:
            if "Face could not be detected" in str(e):
                return [] # 얼굴을 찾지 못한 경우는 빈 리스트 반환
            raise e
