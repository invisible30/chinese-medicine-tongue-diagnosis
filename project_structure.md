# 智能舌苔诊断 Agent 系统项目结构

```
/
├── backend/                  # 后端服务
│   ├── api/                 # API 接口
│   ├── models/              # 模型定义
│   ├── services/            # 业务逻辑
│   ├── utils/               # 工具函数
│   ├── config/              # 配置文件
│   └── main.py              # 入口文件
│
├── frontend/                # 前端应用
│   ├── public/              # 静态资源
│   ├── src/                 # 源代码
│   │   ├── components/      # 组件
│   │   ├── pages/           # 页面
│   │   ├── assets/          # 资源文件
│   │   ├── utils/           # 工具函数
│   │   └── App.js           # 主应用
│   └── package.json         # 依赖配置
│
├── models/                  # 模型文件
│   ├── image_model/         # 舌苔图像分类模型
│   └── embedding/           # 文本向量模型
│
├── data/                    # 数据文件
│   ├── knowledge_base/      # 中医知识库
│   ├── training/            # 训练数据
│   └── user_data/           # 用户数据
│
├── notebooks/               # Jupyter 笔记本
│   └── model_training.ipynb # 模型训练笔记本
│
├── scripts/                 # 脚本文件
│   ├── setup.py             # 环境配置脚本
│   └── data_processing.py   # 数据处理脚本
│
├── tests/                   # 测试文件
│   ├── api_tests/           # API 测试
│   └── model_tests/         # 模型测试
│
├── .env                     # 环境变量
├── requirements.txt         # Python 依赖
├── docker-compose.yml       # Docker 配置
└── README.md                # 项目说明
```