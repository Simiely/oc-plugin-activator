# OC插件 快速激活工具

[![Build Windows EXE](https://github.com/Simiely/oc-plugin-activator/actions/workflows/build-exe.yml/badge.svg)](https://github.com/Simiely/oc-plugin-activator/actions/workflows/build-exe.yml)

一键清空 OctaneRender 缓存、复制 AppData 和 octane 文件夹的 Windows 工具。深色界面，简洁易用。

## 功能

| 按钮 | 功能 | 操作内容 |
|------|------|----------|
| 🗑 清空 OctaneRender 缓存 | 一键清空两个目录 | `Local\OctaneRender` + `Roaming\OctaneRender` |
| 📋 复制资源到目标路径 | 一键复制两个文件夹 | `AppData` → `C:\Users\{用户名}` + `octane` → 指定路径 |

## 快速下载 exe

每次往 `main` 分支推送代码，GitHub Actions 自动构建。最新版本：

👉 https://github.com/Simiely/oc-plugin-activator/actions

点击最新成功的 **Build Windows EXE** 工作流 → 底部 **Artifacts** → 下载 **OC插件快速激活工具**

## 使用方法

1. 下载 `Activator.exe`，放在包含 `AppData` 和 `octane` 文件夹的目录中
2. 双击运行，填写**用户名**和 **octane 复制目标路径**
3. 点击「保存配置」
4. 点击对应按钮执行操作

## 配置说明

- **用户名**：你的 Windows 用户名，会自动拼出 `C:\Users\{用户名}\...` 路径
- **octane 复制目标路径**：点「选择」按钮或手动填写

## 注意事项

- 清空操作**不可撤销**，操作前会弹出确认提示
- 确保 `AppData` 和 `octane` 文件夹与 exe 在同一目录下
- 目标路径不存在时程序会自动创建

## 开发相关

参见 [DEVELOP.md](DEVELOP.md)
