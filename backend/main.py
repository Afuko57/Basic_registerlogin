from fastapi import FastAPI

app = FastAPI(
    title = "Management System ",
    description = "Management System",
    version = "1.0.0",
)

import user.user as router_User

app.include_router(router_User.router)