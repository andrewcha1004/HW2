from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from ml_model import AgePredictionModel

#Hello World!

# FastAPI 앱 생성
app = FastAPI(
    title="Age Prediction MLOps API",
    description="홈 서버를 활용한 얼굴 인식 및 나이 예측 API입니다.",
    version="1.0.0"
)

# 앱 실행 시 한번만 모델 클래스를 메모리에 로드 (싱글톤 패턴과 유사한 효과)
model = AgePredictionModel()

@app.get("/")
def health_check():
    """로드밸런서나 컨테이너 오케스트레이션(Kubernetes 등)을 위한 상태 체크용 엔드포인트"""
    return {"status": "Healthy", "message": "API is running."}

@app.post("/predict/age")
async def predict_age(file: UploadFile = File(...)):
    """이미지 업로드를 통한 나이 예측 엔드포인트"""
    # 1. 파일 확장자/MIME 타입 방어 로직 (보안 및 에러 방지)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    try:
        image_bytes = await file.read()
        
        # 2. 분리해둔 모델에 예측 위임
        predictions = model.predict(image_bytes)
        
        if not predictions:
            return JSONResponse(
                status_code=200, 
                content={"message": "사진에서 얼굴을 감지하지 못했습니다.", "predictions": []}
            )
            
        # 3. 정상 응답
        return {
            "filename": file.filename, 
            "faces_detected": len(predictions), 
            "predictions": predictions
        }
        
    except ValueError as val_e:
        raise HTTPException(status_code=400, detail=str(val_e))
    except Exception as e:
        # 서버 내부 로깅을 위한 처리
        raise HTTPException(status_code=500, detail=f"서버 내부 오류 발생: {str(e)}")

# 직접 스크립트 실행용
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
