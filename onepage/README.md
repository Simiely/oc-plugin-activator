# OC插件快速激活工具 — 产品落地页

本页面基于 [hub-world/templates/template.html](https://github.com/Simiely/hub-world/tree/main/templates) 生成，提供一套 **深色主题、全屏滚动吸附** 的品牌推广页。

## 快速开始

1. **打开 `index.html`** — 直接在浏览器中预览效果
2. **修改 CONFIG 对象** — 打开文件，找到顶部 `var CONFIG = { ... }` 区块，替换内容
3. **部署** — 将完成的 HTML 部署到 GitHub Pages 或任何静态托管服务

### 注意事项

- **保持 CONFIG 所有键名不变**，不要删除或重命名字段
- **文本字段支持 HTML**：`<em>` 斜体强调，`<b>` 加粗，`<br>` 换行
- **不需要的内容留空字符串** `""` 即可
- **主题色统一**：修改 `accentColor` 一处即可全局换色
- **导航栏 GitHub 链接和版本号都跳转到 `repoUrl`**

## 页面结构

```
index.html
├── ★ CONFIG 对象（可编辑区域）
│   ├── pageTitle / brand / version
│   ├── accentColor
│   ├── hero { ... }           ← 首屏
│   ├── problem { ... }        ← 痛点屏
│   ├── features { ... }       ← 功能屏
│   ├── usage { ... }          ← 使用引导屏
│   ├── install { ... }        ← 安装指南屏
│   ├── cta { ... }            ← 行动号召屏
│   └── dotLabels [...]        ← 右侧导航点标签
│
├── CSS 样式（不需要修改）
├── HTML 骨架（不需要修改）
├── 渲染脚本（注入 CONFIG → DOM）
└── 交互脚本（滚动监听 / 导航点 / 视差效果）
```

## 模板特性

| 特性 | 说明 |
|------|------|
| 全屏滚动吸附 | `scroll-snap-type: y mandatory` |
| 入场动画 | 元素淡入上移，8 级延迟 |
| 鼠标视差 | 痛点屏径向渐变跟随鼠标 |
| 背景噪点 | SVG 噪点纹理叠加 |
| 响应式 | 860px / 520px 自适应 |
| 深色主题 | 暗色背景 + 玫瑰红强调色 |
| 无依赖 | 纯 HTML + CSS + JS |

## 文件清单

```
onepage/
├── index.html    ← 产品落地页
└── README.md     ← 本说明文档
```
