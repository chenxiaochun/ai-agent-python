# AI Agent Python

## 项目介绍
这是一个使用Python和OpenAI API（兼容阿里云百炼）构建的AI助手应用。

## 安装依赖

### 使用pip
```bash
pip install -e .
```

### 使用uv
```bash
uv sync
```

## 配置API密钥

为了安全起见，API密钥应存储在环境变量或配置文件中，而不是硬编码在源代码里。

### 方法1：使用.env配置文件（推荐）

1. 复制示例配置文件并创建实际配置文件
```bash
cp .env.example .env
```

2. 编辑.env文件，填入您的阿里云百炼API密钥
```
DASHSCOPE_API_KEY=your_actual_api_key_here
```

3. 运行程序，它会自动从.env文件加载API密钥
```bash
python main.py
```

### 方法2：设置环境变量

在运行程序前设置环境变量：
```bash
export DASHSCOPE_API_KEY=your_actual_api_key_here
python main.py
```

## 注意事项
- 不要将包含实际API密钥的.env文件提交到版本控制系统中
- .env文件已被添加到.gitignore中，以防止意外提交
- 使用.env.example文件作为模板，而不是直接复制包含真实密钥的.env文件

## 许可证
MIT
