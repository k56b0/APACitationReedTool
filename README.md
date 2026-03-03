# APACitationReedTool：APA 格式引文生成工具

一键生成 APA 7th 规范引文，**重点支持 B 站视频链接自动解析**，同时兼容书籍、期刊手动录入，是学术写作、日常撰稿的高效辅助工具，让参考文献格式规范不再繁琐～

[![立即体验](https://img.shields.io/badge/立即体验-点击这里-brightgreen)](https://k56b0-apa-citation-tool.hf.space/)

------

## 📚 项目简介

一款部署于 Hugging Face Docker 环境的轻量网页工具，核心聚焦 APA 格式引文的快速生成。无需复杂配置，浏览器点开即用，支持：

- 🎬 B 站视频链接自动解析（作者、年份、标题一键填充）
- 📖 书籍、期刊信息手动录入
- 📱 全端自适应（电脑 / 移动端无缝适配）
- 📜 严格遵循 APA 7th 学术规范

**技术栈**：HTML/CSS/JS + Vue 3 + Bootstrap 5 + FastAPI + Hugging Face 部署

👉 项目地址：https://github.com/k56b0/APACitationReedTool

------

## 🎯 应用背景

APA 格式（American Psychological Association）是全球通用的学术引用规范，广泛适用于论文、报告、课题等场景，核心优势一目了然：

1. 🌍 通用性强：学校、期刊、平台普遍认可
2. 📝 格式简洁：核心结构「作者（年份）. 标题。来源」，无需死记复杂规则
3. 🧩 兼容广泛：支持网页、视频、书籍、期刊等多类型资源
4. ⚡ 高效省心：自动处理标点、斜体、格式对齐，告别手动排版错误

### ✨ 工具核心亮点

表格

| **特性**     | **详情**                                                     |
| ------------ | ------------------------------------------------------------ |
| 学术级规范   | 严格遵循 APA 7th 标准，兼容《文学遗产》等核心期刊排版体例，直接满足投稿要求 |
| 零门槛上手   | 无需安装、无需配置，浏览器访问即使用，非技术人员也能快速上手 |
| B 站专属优化 | 本地部署支持 B 站链接自动解析，免去手动录入繁琐，提升写作效率 |
| 全端自适应   | 适配电脑、手机等各类设备，随时随地生成引文                   |

------

## 🚀 本地部署指南

### 前置准备

- 推荐编辑器：Visual Studio Code
- 运行环境：Python 3.9+

### 安装步骤

1. 克隆项目至本地，进入项目根目录（`app.py` 所在文件夹）

2. 打开终端，执行依赖安装命令：

   `pip install -r requirements.txt`

3. 启动服务：

   `python app.py`

4. 浏览器访问 `http://localhost:7860`，即可使用（本地网络无访问限制，支持 B 站解析）

### 卸载方法

1. 生成已安装依赖清单（项目根目录执行）：

   `pip freeze > requirements.txt`

2. 批量卸载依赖：

   `pip uninstall -r requirements.txt -y`

3. （可选）清理缓存，验证卸载结果：

   ```bash
   # 清理pip缓存
   pip cache purge
   
   # 验证残留（Windows）
   pip list | findstr "fastapi requests bs4 uvicorn"
   
   # 验证残留（Mac/Linux）
   pip list | grep "fastapi requests bs4 uvicorn"
   ```

------

## ❓ 常见问题

### 1. B 站链接解析功能无法使用？

- 原因：B 站对服务器 IP 爬虫有限制，Hugging Face 线上部署环境无法正常访问；
- 解决方案：通过「本地部署」使用，私人 IP 地址无访问限制，可正常解析 B 站链接。

### 2. 如何反馈 BUG 或建议？

- 欢迎在 GitHub 项目的「Issues」区提交详细的 BUG 描述、复现步骤或功能建议，我们会及时响应优化。

------

## 📌 更新说明

本工具持续迭代更新中，后续将新增更多资源类型支持、格式自定义等功能，欢迎 Star 关注项目动态～

若有个性化需求或技术问题，可通过 GitHub 联系开发者交流！
