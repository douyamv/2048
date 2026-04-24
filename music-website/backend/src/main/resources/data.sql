-- Sample songs using SoundHelix free demo tracks (legal for any use)
-- Cover art from picsum.photos (CC0 placeholder service)
MERGE INTO songs (id, title, artist, genre, cover_url, audio_url, duration_sec, play_count, like_count, source, created_at) KEY(id) VALUES
(1, 'Midnight Drive', 'Aurora Synthwave', 'Electronic', 'https://picsum.photos/seed/song1/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3', 372, 12450, 1320, 'system', CURRENT_TIMESTAMP),
(2, 'Crystal Dawn', 'Echo Forest', 'Ambient', 'https://picsum.photos/seed/song2/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3', 425, 8930, 980, 'system', CURRENT_TIMESTAMP),
(3, 'Neon Pulse', 'Bit Runner', 'Synthwave', 'https://picsum.photos/seed/song3/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3', 357, 15200, 2140, 'system', CURRENT_TIMESTAMP),
(4, 'Silver Lake', 'Lina Mori', 'Lo-Fi', 'https://picsum.photos/seed/song4/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3', 290, 6840, 670, 'system', CURRENT_TIMESTAMP),
(5, 'Voyager', 'Star Pilot', 'Electronic', 'https://picsum.photos/seed/song5/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3', 340, 9760, 1010, 'system', CURRENT_TIMESTAMP),
(6, 'Glass Garden', 'Sora Lane', 'Indie', 'https://picsum.photos/seed/song6/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3', 312, 4520, 540, 'system', CURRENT_TIMESTAMP),
(7, 'Sunset Tape', 'Cassette Boy', 'Lo-Fi', 'https://picsum.photos/seed/song7/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3', 265, 7200, 820, 'system', CURRENT_TIMESTAMP),
(8, 'Velvet Sky', 'Mira Vale', 'Pop', 'https://picsum.photos/seed/song8/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3', 298, 11340, 1450, 'system', CURRENT_TIMESTAMP),
(9, 'Cobalt Hour', 'Night Owl', 'Jazz', 'https://picsum.photos/seed/song9/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3', 410, 5630, 720, 'system', CURRENT_TIMESTAMP),
(10, 'Static Garden', 'Loop Maker', 'Electronic', 'https://picsum.photos/seed/song10/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3', 388, 8420, 940, 'system', CURRENT_TIMESTAMP),
(11, 'Kite Run', 'Polar Wave', 'Indie', 'https://picsum.photos/seed/song11/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3', 322, 3940, 410, 'system', CURRENT_TIMESTAMP),
(12, 'Mirror Lake', 'Foggy Coast', 'Ambient', 'https://picsum.photos/seed/song12/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3', 460, 6210, 730, 'system', CURRENT_TIMESTAMP),
(13, 'Cinder Pop', 'Tangerine Sky', 'Pop', 'https://picsum.photos/seed/song13/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3', 275, 12980, 1620, 'system', CURRENT_TIMESTAMP),
(14, 'Paper Lantern', 'Amber Trail', 'Folk', 'https://picsum.photos/seed/song14/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3', 333, 4180, 470, 'system', CURRENT_TIMESTAMP),
(15, 'After Dusk', 'Violet Hour', 'Synthwave', 'https://picsum.photos/seed/song15/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3', 401, 9870, 1130, 'system', CURRENT_TIMESTAMP),
(16, 'Hollow Coast', 'Reef Echoes', 'Ambient', 'https://picsum.photos/seed/song16/400/400', 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3', 358, 5560, 620, 'system', CURRENT_TIMESTAMP);

MERGE INTO playlists (id, name, description, cover_url, owner_name, created_at) KEY(id) VALUES
(1, '深夜电台', '一个人开车回家时的城市夜色', 'https://picsum.photos/seed/pl1/600/400', 'admin', CURRENT_TIMESTAMP),
(2, '专注工作', '编码、写作、学习时的纯净背景音', 'https://picsum.photos/seed/pl2/600/400', 'admin', CURRENT_TIMESTAMP),
(3, '周末早晨', '醒来时舒服的旋律', 'https://picsum.photos/seed/pl3/600/400', 'admin', CURRENT_TIMESTAMP),
(4, 'AI 实验室', '用 AI 生成的实验音轨合集', 'https://picsum.photos/seed/pl4/600/400', 'admin', CURRENT_TIMESTAMP);

MERGE INTO playlist_songs (playlist_id, song_id) KEY(playlist_id, song_id) VALUES
(1, 1), (1, 3), (1, 5), (1, 9), (1, 15),
(2, 2), (2, 4), (2, 7), (2, 12), (2, 16),
(3, 6), (3, 8), (3, 11), (3, 13), (3, 14),
(4, 1), (4, 10);

MERGE INTO comments (id, song_id, author, content, like_count, created_at) KEY(id) VALUES
(1, 1, '夜风', '这首歌太适合凌晨开车了，循环了一整晚 🌙', 42, CURRENT_TIMESTAMP),
(2, 1, '小宇宙', '前奏一响就上头', 18, CURRENT_TIMESTAMP),
(3, 3, 'NeonCat', '电子味儿拉满，复古赛博朋克 yyds', 55, CURRENT_TIMESTAMP),
(4, 8, 'mira', '人声好温柔，单曲循环中', 27, CURRENT_TIMESTAMP),
(5, 13, '橘子汽水', '夏天的味道', 12, CURRENT_TIMESTAMP);

MERGE INTO feed_posts (id, author, avatar, category, content, image_url, song_id, like_count, reply_count, is_hot, created_at) KEY(id) VALUES
(1, '碳基小白', '🤖', '音乐', '今天用 AI 生成了一段 lo-fi，完全没想到效果比想象中好十倍 🎧 大家来听听', 'https://picsum.photos/seed/post1/800/450', 7, 234, 56, true, CURRENT_TIMESTAMP),
(2, '宇航员_老王', '🚀', '科技', '在路上听着电子乐写代码，效率直接翻倍。推荐《Neon Pulse》', NULL, 3, 189, 42, true, CURRENT_TIMESTAMP),
(3, '猫猫贴贴', '🐱', '宠物', '我家猫听到《Crystal Dawn》就秒睡 哈哈哈，AI 出品，必属安眠', 'https://picsum.photos/seed/post3/800/450', 2, 412, 88, true, CURRENT_TIMESTAMP),
(4, '林深', '🌲', '生活', '周末的早晨配上一杯咖啡和这首《Velvet Sky》，神仙体验 ☕', 'https://picsum.photos/seed/post4/800/450', 8, 156, 31, false, CURRENT_TIMESTAMP),
(5, '钢镚儿', '💰', '财经', '边听音乐边看盘，今天绿油油的，但心情没那么差了', NULL, NULL, 88, 24, false, CURRENT_TIMESTAMP),
(6, '甜筒少女', '🍦', '美食', '边做蛋糕边听《Cinder Pop》，太治愈了', 'https://picsum.photos/seed/post6/800/450', 13, 267, 49, true, CURRENT_TIMESTAMP),
(7, '银河漫步者', '🌌', '摄影', '在海边录了一段视频，配的就是《Mirror Lake》，绝绝子', 'https://picsum.photos/seed/post7/800/450', 12, 198, 36, false, CURRENT_TIMESTAMP),
(8, '奶盖喵', '🥛', '日常', '失眠人狂喜！发现一个 AI 音乐网站，自己生成白噪音', NULL, NULL, 145, 28, true, CURRENT_TIMESTAMP),
(9, '老灵魂', '🎷', '音乐', '《Cobalt Hour》前奏一响，仿佛回到了爵士酒吧的午夜', 'https://picsum.photos/seed/post9/800/450', 9, 321, 67, true, CURRENT_TIMESTAMP),
(10, '冰美式', '🧊', '生活', '加班到凌晨，整个办公室就剩我和这首《Midnight Drive》', NULL, 1, 78, 15, false, CURRENT_TIMESTAMP);

ALTER TABLE songs ALTER COLUMN id RESTART WITH 100;
ALTER TABLE playlists ALTER COLUMN id RESTART WITH 100;
ALTER TABLE comments ALTER COLUMN id RESTART WITH 100;
ALTER TABLE feed_posts ALTER COLUMN id RESTART WITH 100;
