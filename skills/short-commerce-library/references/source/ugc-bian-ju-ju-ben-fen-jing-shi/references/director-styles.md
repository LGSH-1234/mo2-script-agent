# 多导演风格适配库 · 完整版

> **核心原则**：风格要服务主题，模仿中要创新，情感要跨风格。
> 每个导演风格都拆解为可执行的叙事结构 + 视觉词典 + 分镜特征 + 提示词模板。

---

## 一、各导演风格完整档案

### 1. 王家卫

**叙事结构：** 碎片化叙事 / 情感驱动的非线形 / 时间跳跃

**哲学主题：** 孤独 / 错过 / 记忆 / 都市疏离 / 时间流逝

**视觉词典：**
```
色彩空间：浓郁饱和的红、绿、蓝 + 霓虹灯光 + 高对比度
主色调：暗红(#8B0000) / 墨绿(#2F4F2F) / 琥珀金(#FFBF00)

构图特征：倾斜构图 / 框架式构图（窗框/门框/镜框）/
           反射镜像（水/玻璃/后视镜）/ 大面积负空间

运镜语言：抽帧慢动作(22fps降18fps再还原) /
           手持跟拍 / 旋转环绕 / 升降悬停

光学参数：广角24-35mm + 大光圈f/1.4-f/2 + 近距离摄影
           浅景深 + 前景虚化色散

光影设计：城市霓虹(4000K-5500K) + 钨丝暖光(2800K)混色 /
           窗光侧45°柔光 / 夜雨中倒影光斑

色彩粒理：胶片颗粒 + 光斑虚化 + 色彩偏移 / 抽帧卡顿感 /
           过曝高光 + 暗部提灰

标志性元素：时钟/日历/日期标题卡 / 雨/雨滴在玻璃 /
            烟雾/香烟 / 食品特写（罐头/速食）/ 旗袍/
            独白旁白 / 高跟鞋脚步声 / 旧式电扇
```

**分镜特征：**
```
景别偏好：特写→大特写（极近拍脸/道具） + 全景（环境孤寂）
转场方式：叠化（叠化时长比其他风格长30%）/ 匹配剪辑（动作/烟雾/雨）
景别节奏：特写→全景→特写（两极跳，中间不插中景）
目光方向：人物几乎不看镜头 = 沉浸在自己的世界
人物构图：通常偏画左或画右1/3，另一侧大面积留白
```

**文生图提示词模板：**
```
Close-up shot, 35mm lens, f/1.4 shallow depth of field,
[主体描述] + @CharID:XXX, face partially obscured by cigarette smoke,
neon light mixed with warm tungsten 2800K from side,
rain streaks on window pane in foreground bokeh,
dominant color: deep red (#8B0000) with emerald green (#2F4F2F) accents,
18fps stutter motion feel, film grain, chromatic aberration on highlights,
slightly overexposed skin tones with lifted shadows,
negative space occupying right 2/3 of frame,
--ar 16:9 --style raw --s 250 --v 6.1
--no plastic skin, airbrushed, clean digital look, cinematic feel
```

---

### 2. 克里斯托弗·诺兰

**叙事结构：** 非线性时间折叠 / 高概念前提 / 多时间层交织

**哲学主题：** 时间 / 记忆 / 身份 / 存在意义 / 牺牲与救赎

**视觉词典：**
```
色彩空间：自然真实色调 + 冷峻蓝色(#4A708B) + 温暖琥珀(#D2691E)
          高对比度 + 暗部扎实

构图特征：宏观微观对比 / 对称构图（建筑/空间站）/
           广阔景观 / 人物偏中下（宏大留白在上）

运镜语言：IMAX级实拍运动 / 手持跟拍（紧张感）/
           缓慢推近（聚焦关键信息）/ 360°环绕（概念展示）

光学参数：广角14-24mm（大场景）+ 中焦50-85mm（人物）
          深景深f/8-f/11（IMAX广角）+ 浅景深f/2.8（特写）

光影设计：自然光优先 / 实景光效 / 高对比低调光 /
           主光硬朗(侧光+顶光) / 暗部细节保留

色彩粒理：胶片IMAX质感 / 真实颗粒 / 极简CGI / 真实物理破坏 /
           无多余色彩分层 / 色温自然度极高

标志性元素：陀螺 / 怀表 / 多重梦境 / 时间倒转 /
            旋转走廊 / 雪地/沙漠 / 极简会议桌 /
            都市夜景直升机航拍 / 特殊时间装置
```

