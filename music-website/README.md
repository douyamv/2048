# 碳基音浪 (Carbon Wave)

一个仿 ai6666.com 风格的音乐 + 社区网站。前端原生 HTML/CSS/JS，后端 Java + Spring Boot + Maven，H2 文件库。

## 功能

- 🎵 **歌曲库**：浏览、搜索、分类、播放计数、点赞、评论
- 📻 **歌单**：创建、增删歌曲、播放全部
- 🎼 **教父 AI 音乐**：调用 Replicate `musicgen` 真实生成；未配置 token 时使用兜底音轨
- 🌍 **碳基圈信息流**：分类发帖、点赞、热榜
- 🎧 **全局播放器**：固定底部，连续播放，进度条、音量
- 无登录，按本地昵称交互

## 目录

```
music-website/
├── backend/    Spring Boot 3 + JPA + H2 文件库
└── frontend/   静态页面，由后端直接 serve
```

## 启动

需要 JDK 17+ 和 Maven。

```bash
cd backend
mvn spring-boot:run
```

打开 http://localhost:8080 即可。

H2 控制台：http://localhost:8080/h2-console
- JDBC URL: `jdbc:h2:file:./data/musicdb;AUTO_SERVER=TRUE`
- 用户: `sa`，密码留空

数据文件存放在 `backend/data/` 下，重启后保留。

## 开启真实 AI 音乐生成

默认使用 Replicate 的 `musicgen` 模型。设置环境变量后启动：

```bash
export REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxxxxxx
cd backend && mvn spring-boot:run
```

未设置 token，或调用失败时，系统会自动从 SoundHelix 公共演示音轨中随机选一首作为兜底，保证用户始终能听到音频。

更换模型版本：编辑 `backend/src/main/resources/application.yml` 中的 `ai.replicate.model-version`。

## 主要 API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/songs` | 歌曲列表（支持 `genre`, `page`, `size`） |
| GET | `/api/songs/hot` | 热门 Top 10 |
| GET | `/api/songs/latest` | 最新 12 |
| GET | `/api/songs/search?q=` | 搜索 |
| POST | `/api/songs/{id}/play` | 播放计数 +1 |
| POST | `/api/songs/{id}/like` | 点赞 +1 |
| GET/POST | `/api/playlists` | 歌单 |
| POST | `/api/playlists/{id}/songs/{songId}` | 加入歌单 |
| GET/POST | `/api/comments` | 评论 |
| GET/POST | `/api/feed` | 碳基圈 |
| POST | `/api/feed/{id}/like` | 点赞动态 |
| GET | `/api/ai/status` | 检查 AI 是否已配置 |
| POST | `/api/ai/generate` | 生成音乐 |
| GET | `/api/ai/generations` | 最近 20 个生成结果 |

## 关于音频版权

- 示例曲库使用 [SoundHelix](https://www.soundhelix.com/audio-examples) 的免费演示音轨，可自由用于演示用途
- 封面图来自 [picsum.photos](https://picsum.photos/)（CC0）
- AI 生成音乐由 Replicate `musicgen` 实时合成，归创作者所有
