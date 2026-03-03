from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
import re
import os
import datetime
import logging

# 配置日志（只配置一次，避免重复）
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 初始化FastAPI
app = FastAPI(docs_url=None, redoc_url=None)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 修复后的安全查找函数（关键：参数顺序适配BeautifulSoup）
def safe_find(soup_elem, name=None, attrs=None,** kwargs):
    """
    安全查找标签，适配BeautifulSoup的find方法参数规则
    :param soup_elem: 父元素（可为None）
    :param name: 标签名（如"meta"）
    :param attrs: 属性字典（如{'name': 'publish_time'}）
    :param kwargs: 其他参数
    :return: 找到的标签或None
    """
    if soup_elem is None:
        return None
    # 调用BeautifulSoup的find方法，避免参数冲突
    return soup_elem.find(name=name, attrs=attrs, **kwargs)

# 解析B站链接核心函数
def parse_bilibili_video(url: str):
    try:
        logger.debug(f"解析B站链接：{url}")
        # 1. 处理短链接（单独判空，避免重定向失败）
        final_url = url
        if url.startswith("https://b23.tv/"):
            try:
                resp = requests.head(url, allow_redirects=True, timeout=5)
                final_url = resp.url
                logger.debug(f"短链接跳转后：{final_url}")
            except Exception as e:
                logger.warning(f"短链接解析失败，使用原链接：{e}")
                final_url = url

        # 2. 请求B站页面（强制编码+超时）
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        
        resp = requests.get(final_url, headers=headers, timeout=10, verify=False)  # 关闭SSL验证（本地环境兼容）
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        logger.debug("B站页面解析完成")

        # ===== 3. 提取标题 =====
        title = "未知标题"
        title_meta = safe_find(soup, name="meta", attrs={"property": "og:title"})
        if title_meta and title_meta.get("content"):
            title = title_meta["content"].replace("_哔哩哔哩_bilibili", "").strip()
            logger.debug(f"Meta标题：{title}")
        
        # ===== 4. 提取UP主 =====
        author = "未知UP主"
        author_meta = safe_find(soup, name="meta", attrs={"property": "og:author"})
        if author_meta and author_meta.get("content"):
            author = author_meta["content"].strip()
            logger.debug(f"Meta作者：{author}")
         # UP主兜底
        if author == "未知UP主":
            up_div = safe_find(soup, name="div", attrs={"class": "up-detail-top"})
            up_a = safe_find(up_div, name="a")
            if up_a and up_a.get_text():
                author = up_a.get_text(strip=True)
                logger.debug(f"层级标签UP主：{author}")
        
        # ===== 5. 提取年份 =====
        year = "n.d."
        page_text = soup.get_text()  # 预存页面全文，用于全局匹配
        # 提取div类型的pubdate-ip-text（你确认的标签）
        logger.debug("方式1：提取div.pubdate-ip-text标签...")
        pubdate_div = safe_find(soup, name="div", attrs={"class": "pubdate-ip-text"})
        if pubdate_div and pubdate_div.get_text(strip=True):
            pubdate_text = pubdate_div.get_text(strip=True)
            logger.debug(f"pubdate-ip-text内容：{pubdate_text}")
            year_match = re.search(r"\d{4}", pubdate_text)
            if year_match:
                year = year_match.group(0)
                logger.debug(f"提取年份：{year}")
        
        # 6. 返回结果（确保无None）
        result = {
            "author": author or "未知UP主",
            "year": year or "n.d.",
            "title": title or "未知标题",
            "url": final_url
        }
        logger.debug(f"最终解析结果：{result}")
        return result

    except requests.exceptions.Timeout:
        logger.error("访问B站超时", exc_info=True)
        raise HTTPException(status_code=500, detail="访问B站超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        logger.error(f"访问B站失败：{e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"无法访问B站链接：{str(e)}")
    except Exception as e:
        logger.error(f"解析失败（终极兜底）：{e}", exc_info=True)
        # 即使解析出错，也返回兜底数据，避免前端500
        return {
            "author": "未知UP主",
            "year": "n.d.",
            "title": "未知标题",
            "url": url
        }

# B站解析接口
@app.get("/parse-bilibili")
async def api_parse_bilibili(url: str):
    if not url or not url.startswith(("https://www.bilibili.com/", "https://b23.tv/")):
        raise HTTPException(status_code=400, detail="请输入有效的B站视频链接（以https://www.bilibili.com/或https://b23.tv/开头）")
    try:
        return parse_bilibili_video(url)
    except Exception as e:
        # 接口层终极兜底，永不返回500
        logger.error(f"接口层异常：{e}", exc_info=True)
        return {
            "author": "未知UP主",
            "year": "n.d.",
            "title": "未知标题",
            "url": url
        }

# 前端页面
@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

# 修复favicon.ico路由（核心：直接返回文件，不依赖全局挂载）
@app.get("/favicon.ico")
async def favicon():
    # 检查favicon.ico是否存在（和app.py同目录）
    ico_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if os.path.exists(ico_path):
        # 返回ico文件，指定正确的媒体类型 + 禁用缓存
        return FileResponse(
            ico_path, 
            media_type="image/x-icon",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    else:
        # 文件不存在时返回404，但不影响页面显示
        logger.warning(f"favicon.ico文件不存在：{ico_path}")
        return {"detail": "favicon.ico not found"}, 404

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=7860,
        log_level="debug",
        access_log=True
    )