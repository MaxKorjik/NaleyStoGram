from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .auth import router

app = FastAPI()
app.include_router(router=router)

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Use the list, not ["*"]
    allow_credentials=True,       # This must be True for cookies/auth headers
    allow_methods=["*"],          # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],          # Allows all headers
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