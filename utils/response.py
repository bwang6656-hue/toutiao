from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message:str="success", data=None):
    content = {"code":200, "message": message, "data": data}
    #目标：把 任何 数据类型 都 转换 为 标准的 json 数据类型都要正常响应code,message,data
    return JSONResponse(content=jsonable_encoder(content))
