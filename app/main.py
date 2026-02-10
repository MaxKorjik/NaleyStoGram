from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .auth import router

app = FastAPI()
app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

@app.get('/')
def home():
    return {"Hello" : "World"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True,
#     )