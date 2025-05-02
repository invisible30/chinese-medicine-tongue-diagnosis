# 智能舌苔诊断 Agent 系统启动指南

本文档提供了如何设置和运行智能舌苔诊断 Agent 系统的基本框架的说明。

## 项目结构

项目采用前后端分离的架构：
- 后端：Python FastAPI 框架
- 前端：Vue.js 3 框架

详细的项目结构可以在 `project_structure.md` 文件中查看。

## 环境要求

- Python 3.8+
- Node.js 14+
- npm 6+

## 后端设置

1. 创建并激活虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 激活虚拟环境（Linux/Mac）
source venv/bin/activate
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 启动后端服务

```bash
cd backend
python main.py
```

后端服务将在 http://localhost:8000 上运行。

## 前端设置

1. 安装依赖

```bash
cd frontend
npm install
```

2. 启动开发服务器

```bash
npm run dev
```

前端应用将在 http://localhost:3000 上运行。

## 功能测试

1. 打开浏览器访问 http://localhost:3000
2. 上传舌苔图像进行分析
3. 通过聊天界面与系统进行交互

## 注意事项

- 当前版本是基本框架，仅包含核心功能的模拟实现
- 图像分类模型使用随机结果模拟，实际项目中需要替换为训练好的 ResNet18 模型
- 对话功能使用规则匹配模拟，实际项目中需要集成大模型 API
- 知识库使用静态数据模拟，实际项目中需要构建向量数据库

## 后续开发建议

1. 集成实际的 ResNet18 模型用于舌苔图像分类
2. 接入 GPT-4 或 DeepSeek-V3 等大模型 API
3. 构建中医知识向量数据库
4. 完善用户界面和交互体验
5. 添加用户认证和数据存储功能

## 目录结构创建

在开始运行前，请确保创建以下目录：

```bash
mkdir -p backend/services
mkdir -p backend/api
mkdir -p backend/models
mkdir -p backend/utils
mkdir -p backend/config
mkdir -p data/sessions
mkdir -p data/knowledge_base
mkdir -p frontend/src/assets
mkdir -p frontend/src/components
mkdir -p frontend/src/pages
mkdir -p frontend/public
mkdir -p models/image_model
mkdir -p models/embedding
```

## 创建必要的资源文件

```bash
# 创建前端CSS文件
echo "/* 主样式文件 */" > frontend/src/assets/main.css

# 创建上传目录
mkdir -p uploads
```