**分镜特征：**
```
景别偏好：大远景→特写两极切换（宏大+聚焦）
转场方式：匹配剪辑（动作匹配/形状匹配）/ 硬切（节奏感）
时间标识：地点+时间字幕叠加 / 视觉锚点区分时间层
对白方式：快速剪接+对白重叠 / exposition通过画面展示
视觉层级：广角建立空间 → 中景解释机制 → 特写揭示情感
```

**文生图提示词模板：**
```
Wide establishing shot, 14mm IMAX lens, f/11 deep focus,
[场景描述] + @SceneID:XXX, massive scale with human figure
occupying lower-center 1/5 of frame,
natural cold steel blue (#4A708B) concrete corridors with
warm amber (#D2691E) light leaking from distant source,
hard key light from 45-degree top-side, contrast ratio 4:1,
dark shadows with preserved detail, IMAX film grain,
practical SFX aesthetic, minimalist sci-fi texture,
macro-micro scale contrast emphasized,
--ar 16:9 --style raw --s 180 --v 6.1
--no plastic, airbrushed, over-saturated, lens flare gimmick
```

---

### 3. 韦斯·安德森

**叙事结构：** 章节式叙事 / 独立分段 / 并列结构

**哲学主题：** 童年 / 家庭 / 异想天开的冒险 / 古怪中的温暖

**视觉词典：**
```
色彩空间：高饱和pastel色调 + 每场景单一主色(#FFB6C1/#87CEEB/#F5DEB3)
          完美配色组合 + 平面化色彩

构图特征：绝对中心对称 / 平面化横移 / 二分法 /
           正视角(90°)俯拍（桌面/Bed） / 微缩模型感

运镜语言：轨道横移（90°pan） / 垂直升降 / 精准推拉 /
           追踪横移（人物从画左走向画右）

光学参数：中焦40-65mm（无畸变） + 光圈f/4-f/5.6（整体清晰）
          无鱼眼无广角变形

光影设计：均匀柔光 / 无强烈阴影 / 戏剧化布光（舞台感） /
           每场一盏主色灯 / 边界清晰

色彩粒理：微缩模型感 / 精緻手工质感 / 纹理化（木纹/布料）/
           色彩分离（每物每色清晰独立）

标志性元素：对称构图 / 大家族合照 / 横移展示房间剖面 /
            黄色粗体字幕 / 复古道具 / 新浪潮配乐 /
            慢动作行走 / 独立小章节标题卡
```

**分镜特征：**
```
景别偏好：全景（对称建立）→中景（对话横移）→特写（道具）
运镜法则：横移是主要语言（人物+镜头同步90°pan）
构图铁律：绝对对称/平面化/正俯桌拍/正对建筑
节奏特征：快速工整 / 精确节奏 / 无手持晃
转场方式：横移转场 / 章节标题卡 + 硬切
```

**文生图提示词模板：**
```
Centered symmetrical wide shot, 50mm lens, f/5.6,
[场景描述] + @CharID:XXX positioned at exact center,
pastel color palette with single dominant color [HEX#XXX],
tracking lateral dolly movement,
precisely arranged objects with handmade miniature feel,
flat lighting with no harsh shadows, theatrical illumination,
textured retro wallpaper and fabric visible in detail,
color separation — every object its own distinct shade,
--ar 16:9 --style raw --s 200 --v 6.1
--no distortion, handheld, shallow depth of field, cinematic feel
```

---

### 4. 蒂姆·伯顿

**叙事结构：** 哥特童话 / 英雄旅程 / 怪异与边缘

**哲学主题：** 怪异中的美丽 / 孤独者的归属 / 黑暗外表下的纯真

**视觉词典：**
```
色彩空间：黑白对比 + 深紫黑(#2B1B2B) + 金属铁灰(#4A4A4A) +
          荧光色点缀(绿#39FF14/紫#BF00FF)
          低饱和整体 + 局部荧光高饱和

构图特征：扭曲透视 / 螺旋元素 / 哥特建筑框 /
           夸张比例（大头小身/长腿/高帽） /
           倾斜角度 / 不对成

运镜语言：诡异的升降 / 突然的变焦推进(急推) /
           梦幻旋转 / 低角度仰视 / 乌鸦/蝙蝠跟随视角

光学参数：广角变形28mm（夸张） + 长焦压缩135mm（孤立）
          大光圈f/1.4（浅景深分离主体与哥特背景）

光影设计：戏剧性明暗(chiaroscuro) / 顶光底光混合 /
           强侧光 + 边缘光 / 阴影条纹(百叶窗/栏杆投影) /
           冷光为主偶尔暖光(唯一温暖光源)

色彩粒理：手绘/水彩质感 / 定格动画感 /
           编织纹理 / 暗部粗糙颗粒 /
           赛璐璐动画染色

标志性元素：苍白皮肤 + 黑眼圈 / 螺旋/条纹图案 /
            哥特尖顶 / 骷髅/蝙蝠/南瓜 /
            剪刀手/机械针脚 / 夸张发型 /
            浓重的戏剧化化妆
```

