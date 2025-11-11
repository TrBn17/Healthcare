from fastapi import FastAPI
from api.predict import predict_stroke
from api.chat import router as chat_router
from api.users import router as users_router
from db.database import init_db

app = FastAPI(title="Stroke Prediction API")

# Khởi tạo database
init_db()

app.post("/predict")(predict_stroke)
app.include_router(chat_router)
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8333)
