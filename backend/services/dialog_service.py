import uuid
import json
import os
from typing import Dict, Any, List, Optional

# 模拟对话会话管理
class DialogSessionManager:
    """对话会话管理器"""
    def __init__(self):
        self.sessions = {}
        self.session_dir = "data/sessions"
        os.makedirs(self.session_dir, exist_ok=True)
    
    def create_session(self) -> str:
        """创建新的对话会话
        
        Returns:
            会话ID
        """
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "history": [],
            "patient_info": {},
            "tasks": [],
            "diagnosis": None,
            "image_analysis": None
        }
        return session_id
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """获取会话信息
        
        Args:
            session_id: 会话ID
            
        Returns:
            会话信息字典
        """
        return self.sessions.get(session_id, None)
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> None:
        """更新会话信息
        
        Args:
            session_id: 会话ID
            data: 要更新的数据
        """
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """添加对话消息
        
        Args:
            session_id: 会话ID
            role: 消息角色（'user' 或 'system'）
            content: 消息内容
        """
        if session_id in self.sessions:
            self.sessions[session_id]["history"].append({
                "role": role,
                "content": content
            })
    
    def save_session(self, session_id: str) -> None:
        """保存会话到文件
        
        Args:
            session_id: 会话ID
        """
        if session_id in self.sessions:
            file_path = os.path.join(self.session_dir, f"{session_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.sessions[session_id], f, ensure_ascii=False, indent=2)

# 初始化会话管理器
session_manager = DialogSessionManager()

# 模拟任务规划器
class TaskPlanner:
    """诊断任务规划器"""
    def __init__(self):
        # 预定义的任务模板
        self.task_templates = {
            "basic_info": {
                "name": "基本信息收集",
                "questions": [
                    "请问您的年龄是多少？",
                    "请问您的性别是？",
                    "您最近的主要不适症状是什么？",
                    "这些症状持续了多长时间？"
                ]
            },
            "tongue_diagnosis": {
                "name": "舌象诊断",
                "questions": [
                    "您的舌头是否有特殊感觉，如疼痛、麻木等？",
                    "您的舌苔颜色是什么样的？",
                    "您的舌头是否有裂纹或齿痕？"
                ]
            },
            "lifestyle": {
                "name": "生活习惯调查",
                "questions": [
                    "您的饮食习惯如何？",
                    "您的睡眠质量如何？",
                    "您是否有运动习惯？"
                ]
            }
        }
    
    def generate_tasks(self, patient_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据患者信息生成任务列表
        
        Args:
            patient_info: 患者信息
            
        Returns:
            任务列表
        """
        # 根据患者信息选择合适的任务
        # 这里简单返回所有任务，实际项目中应该根据患者信息进行个性化选择
        return list(self.task_templates.values())

# 初始化任务规划器
task_planner = TaskPlanner()

# 模拟信息提取器
class InfoExtractor:
    """患者信息提取器"""
    def __init__(self):
        pass
    
    async def extract_info(self, message: str) -> Dict[str, Any]:
        """从用户消息中提取关键信息
        
        Args:
            message: 用户消息
            
        Returns:
            提取的信息字典
        """
        # TODO: 使用NLP模型（如DeepSeek-V3）进行信息提取
        # 实际项目中应该使用NLP模型（如DeepSeek-V3）进行信息提取
        # 这里使用简单的规则进行模拟
        info = {}
        
        # 简单的规则匹配示例
        if "岁" in message or "年龄" in message:
            # 尝试提取年龄
            import re
            age_match = re.search(r'(\d+)岁', message)
            if age_match:
                info["age"] = int(age_match.group(1))
        
        if "男" in message:
            info["gender"] = "男"
        elif "女" in message:
            info["gender"] = "女"
        
        # 提取主诉（简化处理）
        if "疼" in message or "痛" in message:
            info["main_complaint"] = "疼痛"
        elif "咳嗽" in message:
            info["main_complaint"] = "咳嗽"
        elif "乏力" in message or "疲劳" in message:
            info["main_complaint"] = "乏力"
        
        return info

# 初始化信息提取器
info_extractor = InfoExtractor()

# 对话服务函数
def create_dialog_session() -> str:
    """创建新的对话会话
    
    Returns:
        会话ID
    """
    return session_manager.create_session()

async def process_dialog(session_id: str, message: str, user_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """处理对话消息
    
    Args:
        session_id: 会话ID
        message: 用户消息
        user_info: 用户信息（可选）
        
    Returns:
        系统响应
    """
    # 获取会话信息
    session = session_manager.get_session(session_id)
    if not session:
        return {"error": "会话不存在"}
    
    # 添加用户消息到历史记录
    session_manager.add_message(session_id, "user", message)
    
    # 提取用户信息
    extracted_info = await info_extractor.extract_info(message)
    if extracted_info:
        # 更新患者信息
        session["patient_info"].update(extracted_info)
    
    # 如果提供了额外的用户信息，也进行更新
    if user_info:
        session["patient_info"].update(user_info)
    
    # TODO: 使用大模型生成系统响应
    # 生成系统响应（实际项目中应该使用大模型生成）
    response = generate_response(session, message)
    
    # 添加系统响应到历史记录
    session_manager.add_message(session_id, "system", response)
    
    # 保存会话
    session_manager.save_session(session_id)
    
    return {
        "response": response,
        "extracted_info": extracted_info,
        "patient_info": session["patient_info"]
    }

def generate_response(session: Dict[str, Any], message: str) -> str:
    """生成系统响应
    
    Args:
        session: 会话信息
        message: 用户消息
        
    Returns:
        系统响应
    """
    # TODO: 使用大模型生成更智能的对话响应
    # 检查会话状态，决定下一步操作
    history = session["history"]
    patient_info = session["patient_info"]
    
    # 如果是首次对话
    if len(history) <= 1:  # 只有当前用户消息
        return "您好，我是智能舌苔诊断助手。请问您有什么不适症状？您也可以上传舌苔照片，我会为您进行初步分析。"
    
    # 如果缺少基本信息，引导用户提供
    if "age" not in patient_info:
        return "请问您的年龄是多少？"
    
    if "gender" not in patient_info:
        return "请问您的性别是？"
    
    if "main_complaint" not in patient_info:
        return "您主要感到哪些不适？请简要描述您的症状。"
    
    # 如果已经有了基本信息，进行更深入的问诊
    if "image_analysis" in session and session["image_analysis"]:
        # 如果已经上传了舌苔图像，结合图像分析结果进行回复
        image_result = session["image_analysis"]
        return f"根据您的舌苔图像分析和症状描述，您的舌象显示为{image_result['class_name']}，这可能与{patient_info.get('main_complaint', '您的症状')}有一定关联。建议您{image_result['suggestions'][0]}。您还有其他问题吗？"
    
    # 一般性回复
    return "感谢您提供的信息。为了更准确地分析您的情况，建议您上传一张清晰的舌苔照片。您也可以继续描述您的其他症状或生活习惯。"