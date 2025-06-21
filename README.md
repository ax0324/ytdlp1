# yt-dlp Render API

## 如何部署到 Render

1. 上传此项目到你的 GitHub。
2. 打开 https://render.com ，新建 Web Service。
3. 设置启动命令：
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
4. 添加环境变量：
```
API_KEY=ax9657.@
```
5. 部署完成！你可以通过 API 使用：
- /api/info?url=xxx
- /api/audio?url=xxx
- /api/cover?url=xxx