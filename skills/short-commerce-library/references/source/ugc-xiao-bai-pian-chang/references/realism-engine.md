# 真实感引擎（招牌档专用）
> 供 Step 4 编译层调用。只在「真实自拍感」预设下挂载；艺术风格档只用第 3、4 节提精准。
> 方法论来源：素材身份论（已获 MIT 授权参考，本文件为小白片场重写版）。

## 1. 素材身份（写提示词前必须先回答）

每条真实感提示词的开头，先在心里回答三句话，再把答案融进描述：
- **谁拍的**：路人、朋友、拍摄者自己、家人
- **什么设备**：手机竖屏 / 2000 年代 DV / VHS 家用机 / Super8 胶片 / 监控摄像头
- **为什么拍**：随手记录、旅行留念、家庭录像、无意中拍到

不写素材身份，模型会自动补成它最熟练的样子：稳、净、对称、商业调色——一眼假。

## 2. 设备缺陷包（按场景四选一，写进摄像风格段）

**手机竖屏自拍包**（默认，AI自拍/风景通用）
轻微过度锐化与 HDR 处理感；走路时画面上下浮动；从暗处走进亮处时曝光会猛地跳一下再稳住；
偶有手指擦过镜头边缘；电子防抖的轻微拉扯感。
负面：无三脚架稳定、无专业布光、无电影运镜。

**2000s DV 家庭录像包**（老照片/家庭场景）
中等数字压缩伪影；褪色偏色；传感器噪点；明显手持抖动；自动对焦偶尔"搜一下"；
进出阴影时曝光抽动。
负面：无稳定、无现代调色、无精致构图。

**VHS 怀旧包**（八九十年代感）
扫描线；色彩溢出偏暖；四角发暗；低分辨率；可加少许磁带噪点。
负面：无高清细节、无数码锐度。

**监控摄像头包**（特殊整蛊/氛围用途）
高位俯视固定机位；低帧率；画面偏灰；时间戳可提但禁止清晰数字（AI 不碰字）；
无声或只有环境低噪。
负面：无运镜、无构图美学。

## 3. 氛围翻译表（抽象词 → 可拍到的具体现象）

| 用户说的 | 翻译成画面里的 |
|---|---|
| 温暖 | 阳光穿过叶隙、杯口白汽、窗帘轻摆、抬手拢发 |
| 孤独 | 大留白构图、空荡街道、冷白荧光、脚步带回响 |
| 紧张 | 灯管忽明忽暗、走廊深影、频频回望、远处金属撞击 |
| 生活气息 | 摊主忙碌、蒸汽升腾、人声交错、车铃声 |
| 浪漫 | 逆金光、慢速行人虚化、同撑一把伞、橱窗暖光 |
| 怀旧 | 褪色、老物件、颗粒、画幅暗角 |

## 4. 去 AI 感自检（提交提示词前过一遍）

- 主体一致性写死了吗（脸/服装/发型逐条钉）
- 地点够具体吗（拒绝"美丽的街道"，要"湿润柏油路+早餐车+地铁口"）
- 有物理缺陷吗（曝光抽、对焦慢、手持晃，至少一处）
- 时间轴里有"非完美事件"吗（镜头晚半拍跟上、路人误入、拍到一半移开）
- 声音和画面对得上吗（看见蒸汽就应有嘶嘶声）
- 有没有混进广告片运镜和商业调色（有就删）

## 5. 非完美事件库（每条提示词放 1-2 个）

镜头稍晚才跟上主体转身 ｜ 路人从镜头前走过短暂遮挡 ｜ 对焦先落到猫身上再回到人脸 ｜
风吹乱头发遮住半张脸 ｜ 镜头垂下拍到地面和鞋尖再抬起 ｜ 出阴影那一刻曝光亮了一拍再稳住 ｜
拍到一半突然结束，像拍摄者随手按停

## 6. 示例骨架（招牌档）

⚠️ 无声片最终编译输出一律用**英文正文**（中文指令句会被 H3 当台词念出来，2026-09-08 学费）。
soundscape 只写非音乐物理声，禁止出现任何乐器名（乐器名会被演绎成人声演唱）。

```
[Identity] A casual smartphone vertical video, filmed by a friend on a Paris street
corner at 7 AM, real phone footage feel.
[Subject] (with photo) Image 1 = her face, exactly the same face as the reference,
stable facial proportions; beige trench coat, paper coffee cup in left hand.
[Location] Paris street corner at 7 AM, wet cobblestones, cafe rattan chairs,
bakery with warm glowing window.
[Camera] handheld smartphone, 9:16 vertical, slight over-sharpening and HDR look,
gentle bob while walking, exposure briefly brightens when stepping into sunlight;
no gimbal, no professional lighting, no cinematic camera moves.
[Timeline] 00-04s wet cobblestones and steam from the cup, tilt up to her;
04-08s she turns back and smiles, breeze blows hair across her cheek;
08-12s pigeons fly up, camera follows half a beat late, tilts down and ends.
[Soundscape] only non-musical physical sounds - morning street ambience, pigeon
wings, footsteps on wet stone, soft clink of the cup; no music, no instruments.
[Audio rule] absolutely no human voice - no dialogue, no narration, no voiceover,
no singing, no humming, no crowd mumble, no reading any text aloud.
[Negative] real-time speed, absolutely no slow motion; no readable text;
no commercial color grading.
```
