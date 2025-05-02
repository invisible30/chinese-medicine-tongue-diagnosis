# 智能舌苔诊断 Agent 系统项目结构

```
/
├── backend/                  # 后端服务
│   ├── data/                # 后端数据
│   │   ├── knowledge_base/  # 知识库数据
│   │   └── sessions/        # 会话数据
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py     # 初始化文件
│   │   ├── dialog_service.py  # 对话服务
│   │   ├── image_service.py   # 图像处理服务
│   │   └── knowledge_service.py  # 知识服务
│   ├── static/              # 静态资源
│   ├── uploads/             # 上传文件目录
│   └── main.py              # 入口文件
│
├── frontend/                # 前端应用
│   ├── src/                 # 源代码
│   │   ├── assets/          # 资源文件
│   │   ├── App.vue          # 主应用组件
│   │   └── main.js          # 入口文件
│   ├── index.html           # HTML 入口
│   ├── package.json         # 依赖配置
│   ├── package-lock.json    # 依赖锁定文件
│   └── vite.config.js       # Vite 配置
│
├── models/                  # 模型文件
│   └── image_model/         # 舌苔图像分类模型
│       └── resnet18_model.py  # ResNet18 模型实现
│
├── data/                    # 数据文件
│   └── knowledge_base/      # 中医知识库
│       └── sample_knowledge.json  # 示例知识数据
│
├── uploads/                 # 上传的图像文件
│   └── *.jpg                # 多个舌苔图像样本
│
├── .gitignore               # Git 忽略文件
├── README.md                # 项目说明
├── README_SETUP.md          # 项目启动指南
├── project_structure.md     # 原项目结构文档
├── project_structure_new.md # 新项目结构文档
└── requirements.txt         # Python 依赖
```

## 主要组件说明

### 后端 (backend)
- **services/**: 包含核心业务逻辑服务
  - **dialog_service.py**: 处理用户对话交互
  - **image_service.py**: 处理舌苔图像分析
  - **knowledge_service.py**: 管理中医知识库查询
- **data/**: 存储后端数据
  - **knowledge_base/**: 中医知识库数据
  - **sessions/**: 用户会话数据
- **main.py**: 应用入口点，启动FastAPI服务

### 前端 (frontend)
- 基于Vue.js 3和Vite构建的现代Web应用
- **src/App.vue**: 主应用组件
- **src/main.js**: 前端应用入口

### 模型 (models)
- **image_model/**: 包含用于舌苔图像分析的深度学习模型
  - **resnet18_model.py**: 基于ResNet18架构的图像分类模型

### 数据 (data)
- **knowledge_base/**: 存储结构化的中医知识
  - **sample_knowledge.json**: 示例知识数据

### 上传文件 (uploads)
- 存储用户上传的舌苔图像，用于分析和诊断

### 配置文件
- **requirements.txt**: 列出所有Python依赖
- **README_SETUP.md**: 提供项目设置和启动指南