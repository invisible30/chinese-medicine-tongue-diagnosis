import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

# 导入服务模块
from services.image_service import process_tongue_image
from services.dialog_service import create_dialog_session, process_dialog
from services.knowledge_service import search_knowledge_base

app = FastAPI(title="智能舌苔诊断系统", description="基于多模态信息的中医舌苔诊断辅助系统")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件目录配置
os.makedirs("./uploads", exist_ok=True)
os.makedirs("./static", exist_ok=True)
app.mount("/static", StaticFiles(directory="./static"), name="static")

# 数据模型
class DialogRequest(BaseModel):
    session_id: str
    message: str
    user_info: Optional[dict] = None

class DiagnosisResponse(BaseModel):
    diagnosis: str
    confidence: float
    recommendations: List[str]
    reference_sources: List[str]

# API路由
@app.get("/")
async def read_root():
    return {"message": "智能舌苔诊断系统API服务正在运行"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """上传舌苔图像并进行初步分析"""
    try:
        result = await process_tongue_image(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dialog/start/")
async def start_dialog():
    """开始一个新的对话会话"""
    session_id = create_dialog_session()
    return {"session_id": session_id}

@app.post("/dialog/message/", response_model=dict)
async def dialog_message(request: DialogRequest):
    """处理对话消息"""
    response = await process_dialog(request.session_id, request.message, request.user_info)
    return response

@app.post("/knowledge/search/")
async def search_knowledge(query: str = Form(...)):
    """搜索中医知识库"""
    results = await search_knowledge_base(query)
    return {"results": results}

@app.get("/diagnosis/summary/{session_id}")
async def get_diagnosis_summary(session_id: str):
    """获取诊断摘要"""
    # 这里应该从会话中获取诊断摘要
    # 暂时返回模拟数据
    return {
        "patient_info": {
            "gender": "男",
            "age": 30,
            "main_complaint": "舌苔发白，口干"
        },
        "diagnosis": "疑似脾胃湿热",
        "recommendations": ["建议清淡饮食", "可考虑服用xxx中药"]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)