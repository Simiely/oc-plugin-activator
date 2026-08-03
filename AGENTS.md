# AGENTS.md · 项目规则

> 给 AI / 未来的你：只记代码里看不出的关键信息。详细问题记录见 [DEVELOP.md](DEVELOP.md)（8 条一坑一篇）。

## 技术栈

- Python tkinter（**不用 ttk**——ttk Style + clam 主题下 padding tuple 转字符串致 Tcl 解析失败）+ PyInstaller 打包
- 超椭圆圆角图标（小米风格，|x/a|³+|y/b|³=1）+ ImageMagick 多尺寸 ICO
- CI：GitHub Actions 构建 exe + onepage 落地页部署

## 关键坑

1. **PyInstaller 路径陷阱**：exe 运行时 `__file__` 指向 `C:\Temp\_MEIxxxxx` 临时解压目录——用 `sys.executable`（frozen 判断）取真实路径
2. **ttk padding tuple 坑**：某些 tk 版本转字符串 `"0 14"` 传 Tcl 失败（Bad screen distance）——抛弃 ttk 用 tk 原生 + bg/fg 写死，控件不传 padding tuple
3. **目标目录锁文件**：shutil.rmtree 会失败——用 `copytree(src, dst, dirs_exist_ok=True)` 合并覆盖，每个文件单独 try/except
4. **ICO 多尺寸**：PIL `save(format='ICO', sizes=[...])` 只输出单帧——PIL 处理透明度 + ImageMagick `convert` 合并多尺寸
5. **透明通道丢失**：上传 PNG 被转 JPEG 丢 alpha——保留透明源文件 + CI 用 ImageMagick 重新生成
6. **深色标题栏**：纯 tkinter 改不了——`DwmSetWindowAttribute(hwnd, 20, c_int(2), 4)`
7. **GitHub Actions Node.js 24**：2026 年 6 月起强制，checkout@v4 等有 deprecation 警告但可用

## 约定

- 中文 UI；config.json 自动生成；构建：`pyinstaller --onefile --windowed --icon icon.ico`
