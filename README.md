# OC插件 快速激活工具

[![Build Windows EXE](https://github.com/Simiely/oc-plugin-activator/actions/workflows/build-exe.yml/badge.svg)](https://github.com/Simiely/oc-plugin-activator/actions/workflows/build-exe.yml)

一键清空 OctaneRender 缓存、复制 AppData 和 c4doctane 文件夹的 Windows 工具。

## 功能

| 按钮 | 功能 | 目标路径 |
|------|------|----------|
| 🗑 清空 OctaneRender (Local) | 删除文件夹内所有内容 | `C:\Users\{用户名}\AppData\Local\OctaneRender` |
| 🗑 清空 OctaneRender (Roaming) | 删除文件夹内所有内容 | `C:\Users\{用户名}\AppData\Roaming\OctaneRender` |
| 📋 复制 AppData 到用户目录 | 复制程序所在目录下的 `AppData` 文件夹 | → `C:\Users\{用户名}\AppData` |
| 📋 复制 c4doctane 到目标路径 | 复制程序所在目录下的 `c4doctane` 文件夹 | → 用户自行填写的路径 |

## 快速下载 exe

每次往 `main` 分支推送代码，GitHub Actions 会自动构建 exe：

1. 打开：https://github.com/Simiely/oc-plugin-activator/actions
2. 点击最新成功的 **Build Windows EXE** 工作流
3. 滚动到底部 **Artifacts** 区域
4. 下载 **OC插件快速激活工具**（zip 包，约 10 MB）
5. 解压得到 `Activator.exe`

## 使用方法

### 方式一：直接下载 exe（推荐）

1. 从上方 Actions 页面下载 `Activator.exe`
2. 把 exe 放到包含 `AppData` 和 `c4doctane` 文件夹的目录中
3. 双击运行，填写用户名和路径，点击对应按钮

### 方式二：运行 Python 脚本

1. 确保已安装 Python 3.7+
2. 克隆仓库并运行：
   ```bash
   git clone https://github.com/Simiely/oc-plugin-activator.git
   cd oc-plugin-activator
   python oc_tool.py
   ```

### 方式三：本地打包 exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Activator" oc_tool.py
# exe 在 dist/Activator.exe
```

## 配置说明

打开程序后，在配置区填写：

- **用户名**：你的 Windows 用户名（如 `Simiely`），程序会自动拼出对应路径
- **c4doctane 复制目标路径**：点击「选择文件夹」或手动填写

填写后点击「保存配置」，下次打开自动记住。

路径预览区会实时显示各功能对应的实际路径，确认无误后再操作。

## 注意事项

- 清空文件夹操作**不可撤销**，操作前会弹出确认提示
- 确保 `AppData` 和 `c4doctane` 文件夹与程序在同一目录下
- 如目标路径不存在，程序会自动创建

## 开发相关

参见 [DEVELOP.md](DEVELOP.md)
