from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import history, news, users, favorite
from utils.exception_handlers import register_exception_handlers

app = FastAPI(
    title="FastAPI Demo",
    description="头条练习",
    version="0.1.0",
)

# 注册异常处理器
register_exception_handlers(app)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 消除favicon.ico请求的404错误
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return ""


# 注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