**分镜特征：**
```
景别偏好：特写（脸部夸张特征）→ 大远景（哥特环境）→ 中景
运动语言：低角度仰拍 + 急推变焦（揭示时刻）
构图特征：螺旋/条纹作为视线引导 / 主体偏下/偏边
色彩节奏：黑白或单色为主→彩色道具/角色穿插
转场方式：叠化（雾气/黑暗过渡）/ 形状匹配（螺旋对螺旋）
```

**文生图提示词模板：**
```
Extreme close-up, 28mm wide-angle lens, f/1.4,
[角色] + @CharID:XXX, pale skin with dark eye circles,
black and white striped outfit, exaggerated proportions,
chiaroscuro lighting with dramatic side key light and
green fluorescent accent (#39FF14) from below,
Gothic cathedral window frame in background,
deep purple-black shadows (#2B1B2B),
stop-motion texture, watercolor grain analogue feel,
spiral composition leading eye to subject's wide eyes,
--ar 16:9 --style raw --s 250 --v 6.1
--no plastic, smooth, airbrushed, digital clean, 3D render
```

---

### 5. 丹尼斯·维伦纽瓦

**叙事结构：** 缓慢铺陈的史诗叙事 / 沉默探索

**哲学主题：** 语言 / 沟通 / 文明碰撞 / 未知恐惧 / 存在主义

**视觉词典：**
```
色彩空间：极简主义调色板 + 每场景单一主导色 /
          沙漠橙褐(#C4A882) / 冷灰蓝(#6B7B8D) / 暗绿(#3B4A3B)
          色板极窄（每场不超过3色）

构图特征：巨物与微小人对比 / 对称但不对称中的对称 /
           地平线极低或极高 / 大面积单一材质 /
           人物常位于画框底部1/4

运镜语言：极慢推进（拍摄10分钟素材加速到30s）/
           缓慢横移（穿越感受） / 直升机宏大航拍 /
           稳定器中速跟随（人物穿越巨大空间）

光学参数：广角14-35mm（宏大环境） + 长焦200mm（压平巨物）
          适中光圈f/5.6-f/8（整体清晰但保留景深层次）

光影设计：自然光主导 / 魔幻时刻光 /
           单一强方向光（沙漠烈日/巨窗漏光） /
           暗部极暗但保留边缘轮廓 /
           光比巨大(6:1-10:1)

色彩粒理：超35mm胶片 / 低饱和度(降低20-30%饱和) /
           高锐度 / 颗粒感适中 /
           无多余视觉信息 / 材质感(沙/石/布料/金属)

标志性元素：巨型几何体 / 沙尘 / 沉默的人物行走 /
            语言符号 / 虫壳飞行器 / 超规格建筑 /
            多人安静看向同一方向 / 巨物遮天蔽日
```

**分镜特征：**
```
景别偏好：大远景（建立巨物感）→ 中景（人物反应）→ 大特写（细节/音效触发）
节奏特征：极慢 / 停留时间长(比正常长2-3倍) / 沉默段落
声音设计：低频轰鸣 / 沉默是重要元素 / 突然的音效冲击
转场方式：叠化（慢到几乎感觉不到）/ 黑暗过渡 / 声音桥
```

**文生图提示词模板：**
```
Extreme wide shot, 14mm lens, f/8 deep focus,
[场景描述] + @SceneID:XXX, tiny human figure at bottom 1/4
of frame, massive geometric structure dominating upper 3/4,
single dominant color desert sand (#C4A882),
monumental silence atmosphere, natural harsh sunlight
from high desert sun, contrast ratio 8:1,
extremely low saturation (-30%), fine film grain,
enormous negative space, texture of sand and stone visible,
mineral and textile materiality emphasized,
--ar 16:9 --style raw --s 180 --v 6.1
--no people smiling, over-saturated, fast pace, commercial look
```

---

### 6. 昆汀·塔伦蒂诺

**叙事结构：** 章节式暴力叙事 / 非线性章节 / 长篇对话

