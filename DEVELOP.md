# 开发文档

## 文件

```
oc_tool.py      主程序（纯 tkinter，深色模式）
icon.ico        超椭圆圆角图标（小米风格 n=3）
config.json     自动生成
.github/workflows/build-exe.yml    GitHub Actions 自动打包
```

## 开发

```bash
pip install pyinstaller
python oc_tool.py                          # 直接运行
pyinstaller --onefile --windowed --icon icon.ico --name "Activator" oc_tool.py
```

推送 main 分支后 GitHub Actions 自动构建。

## 规则

- 控件构造器不传 padx/pady tuple（放 pack/grid 里）
- 不用 ttk，颜色直接 bg/fg 写死
- 打包后路径用 sys.executable，源码用 \_\_file\_\_
