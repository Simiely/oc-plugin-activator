# OC插件 快速激活工具

[![Build Windows EXE](https://github.com/Simiely/oc-plugin-activator/actions/workflows/build-exe.yml/badge.svg)](https://github.com/Simiely/oc-plugin-activator/actions/workflows/build-exe.yml)

一键清空 OctaneRender 缓存 + 复制 AppData / octane 文件夹的 Windows 工具。

## 功能

| 按钮 | 操作 |
|------|------|
| 🗑  清空 OctaneRender 缓存 | 清空 `Local\OctaneRender` + `Roaming\OctaneRender` |
| 📋  复制资源到目标路径 | 复制 `AppData` → `C:\Users\{用户名}` + 复制 `octane` → 指定路径 |

## 使用方法

1. 下载 `Activator.exe`，放在和 `AppData`、`octane` 同级的目录
2. 双击运行，填写**用户名**和 **octane 复制目标路径**
3. 点击「保存配置」
4. 点击按钮执行操作

## 下载 exe

👉 https://github.com/Simiely/oc-plugin-activator/actions

点击最新成功的 Build Windows EXE → 底部 Artifacts → 下载

## 注意事项

- 清空**不可撤销**
- `AppData` 和 `octane` 文件夹需和 exe 在同一目录
- 窗口可自由拉伸
- Windows 10/11 支持深色标题栏
