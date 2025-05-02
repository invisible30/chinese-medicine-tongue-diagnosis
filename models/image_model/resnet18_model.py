import torch
import torch.nn as nn
import torchvision.models as models
from typing import Dict, Any, Tuple
import os

class TongueClassifier(nn.Module):
    """舌苔图像分类模型，基于ResNet18架构"""
    def __init__(self, num_classes: int = 8):
        super(TongueClassifier, self).__init__()
        # 加载预训练的ResNet18模型
        self.model = models.resnet18(pretrained=True)
        
        # 修改最后的全连接层以适应我们的分类任务
        in_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(in_features, num_classes)
        )
        
        # 舌苔分类标签
        self.classes = [
            "正常舌", "齿痕舌", "地图舌", "裂纹舌", "镜面舌", "紫舌", "红舌", "淡白舌"
        ]
    
    def forward(self, x):
        """前向传播"""
        return self.model(x)
    
    def predict(self, image_tensor: torch.Tensor) -> Dict[str, Any]:
        """预测图像类别
        
        Args:
            image_tensor: 预处理后的图像张量
            
        Returns:
            包含分类结果和置信度的字典
        """
        self.eval()
        with torch.no_grad():
            outputs = self(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            return {
                "class_name": self.classes[predicted.item()],
                "confidence": confidence.item(),
                "class_probabilities": {self.classes[i]: prob.item() for i, prob in enumerate(probabilities[0])}
            }
    
    def save(self, path: str) -> None:
        """保存模型
        
        Args:
            path: 保存路径
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.state_dict(), path)
    
    def load(self, path: str) -> None:
        """加载模型
        
        Args:
            path: 模型路径
        """
        self.load_state_dict(torch.load(path))
        self.eval()

# 图像预处理函数
def preprocess_image(image_path: str) -> torch.Tensor:
    """预处理图像用于模型输入
    
    Args:
        image_path: 图像文件路径
        
    Returns:
        预处理后的图像张量
    """
    from torchvision import transforms
    from PIL import Image
    
    # 定义预处理变换
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # 加载并预处理图像
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)  # 添加批次维度
    
    return image_tensor

# 模型训练函数
def train_model(model: TongueClassifier, train_loader, valid_loader, 
               num_epochs: int = 10, learning_rate: float = 0.001) -> Tuple[TongueClassifier, Dict[str, list]]:
    """训练舌苔分类模型
    
    Args:
        model: 模型实例
        train_loader: 训练数据加载器
        valid_loader: 验证数据加载器
        num_epochs: 训练轮数
        learning_rate: 学习率
        
    Returns:
        训练后的模型和训练历史
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # 训练历史记录
    history = {
        "train_loss": [],
        "train_acc": [],
        "valid_loss": [],
        "valid_acc": []
    }
    
    for epoch in range(num_epochs):
        # 训练阶段
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            # 梯度清零
            optimizer.zero_grad()
            
            # 前向传播
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # 反向传播和优化
            loss.backward()
            optimizer.step()
            
            # 统计
            train_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        # 计算训练集上的平均损失和准确率
        train_loss = train_loss / train_total
        train_acc = train_correct / train_total
        
        # 验证阶段
        model.eval()
        valid_loss = 0.0
        valid_correct = 0
        valid_total = 0
        
        with torch.no_grad():
            for inputs, labels in valid_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                
                # 前向传播
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                # 统计
                valid_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                valid_total += labels.size(0)
                valid_correct += (predicted == labels).sum().item()
        
        # 计算验证集上的平均损失和准确率
        valid_loss = valid_loss / valid_total
        valid_acc = valid_correct / valid_total
        
        # 记录历史
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["valid_loss"].append(valid_loss)
        history["valid_acc"].append(valid_acc)
        
        print(f"Epoch {epoch+1}/{num_epochs}, "
              f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
              f"Valid Loss: {valid_loss:.4f}, Valid Acc: {valid_acc:.4f}")
    
    return model, history