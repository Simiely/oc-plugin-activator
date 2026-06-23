# 开发文档 - OC插件 快速激活工具

## 项目结构

```
oc-plugin-activator/
├── oc_tool.py                  # 主程序（Python + tkinter GUI）
├── config.json                 # 用户配置文件（运行后自动生成）
├── README.md                   # 使用说明
├── DEVELOP.md                  # 本文件
├── build_exe.bat              # Windows 本地打包脚本
└── .github/workflows/
    └── build-exe.yml           # GitHub Actions 自动打包
```

## 环境要求

- Python 3.7+
- tkinter（通常随 Python 自带）
- Windows 系统（路径依赖 `C:\Users\...`）

## 本地开发

```bash
# 克隆仓库
git clone https://github.com/Simiely/oc-plugin-activator.git
cd oc-plugin-activator

# 直接运行
python oc_tool.py

# 本地打包 exe
pip install pyinstaller
pyinstaller --onefile --windowed --name "Activator" oc_tool.py
```

## GitHub Actions 自动打包

每次向 `main` 分支推送代码，会自动触发打包流程。

流程文件：`.github/workflows/build-exe.yml`

**工作流程：**
1. 检出代码
2. 设置 Python 3.11 环境
3. 安装 PyInstaller
4. 执行 `pyinstaller --onefile --windowed --name "Activator"`
5. 上传生成的 exe 为 Artifact

**下载地址：** https://github.com/Simiely/oc-plugin-activator/actions

> ⚠️ 注意：GitHub Actions 的 `actions/checkout@v4`、`actions/setup-python@v5` 等目前使用 Node.js 20（2026 年已弃用），但会被强制在 Node.js 24 上运行，不影响正常使用。后续可升级到 Node.js 24 原生版本。

## 核心逻辑说明

### 路径生成

用户名填写后，以下路径自动生成：

```python
local_path   = f"C:\\Users\\{username}\\AppData\\Local\\OctaneRender"
roaming_path = f"C:\\Users\\{username}\\AppData\\Roaming\\OctaneRender"
appdata_dst  = f"C:\\Users\\{username}\\AppData"
```

### 安全清空文件夹（`safe_clean_folder`）

- 只删除**内容**，不删除文件夹本身
- 遍历目录下所有文件和子文件夹逐一删除
- 无权限的文件/文件夹会跳过并提示

### 安全复制文件夹（`safe_copy_folder`）

- 目标存在时先删除再复制，确保完全覆盖
- 使用 `shutil.copytree` 保留目录结构

### 配置文件

`config.json` 结构：

```json
{
    "username": "Simiely",
    "c4doctane_target": "D:\\Cinema4D\\plugins"
}
```

程序启动时自动读取，关闭前保存。

## 修改指南

### 添加新的清空路径

在 `oc_tool.py` 中添加新的按钮回调，参考现有 `on_clean_local` 的写法：

```python
def on_clean_new_path(self):
    username = self.get_username()
    if not username: return
    path = f"C:\\Users\\{username}\\Some\\New\\Path"
    # ... 确认弹窗、清空逻辑
```

然后在 `setup_ui` 中添加对应的按钮。

### 修改界面样式

`ttk.Style` 支持自定义主题，修改 `setup_ui` 中的配置：

```python
self.style.configure("Action.TButton", font=("Microsoft YaHei", 11, "bold"), padding=8)
```

## 常见问题

### 为什么 GitHub Actions 构建显示 Node.js 20 deprecated 警告？

这是 GitHub 平台迁移节点导致的。2026 年 6 月起 Node.js 20 被弃用，GitHub 官方 action 正在陆续升级到 Node.js 24。当前这些 action 仍能正常工作（被强制在 Node.js 24 上运行）。

### Python 打包后 exe 多大？

约 **10 MB**，包含 Python 运行时 + tkinter GUI 库 + 程序代码。

### tkinter 在 Windows 上需要额外安装吗？

不需要。官版 Python for Windows 自带 tkinter。如果使用 GitHub Actions 的 `setup-python`，Python 来自 `actions/python-versions` 构建，同样包含 tkinter。

## TODO

- [ ] Node.js 24 原生兼容的 GitHub Actions（升级 `checkout`/`setup-python`/`upload-artifact` 版本）
- [ ] 支持拖拽文件夹到界面
- [ ] 增加操作成功/失败的系统通知
- [ ] 支持多语言（中/英）
- [ ] 增加日志文件输出（当前仅在界面显示）
- [ ] 数字签名 exe，减少杀软误报

## 授权

MIT License
