from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title = "Management System ",
    description = "Management System",
    version = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

import user.user as router_User

app.include_router(router_User.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)