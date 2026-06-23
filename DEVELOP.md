# 开发文档 — OC插件 快速激活工具

## 文件结构

```
├── oc_tool.py          # 主程序（纯 tkinter，深色模式）
├── config.json          # 自动生成
├── README.md
├── DEVELOP.md
├── build_exe.bat
└── .github/workflows/build-exe.yml
```

## 技术要求

- Python 3.7+
- tkinter（内置）
- Windows（路径依赖 `C:\Users\...`）

## 开发运行

```bash
git clone https://github.com/Simiely/oc-plugin-activator.git
cd oc-plugin-activator
python oc_tool.py
```

## 打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Activator" oc_tool.py
```

GitHub Actions 推送 main 自动打包。

## 设计规范

### 深色模式

纯 `tk` 控件 + 颜色写死，不用 `ttk.Style`。

颜色变量：
```
BG   = "#1e1e1e"  窗口背景
CARD = "#2d2d2d"  卡片背景
INPUT= "#3c3c3c"  输入框背景
BLUE = "#0078d4"  按钮
RED  = "#c42b1c"  清空按钮（警示）
```

### 标题栏深色

Windows 10/11 通过 `dwmapi.DwmSetWindowAttribute` 设置，非 Windows 自动跳过。

### 核心规则（避坑）

- 控件构造器 **不传** `padx`/`pady` tuple（只传 pack/grid）
- 不用 `ttk`、不用 `LabelFrame`
- 路径用 `sys.executable`（打包后）或 `__file__`（源码）
