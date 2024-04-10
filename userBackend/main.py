import os
import sys
from fastapi import FastAPI


from routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from load_dotenv import load_dotenv

import uvicorn

app = FastAPI(title="Api", version="1.0.0")
sys.path.append(os.path.join(os.path.dirname(__file__)))
load_dotenv()


# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8001, debug=True)
