# CHANGELOG.md · 版本记录

> 项目无正式版本 tag，按功能迭代记录。完整问题记录见 [DEVELOPMENT.md](DEVELOPMENT.md)。

## 功能里程碑

- **接入文档检查（2026-11-17）**：接入单项目规范（spec 2.1.3 / repo-kit 2.7.2，`link-only`）；新增 `schema/`、`tools/repo-kit/`、`kit.lock` 与 CI；只查链接，不要求 frontmatter；既有 `build-exe.yml` 保持不变，新增的 `repo-check.yml` 与之并存
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
