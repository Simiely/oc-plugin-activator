# CHANGELOG.md · 版本记录

> 项目无正式版本 tag，按功能迭代记录。完整问题记录见 [DEVELOP.md](DEVELOP.md)。

## 功能里程碑

- **OC 插件快速激活工具**：一键清空 OctaneRender 缓存、复制 AppData 和 c4doctane 文件夹的 Windows 工具（oc_tool.py 单文件 + icon.ico + config.json 自动生成）
- **超椭圆圆角图标**（n=3，小米风格）：PIL numpy 处理透明度 + ImageMagick 多尺寸 ICO
- **CI/CD**：GitHub Actions 构建 exe（build-exe.yml）+ onepage 落地页部署（deploy-onepage.yml）

## 关键修复

- Bad screen distance：抛弃 ttk 改 tk 原生
- PyInstaller 路径：sys.executable 取真实目录
- 复制中断：copytree dirs_exist_ok 合并覆盖 + 单文件 try/except
- 透明通道丢失：保留 PNG 源文件 + CI 重新生成
- 深色标题栏：DwmSetWindowAttribute

## 备注

- 无版本 tag / Release；仓库含 20260704Final 空占位文件（无内容）
