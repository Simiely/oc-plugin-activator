# 开发文档

## 文件结构

```
oc_tool.py      主程序（纯 tkinter，深色模式）
icon.ico        程序图标（超椭圆圆角）
config.json     自动生成
.github/workflows/build-exe.yml    GitHub Actions 自动打包
```

## 本地开发

```bash
pip install pyinstaller
python oc_tool.py                          # 直接运行
pyinstaller --onefile --windowed --icon icon.ico --name "Activator" oc_tool.py  # 打包
```

## 关键规则

- 控件构造器不传 `padx/pady` tuple（放 `pack`/`grid` 里）
- 不用 `ttk` 控件
- 打包后路径用 `sys.executable`，源码用 `__file__`
