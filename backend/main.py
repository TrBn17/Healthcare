from fastapi import FastAPI
from api.predict import predict_stroke
from api.chat import router as chat_router

app = FastAPI(title="Stroke Prediction API")

app.post("/predict")(predict_stroke)
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8333)
