# 服务模块初始化文件
# 导出所有服务模块，方便导入

from .image_service import process_tongue_image
from .dialog_service import create_dialog_session, process_dialog
from .knowledge_service import search_knowledge_base, generate_report