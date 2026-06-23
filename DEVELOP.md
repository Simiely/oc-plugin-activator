# 开发文档 - OC插件 快速激活工具

## 项目结构

```
oc-plugin-activator/
├── oc_tool.py                  # 主程序（Python + tkinter GUI，深色模式）
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

每次向 `main` 分支推送代码，自动触发打包流程。exe 可在 Actions 页面下载。

## 核心逻辑

### 两个核心按钮

| 按钮 | 内部操作 |
|------|---------|
| **清空 OctaneRender 缓存** | 同时清空 `Local\OctaneRender` 和 `Roaming\OctaneRender` 两个目录 |
| **复制资源到目标路径** | 同时复制 `AppData` 到 `C:\Users\{用户名}`，复制 `octane` 到配置的路径 |

### 路径获取（重要）

PyInstaller 打包后，`__file__` 指向临时解压目录，需用 `sys.executable` 获取真实路径：

```python
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
```

### 安全清空（`safe_clean_folder`）

- 只删除**内容**，不删除文件夹本身
- 遍历所有文件和子文件夹逐一删除
- 无权限的项目会跳过并提示

### 安全复制（`safe_copy_folder`）

- 目标存在时先删除再复制，确保完全覆盖
- 使用 `shutil.copytree` 保留目录结构

### 深色主题

使用 `ttk.Style` + `clam` 主题实现深色模式。颜色定义在文件顶部：

```python
BG = "#1e1e1e"      # 窗口背景
FG = "#d4d4d4"      # 文字颜色
FRAME_BG = "#252526" # 框架背景
ENTRY_BG = "#3c3c3c" # 输入框背景
BTN_BG = "#0e639c"   # 按钮背景
```

### 配置文件

`config.json` 结构：

```json
{
    "username": "Simiely",
    "octane_target": "D:\\plugins\\octane"
}
```

程序启动时自动读取，保存时自动写入。

## 修改指南

### 添加新的功能

1. 在 `setup_ui` 中添加新按钮
2. 编写对应的回调方法（如 `on_new_function`）
3. 在 `refresh_preview` 中更新路径预览
4. 更新 `load_config` / `save_config` 中的默认配置字段

### 修改深色主题颜色

修改文件顶部 `BG`、`FG` 等颜色变量即可全局生效。

### 注意

- 所有路径使用 `os.path.join` 拼接，确保跨平台兼容
- 操作前弹出确认弹窗，防止误操作
- 日志用 `self.log()` 写入，同时显示在界面

## TODO

- [ ] Node.js 24 原生兼容的 GitHub Actions
- [ ] 支持拖拽文件夹到界面
- [ ] 增加操作成功/失败的系统通知
- [ ] 支持多语言（中/英）
- [ ] 增加日志文件输出
- [ ] 数字签名 exe，减少杀软误报

## 授权

MIT License
