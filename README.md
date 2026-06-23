# OC插件 快速激活工具

一键清空 OctaneRender 缓存、复制 AppData 和 c4doctane 文件夹的 Windows 工具。

## 功能

| 按钮 | 功能 | 目标路径 |
|------|------|----------|
| 🗑 清空 OctaneRender (Local) | 删除文件夹内所有内容 | `C:\Users\{用户名}\AppData\Local\OctaneRender` |
| 🗑 清空 OctaneRender (Roaming) | 删除文件夹内所有内容 | `C:\Users\{用户名}\AppData\Roaming\OctaneRender` |
| 📋 复制 AppData 文件夹到用户目录 | 复制程序所在目录下的 `AppData` 文件夹 | → `C:\Users\{用户名}\AppData` |
| 📋 复制 c4doctane 文件夹到目标路径 | 复制程序所在目录下的 `c4doctane` 文件夹 | → 用户自行填写的路径 |

## 使用方法

### 方式一：直接运行 Python 脚本

1. 确保已安装 Python 3.7+
2. 下载 `oc_tool.py` 和 `config.json`
3. 将 `oc_tool.py` 放在包含 `AppData` 和 `c4doctane` 文件夹的目录中
4. 运行 `python oc_tool.py`

### 方式二：打包为 exe（推荐）

1. 安装 PyInstaller：`pip install pyinstaller`
2. 双击运行 `build_exe.bat`，或手动执行：
   ```bash
   pyinstaller --onefile --windowed --name "OC插件快速激活工具" oc_tool.py
   ```
3. 打包完成后，exe 文件位于 `dist\OC插件快速激活工具.exe`
4. 将 exe 放在包含 `AppData` 和 `c4doctane` 文件夹的目录中，双击运行

## 配置说明

打开程序后，在配置区填写：

- **用户名**：你的 Windows 用户名（如 `Simiely`），程序会自动拼出对应路径
- **c4doctane 复制目标路径**：点击「选择文件夹」或手动填写目标路径

填写后点击「保存配置」，下次打开自动记住。

路径预览区会实时显示各功能对应的实际路径，确认无误后再操作。

## 注意事项

- 清空文件夹操作不可撤销，操作前会弹出确认提示
- 确保 `AppData` 和 `c4doctane` 文件夹与程序在同一目录下
- 如目标路径不存在，程序会自动创建

## 开发相关

参见 [DEVELOP.md](DEVELOP.md)
