
---
name: pov-character-video
description: Generate production-ready video prompts for 小云雀 when the user wants a POV/first-person interactive video built around an uploaded character image. Use this skill whenever the request involves 第一视角、POV、与上传角色互动、陪伴感、恋爱感、宠物式陪伴、治愈陪伴、搞笑反差、Q版3D可爱角色、真实环境中的角色互动，even if the user does not explicitly ask for a prompt. This skill is especially suitable when the user wants a 9:16 vertical video with real-world lighting, preserved character traits, visible first-person hands/body presence, and no subtitles, text, logo, or watermark.
---

# POV Character Video

为“小云雀”生成可直接使用的成品级视频提示词，核心任务是：

- 把**用户上传的角色图**转化为视频中的互动主角
- 使用**POV / 第一人称视角**构建沉浸式关系
- 让角色处于**现实世界环境**中，但保留**3D、Q版、可爱化**表现
- 输出适合“小云雀”的**完整视频 prompt**

## 何时使用

当用户出现以下意图时，优先使用本 skill：

- 要求生成 **POV / 第一视角** 视频
- 要求让**上传角色和用户互动**
- 想做**宠物式陪伴 / 恋爱感 / 治愈陪伴 / 搞笑反差**视频
- 明确要求 **Q版 3D 可爱化**、但发生在**真实世界场景**
- 想把图片角色做成**陪伴型、互动型、沉浸型短视频**
- 虽然没说“提示词”，但明显是在要**小云雀视频生成用语**

## 默认约束

除非用户明确要求覆盖，否则默认采用以下规则：

- 视频比例：**9:16 竖屏**
- **禁止字幕、文字、logo、水印**
- **保留上传角色核心特征**，不要改成陌生角色
- 场景采用**真实环境、真实光影、真实空间透视**
- 角色表现为**3D Q版可爱化**，而不是二维平涂或纯写实人类
- 强调**第一人称镜头中的手部 / 身体存在感**，让“我”真实参与互动
- 互动必须是**用户与角色之间发生**，不要只让角色单独表演

## 工作方法

### 第一步：先识别用户要的互动关系

优先判断属于哪一类，再决定镜头语言与动作设计：

1. **宠物式陪伴**
   - 关键词：黏人、跟随、蹭蹭、求抱、撒娇、陪我出门、陪我回家
   - 气质：轻松、软萌、依赖、日常陪伴

2. **恋爱感**
   - 关键词：心动、暧昧、牵手、靠近、对视、接我下班、陪我散步
   - 气质：甜、克制、近距离、情绪细腻

3. **治愈陪伴**
   - 关键词：安慰、治愈、陪伴、低落时陪我、温暖、日常恢复能量
   - 气质：安静、柔和、稳定、安全感

4. **搞笑反差**
   - 关键词：反差萌、一本正经搞笑、角色很小但气场很强、夸张互动
   - 气质：节奏明确、动作反差、视觉笑点

如果用户没有明确说，就根据语气和场景自动选择最接近的一类；必要时在输出里给 2 个备选方向。

### 第二步：把“互动”写得具体

避免抽象词，比如“很有爱”“很治愈”。要改写成可拍摄、可生成的动作：

- 靠近镜头抬头看我
- 轻轻蹭我的手
- 拉住我的手指往前走
- 坐在我肩膀上回头对我笑
- 从桌面跳到我手心
- 站在我膝盖上递给我一个小物件
- 在我低头时突然闯入镜头，制造反差
- 假装很酷地下指令，但体型又很Q版可爱

### 第三步：强化 POV 的身体感

第一人称不能只写“POV”。应尽量体现“我”在现场：

- 我的手伸向角色
- 我的腿、膝盖、肩膀、手臂偶尔入镜
- 角色主动触碰我、拉我、蹭我、跳到我身上
- 镜头运动符合人的真实动作：低头、抬手、转身、迈步、坐下、起身

如果是强互动场景，优先让“角色对我做动作”，而不是只让它在前方表演。

### 第四步：处理视觉风格

需要同时满足两层：

1. **现实世界底座**
   - 真实街道、卧室、咖啡馆、公园、地铁口、客厅、办公桌、便利店等
   - 真实材质、真实景深、真实光线方向、真实空间关系

2. **角色表现**
   - 3D 建模感
   - Q版比例
   - 可爱、圆润、讨喜
   - 保留上传角色的颜色、轮廓、标志性特征、服饰元素或身份识别点

不要把“Q版”写成过度幼态、廉价玩具感、低幼卡通感。重点是“现实环境中的高完成度 3D 萌化角色”。

### 第五步：适配小云雀 prompt

输出时，默认给出**成品级一段式 prompt**，内容需包含：

- 视角设定
- 主体设定（上传角色如何出现）
- 场景设定
- 互动动作
- 镜头运动
- 光影与质感
- 风格约束
- 负面限制

## 输出格式

默认使用以下结构：

### 1. 创意方向
用 1-2 句话说明视频看点。

### 2. 成品 Prompt
直接给出可投喂小云雀的视频 prompt。

### 3. 关键执行点
用 3-5 个短点提炼这条 prompt 的执行重点，便于用户快速改写：
- 场景
- 互动动作
- 情绪氛围
- 镜头运动
- 风格约束

