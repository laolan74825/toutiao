from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response( message: str = "请求成功",data=None):
    """
    成功响应
    :param data: 响应数据
    :param message: 响应消息
    :return: 响应字典
    """
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    # 把任何的FastAPI、Pydantic、ORM对象都要正常响应，必须使用jsonable_encoder进行编码
    return JSONResponse(content=jsonable_encoder(content))
