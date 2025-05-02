<template>
  <div class="app-container">
    <header class="app-header">
      <h1>智能舌苔诊断系统</h1>
    </header>
    
    <main class="main-content">
      <div class="left-panel">
        <div class="image-upload-section">
          <h2>舌苔图像上传</h2>
          <div 
            class="upload-area"
            @dragover.prevent
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <input 
              type="file" 
              ref="fileInput" 
              style="display: none" 
              accept="image/*"
              @change="handleFileChange"
            >
            <div v-if="!imagePreview" class="upload-placeholder">
              <i class="upload-icon">📷</i>
              <p>点击或拖拽图片到此处上传</p>
            </div>
            <img v-else :src="imagePreview" class="image-preview" alt="舌苔图像预览">
          </div>
          <button 
            class="upload-button" 
            :disabled="!selectedFile" 
            @click="uploadImage"
          >
            {{ uploading ? '上传中...' : '开始分析' }}
          </button>
        </div>
        
        <div v-if="imageAnalysis" class="analysis-result">
          <h2>图像分析结果</h2>
          <div class="result-card">
            <p><strong>舌象类型:</strong> {{ imageAnalysis.class_name }}</p>
            <p><strong>置信度:</strong> {{ (imageAnalysis.confidence * 100).toFixed(2) }}%</p>
            <div class="suggestions">
              <h3>初步建议:</h3>
              <ul>
                <li v-for="(suggestion, index) in imageAnalysis.suggestions" :key="index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <div class="right-panel">
        <div class="chat-section">
          <h2>智能问诊对话</h2>
          <div class="chat-container">
            <div class="chat-messages" ref="chatMessages">
              <div 
                v-for="(message, index) in chatHistory" 
                :key="index"
                :class="['message', message.role === 'user' ? 'user-message' : 'system-message']"
              >
                <div class="message-content">{{ message.content }}</div>
              </div>
            </div>
            
            <div class="chat-input">
              <textarea 
                v-model="userMessage" 
                placeholder="请描述您的症状或提问..."
                @keyup.enter.ctrl="sendMessage"
              ></textarea>
              <button @click="sendMessage" :disabled="!userMessage.trim() || sending">
                {{ sending ? '发送中...' : '发送' }}
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="patientInfo && Object.keys(patientInfo).length > 0" class="patient-info">
          <h2>患者信息摘要</h2>
          <div class="info-card">
            <p v-if="patientInfo.gender"><strong>性别:</strong> {{ patientInfo.gender }}</p>
            <p v-if="patientInfo.age"><strong>年龄:</strong> {{ patientInfo.age }}岁</p>
            <p v-if="patientInfo.main_complaint"><strong>主诉:</strong> {{ patientInfo.main_complaint }}</p>
            <p v-if="patientInfo.duration"><strong>病程:</strong> {{ patientInfo.duration }}</p>
          </div>
        </div>
      </div>
    </main>
    
    <footer class="app-footer">
      <p>© 2023 智能舌苔诊断系统 - 基于多模态信息的中医辅助诊断平台</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      // 图像上传相关
      selectedFile: null,
      imagePreview: null,
      uploading: false,
      imageAnalysis: null,
      
      // 对话相关
      sessionId: null,
      userMessage: '',
      chatHistory: [],
      sending: false,
      patientInfo: {},
    }
  },
  mounted() {
    // 创建对话会话
    this.createDialogSession();
    
    // 添加系统欢迎消息
    this.chatHistory.push({
      role: 'system',
      content: '您好，我是智能舌苔诊断助手。请问您有什么不适症状？您也可以上传舌苔照片，我会为您进行初步分析。'
    });
  },
  methods: {
    // 图像上传相关方法
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.processSelectedFile(file);
      }
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.processSelectedFile(file);
      }
    },
    processSelectedFile(file) {
      this.selectedFile = file;
      const reader = new FileReader();
      reader.onload = e => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    async uploadImage() {
      if (!this.selectedFile) return;
      
      this.uploading = true;
      
      try {
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        
        // 调用后端API上传图像
        const response = await fetch('http://localhost:8000/upload-image/', {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error('图像上传失败');
        }
        
        const result = await response.json();
        this.imageAnalysis = result;
        
        // 将分析结果添加到对话中
        this.chatHistory.push({
          role: 'system',
          content: `我已分析您的舌苔图像，您的舌象显示为${result.class_name}，置信度为${(result.confidence * 100).toFixed(2)}%。${result.suggestions[0]}`
        });
        
        // 滚动到最新消息
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error('上传图像出错:', error);
        alert('图像上传失败，请重试');
      } finally {
        this.uploading = false;
      }
    },
    
    // 对话相关方法
    async createDialogSession() {
      try {
        const response = await fetch('http://localhost:8000/dialog/start/', {
          method: 'POST'
        });
        
        if (!response.ok) {
          throw new Error('创建对话会话失败');
        }
        
        const data = await response.json();
        this.sessionId = data.session_id;
      } catch (error) {
        console.error('创建对话会话出错:', error);
      }
    },
    async sendMessage() {
      if (!this.userMessage.trim() || !this.sessionId) return;
      
      // 添加用户消息到历史记录
      this.chatHistory.push({
        role: 'user',
        content: this.userMessage
      });
      
      const message = this.userMessage;
      this.userMessage = '';
      this.sending = true;
      
      // 滚动到最新消息
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      
      try {
        // 调用后端API发送消息
        const response = await fetch('http://localhost:8000/dialog/message/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            session_id: this.sessionId,
            message: message
          })
        });
        
        if (!response.ok) {
          throw new Error('发送消息失败');
        }
        
        const data = await response.json();
        
        // 添加系统回复到历史记录
        this.chatHistory.push({
          role: 'system',
          content: data.response
        });
        
        // 更新患者信息
        if (data.patient_info) {
          this.patientInfo = data.patient_info;
        }
        
        // 滚动到最新消息
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error('发送消息出错:', error);
        // 添加错误消息
        this.chatHistory.push({
          role: 'system',
          content: '消息发送失败，请重试'
        });
      } finally {
        this.sending = false;
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatMessages;
      container.scrollTop = container.scrollHeight;
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #1e88e5;
  color: white;
  padding: 1rem 2rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-content {
  display: flex;
  flex: 1;
  padding: 2rem;
  gap: 2rem;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
}

.left-panel, .right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.image-upload-section, .analysis-result, .chat-section, .patient-info {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #1e88e5;
  background-color: rgba(30, 136, 229, 0.05);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #1e88e5;
}

.image-preview {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
}

.upload-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #1e88e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.upload-button:hover:not(:disabled) {
  background-color: #1976d2;
}

.upload-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result-card, .info-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1rem;
}

.suggestions h3 {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.suggestions ul {
  padding-left: 1.5rem;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-break: break-word;
}

.user-message {
  align-self: flex-end;
  background-color: #1e88e5;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.system-message {
  align-self: flex-start;
  background-color: #f1f1f1;
  border-bottom-left-radius: 0.25rem;
}

.chat-input {
  display: flex;
  border-top: 1px solid #eee;
  padding: 0.75rem;
}

.chat-input textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  height: 80px;
  font-family: inherit;
}

.chat-input button {
  padding: 0 1.5rem;
  margin-left: 0.75rem;
  background-color: #1e88e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chat-input button:hover:not(:disabled) {
  background-color: #1976d2;
}

.chat-input button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.app-footer {
  background-color: #f5f5f5;
  padding: 1rem;
  text-align: center;
  border-top: 1px solid #eee;
  margin-top: auto;
}

h2 {
  margin-bottom: 1rem;
  color: #333;
  font-weight: 500;
}
</style>