### 4. 可选加一个变体（如适合）
当用户需求较泛，或明显能延展成不同情绪版本时，再补 1-2 个方向：
- 更甜
- 更治愈
- 更搞笑
- 更像宠物陪伴

## Prompt 写法要求

生成 prompt 时，尽量自然、连续、可执行：

- 直接说明这是**POV第一人称视频**
- 说明角色来自**用户上传图片**，并要求保留核心特征
- 明确写出角色与“我”的互动动作
- 写清环境是真实世界，不是纯卡通世界
- 明确是**3D Q版可爱化角色**
- 写清真实光影、镜头运动、空间层次
- 明确 **9:16 vertical**
- 明确 **no subtitles, no text, no logo, no watermark**

## 推荐表达元素

可按需组合：

- POV first-person view
- visible hands / arms / lap / shoulder presence
- realistic environment and natural lighting
- chibi-style 3D character integrated into the real world
- preserve the uploaded character's iconic features
- intimate interaction / soothing companionship / playful contrast
- cinematic close-range movement
- natural occlusion and body-led camera motion

## 输出示例风格

### 示例 1：宠物式陪伴
**创意方向：**
一个现实客厅里的第一视角陪伴短片，上传角色被萌化成 3D Q版小伙伴，像宠物一样黏着“我”，不断蹭手、跳上膝盖、跟着镜头移动，氛围轻松治愈。

**成品 Prompt：**
POV first-person video, the main character is transformed from the user-uploaded character image, preserve the character's core visual traits and iconic details, rendered as a cute chibi 3D character integrated naturally into a real-world living room, realistic environment, realistic lighting, soft daylight through the window, visible first-person hand and lap presence, the tiny character runs toward me, rubs gently against my hand, hops onto my knee, looks up at me with a clingy and adorable expression, then circles around me and leans against my arm like a pet companion, natural body-led camera movement, slight head turns and hand interaction, intimate and healing atmosphere, high-quality 3D texture, realistic shadows and depth, cute but not childish, 9:16 vertical, no subtitles, no text, no logo, no watermark.

### 示例 2：恋爱感
**创意方向：**
在傍晚街头的第一视角里，Q版 3D 角色像偷偷来接我下班，轻轻拉住我的手往前走，甜但不过分夸张。

**成品 Prompt：**
POV first-person video in a real city street at dusk, transform the user-uploaded character into a cute chibi 3D version while preserving the original identity features, realistic sunset lighting, soft reflections on the road, visible first-person hand and subtle body presence, the character walks close to me, looks back with a shy smile, reaches out and gently holds my finger, leading me forward through the street, natural camera sway from walking, close-range emotional interaction, romantic but soft and believable, realistic world, cinematic depth, polished 3D cute styling, 9:16 vertical, no subtitles, no text, no logo, no watermark.

## 如果信息不完整

如果用户没有提供：
- 场景
- 情绪方向
- 互动方式

则不要停住不做。应：

1. 基于用户语义先补出一个最合理版本
2. 再给出 1-2 个可选变体
3. 只在确实影响结果时，简短指出“如果你愿意，我还能改成更甜 / 更搞笑 / 更治愈版本”

## 小云雀导向增强

为了让输出更贴近“小云雀”实际使用场景，优先把 prompt 写得：

- **画面指令明确**：不要只写概念词，要写出可视化动作和镜头变化
- **互动链路完整**：尽量包含“角色出现 → 靠近/互动 → 情绪落点”
- **单条 prompt 可直接用**：避免先讲方法、再讲解释，用户通常要的是成品
- **短视频感更强**：动作密度适中、镜头节奏清晰、单条画面记忆点明确
- **适合二创微调**：关键动作和情绪节点要清楚，便于用户后续改场景或改关系感

## 测试提示词样例

以下测试样例可用于验证 skill 是否稳定触发、且输出方向正确：

### 测试 1：宠物式陪伴
帮我做一个小云雀视频，我会上传一个角色图，把它变成现实世界里的 3D Q版可爱小伙伴。要第一视角，像它在家里一直黏着我，蹭我手、跳到我腿上，整体很治愈，竖屏。

### 测试 2：恋爱感互动
我想用上传的人物图生成一个 POV 恋爱感视频，场景是下班后的傍晚街头，对方轻轻拉住我的手带我往前走，真实环境，真实光影，角色要 Q版3D 但不能太幼稚。

### 测试 3：搞笑反差
给我写一个小云雀 prompt，我会上传角色图。我要第一人称视角，这个角色看起来很小只很Q版，但一本正经地指挥我做事，动作要有反差萌，现实办公桌场景，不能有字幕水印。

## 质量自检

输出前，检查是否同时满足：

- 是否明确写出 **POV / 第一人称**
- 是否明确写出 **用户上传角色图** 且保留核心特征
- 是否存在 **具体互动动作**，而不是空泛情绪词
- 是否体现 **真实环境 + 真实光影**
- 是否明确是 **3D Q版可爱化** 而不是普通卡通
- 是否体现 **手部 / 身体存在感**
- 是否保留 **9:16 竖屏、无字幕、无文字、无 logo、无水印**

## 避免事项

- 不要只输出抽象创意，不给可执行 prompt
- 不要忽略“上传角色”这一前提
- 不要把 POV 写成第三人称旁观
- 不要让角色完全脱离现实环境
- 不要只强调可爱，忽略互动
- 不要出现字幕、文字、logo、水印
- 不要把角色改得失去原始辨识度