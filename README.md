# BySZDesk 说明

桌面助手.

环境: Windows11

目前支持以下功能:

- 自行在config.json输入deepseek api后可以提问
- 简陋的便签功能, 保存到本地的notes文件夹

TODO:

- AI提问查看询问进度和报错信息
- 应用快捷方式存储和访问
- 窗口大小调整
- 文本框markdown渲染, 字体颜色等
- 访问任意日期的便签, 修改已有便签内容, 删除便签
- 模板化便签(每次创建便签都可以自动生成一套既定模板文字, 比如"今日计划:"), 且这个模板可以自定义, 以一个不可删除的便签形式存在

目前自用.

## **使用Anaconda创建虚拟环境**

```bash
# 创建名为floatdesk的虚拟环境（Python 3.11）
conda create -n byszdesk python=3.11

# 激活环境
conda activate byszdesk

# 安装基础依赖
pip install -r requirements.txt
```

之后若使用vscode, 可Ctrl+Shift+P 找到Python: Select Interpreter选择对应的conda解释器.
之后打开cmd终端就会看到创建的conda环境名称.

## **项目启动流程**

1. 获取DeepSeek API Key：

   - 访问 https://platform.deepseek.com/api-keys
   - 创建新密钥并复制

2. 首次运行前：

   ```bash
   # 创建配置文件
   echo {"deepseek_api_key": "你的API密钥"} > config.json
   ```

3. 运行程序：

   ```bash
   python main.py
   ```
