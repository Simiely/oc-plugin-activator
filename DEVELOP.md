# 开发文档 - OC插件 快速激活工具

## 项目结构

```
oc-plugin-activator/
├── oc_tool.py          # 主程序（Python + tkinter GUI）
├── config.json         # 用户配置文件（自动生成）
├── build_exe.bat      # Windows 打包脚本
├── README.md           # 使用说明
└── DEVELOP.md         # 本文件
```

## 环境要求

- Python 3.7+
- tkinter（通常随 Python 自带）
- Windows 系统（路径依赖 `C:\Users\...`）

## 本地运行

```bash
# 克隆仓库
git clone https://github.com/Simiely/oc-plugin-activator.git
cd oc-plugin-activator

# 直接运行
python oc_tool.py
```

## 打包为 exe

### 在 Windows 上：

```bash
# 安装依赖
pip install pyinstaller

# 打包
pyinstaller --onefile --windowed --name "OC插件快速激活工具" oc_tool.py
```

### build_exe.bat

双击运行即可自动完成上述步骤，exe 生成在 `dist/` 目录。

## 核心逻辑说明

### 路径生成

用户名填写后，以下路径自动生成：

```python
local_path  = f"C:\\Users\\{username}\\AppData\\Local\\OctaneRender"
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

在 `oc_tool.py` 的 `get_octane_paths` 函数或按钮回调中添加新路径，参考现有 `on_clean_local` 的写法。

### 修改界面样式

`tickinter` 的 `ttk.Style` 支持自定义主题，修改 `setup_ui` 中的 `self.style` 配置即可。

### 交叉编译（Linux → Windows exe）

当前不支持。建议在 Windows 上直接打包，或使用 [Wine + PyInstaller](https://pyinstaller.org/en/stable/) 尝试交叉编译。

## TODO

- [ ] 支持拖拽文件夹到界面
- [ ] 增加操作成功/失败的的系统通知
- [ ] 支持多语言（中/英）
- [ ] 增加日志文件输出（当前仅在界面显示）

## 授权

MIT License