**视觉词典：**
```
色彩：高饱和黄(#FFD700) + 饱和红(#DC143C) + 蓝色时刻(#1E3F5A)
       饱和度极高(+20%)

构图：低角度仰拍（人物高大化） / 车内地板镜头 /
      后备箱视角(POV) / 长镜头对话对称

运镜：轨道横移（走进场景） / 缓慢变焦推近（紧张） /
      后备箱/行李箱开盖镜头 / 360°车内环绕

光影：高对比 / 艳阳高照 / 强烈顶光 / 车内半明半暗
      霓虹灯管色光 / 工业照明

标志性：脚部特写 / 后备箱POV / 酒馆/汽车旅馆 /
        汽车里对话 / 某角色突然喷血 / 章节标题卡 /
        对话+突然暴力 / 音乐反差(欢乐配暴力)
```

---

### 7. 是枝裕和

**叙事结构：** 日常细腻叙事 / 生活流 / 平淡中的爆破

**视觉词典：**
```
色彩：低饱和自然色 / 白色+米色+浅灰 / 透亮绿色
      色温自然 5200-5600K

构图：固定机位 / 中景为主 / 门框/窗框框架构图 /
      多人横排（日式客厅常见） / 食物特写

运镜：极少量运镜 / 固定长镜为主 / 缓慢横移（跟随动作）
      大部分时间摄像机不动

光影：自然光最大利用 / 窗户透光 / 柔光漫射 /
      阴影柔和过渡 / 无人工感

标志性：做饭/吃饭场景 / 走路场景（日常通勤） /
        对话不看对方 / 沉默的留白 /
        海边/森林散步 / 廉价公寓细节
```

---

## 二、跨风格融合指南

### 融合规则
```
主风格占60%叙事结构 + 副风格占40%视觉语言
或：主风格占60%视觉语言 + 副风格占40%叙事结构
```

**推荐融合组合：**
| 融合 | 叙事结构 | 视觉语言 | 示例 |
|------|---------|---------|------|
| 诺兰×王家卫 | 时间折叠 | 浓郁色彩+抽帧 | 一段记忆的物理性回溯 |
| 维伦纽瓦×王家卫 | 缓慢史诗 | 浓郁红绿+抽帧 | 沙漠孤独者的内心独白 |
| 韦斯·安德森×昆汀 | 章节式 | 高饱和+低角度 | 古怪黑帮的对称冒险 |
| 蒂姆·伯顿×是枝裕和 | 哥特童话 | 自然光+安静 | 怪小孩的质朴日常 |

### 融合声明格式
```
【风格融合声明】
叙事骨架：[主风格名]（占比60%）
视觉语言：[副风格名]（占比40%）
融合关键：[具体哪个视觉特征融入哪个叙事层面]
示例：诺兰的时间非线性叙事 + 王家卫的情感浓郁视觉 = 
      "一段在物理世界倒流的情感记忆"
```

---

## 三、风格快速匹配表

```
用户关键词                → 推荐风格
───────────────────────────────────────
哲学思辨 / 时间 / 记忆    → 诺兰
情感细腻 / 错过 / 孤独    → 王家卫
对称 / 古怪 / 幽默        → 韦斯·安德森
哥特 / 黑暗 / 童话        → 蒂姆·伯顿
史诗 / 沉默 / 宏大        → 维伦纽瓦
暴力 / 黑色 / 娱乐        → 昆汀
日常 / 温情 / 家庭        → 是枝裕和
虚实 / 心理 / 超现实      → 今敏
励志 / 热血 / 梦想        → 岩井俊二（清新）/ 周星驰（无厘头）
科技 / 赛博 / 冷峻        → 雷德利·斯科特 / 丹尼斯·维伦纽瓦
古装 / 武侠 / 意境        → 张艺谋 / 王家卫（古装版）
混乱 / 疯狂 / 万花筒      → 盖·里奇 / 埃德加·赖特
```

---

## 四、风格提示词质量检查

```
□ 视觉风格是否可被识别为该导演（非"看起来像AI模仿"）？
   → 检查用词是否具体（不仅"王家卫风格"而在参数中体现抽帧/色板/构图）
□ 风格是否服务叙事主题，而非纯装饰？
   → 自问"把风格去掉，故事还在吗？"
□ 风格的标志性元素是否克制使用（不过载）？
   → 每场/每镜最多2-3个导演标志元素
□ 用户指定的风格是否覆盖全片一致性？
   → 所有镜头的色彩空间/构图法则/运镜逻辑统一
□ 跨风格融合是否有明确的主次关系和融合声明？
   → 必须说明"哪里用A风格，哪里用B风格"
```
