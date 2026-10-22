---
name: "ugc-pin-pai-logo-dong-tai-pian-tou-sheng-cheng-ji-neng"
display_name: "品牌LOGO动态片头生成技能"
description: "适用于品牌LOGO片头设计"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
video_model: "seedance2.0_vision"
image_model: "seedream_5.0_pro"
---

# [SKILL.MD](http://SKILL.MD)  
skill_name: tvc_logo_intro_blank_reveal  
skill_description: TVC动态LOGO品牌视频片头技能，画面从完全空白起始，完成LOGO从无到有的浮现动画。输出AI视频提示词、中文剪辑提示、AE制作方案、音效设计。适用于TVC广告、品牌宣传片开头。  
trigger_condition: ["TVC","动态LOGO","品牌视频开头","片头","空白到出现","logo渐显","黑屏出logo","白屏出logo"]  
params:  
  logo_text:  
    type: string  
    default: "YOUR BRAND"  
    desc: 品牌LOGO文字/名称  
  duration:  
    type: number  
    default: 3  
    desc: 片头总时长，单位秒，TVC常用2‑4s  
  background_type:  
    type: enum  
    default: black  
    enum_values: ["black","white","gradient","subtle‑texture"]  
    desc: 背景类型  
  reveal_style:  
    type: enum  
    default: fade  
    enum_values: ["fade","glow","particle","draw"]  
    desc: 浮现方式：fade淡入 / glow光效扫过 / particle粒子汇聚 / draw线条描边绘制  
  resolution:  
    type: string  
    default: "1920×1080"  
    desc: 分辨率，可设置3840×2160(4K)  
  frame_rate:  
    type: number  
    default: 25  
    desc: 帧率，国内TVC标准25fps  
  logo_color:  
    type: string  
    default: "#ffffff"  
    desc: LOGO主体颜色  
  atmosphere:  
    type: string  
    default: "高级商务"  
    desc: 整体氛围：高级商务 / 科技未来 / 轻奢质感 / 简约文艺  
  
output_modules:  
  module_1_ai_video_prompt:  
    note: "硬性约束：起始帧完全空白无任何元素，LOGO不能初始出现，平滑过渡显现，TVC广告质感"  
    content: "TVC commercial opening logo intro video, {background_type} background, start from completely blank empty frame, no logo at beginning, {reveal_style} reveal brand logo \"{logo_text}\" slowly emerge into frame, smooth motion, clean premium commercial aesthetic, soft subtle lighting, no extra clutter, sharp vector logo, brand identity opening sequence, {atmosphere}, cinematic color grading, no text overlay other than logo, {resolution}, {frame_rate}fps, smooth motion blur, professional advertisement title sequence, duration {duration} seconds"  
  
  module_2_cn_clip_prompt:  
    note: "剪映、可灵AI等国内AI视频工具中文提示词"  
    content: "品牌TVC片头，总时长{duration}秒。0‑0.5s：画面完全{background_type}空白，画面无任何LOGO图形文字；0.5s‑{duration‑0.5}s：LOGO以{reveal_style}方式从无到有缓缓浮现，运动柔和高级，无抖动，无多余杂物；最后0.5s：LOGO完整稳定定格在画面视觉中心，画面干净，商业广告质感，{atmosphere}，{resolution}，{frame_rate}帧。禁止一开始就出现LOGO。"  
  
  module_3_ae_design_notes:  
    note: "AE后期制作参考"  
    content: |  
      1.新建合成：分辨率{resolution}，帧率{frame_rate}fps，时长 {duration}s  
      2.底层固态层设置背景 {background_type}  
      3.LOGO图层初始透明度：0%，居中放置  
      4.动画分支  
      - fade淡入：透明度关键帧，0.5s为0%，{duration‑0.5}s为100%，使用缓入缓出曲线  
      - glow光效扫过：添加辉光效果，蒙版路径做扫光动画，同步提升LOGO透明度  
      - particle粒子汇聚：LOGO作为粒子发射器，粒子由空白区域汇聚成型LOGO  
      - draw描边绘制：描边效果从0%绘制至100%，同步填充淡入  
      5.输出编码：ProRes422，适配TVC套片输出  
  
  module_4_sound_design:  
    note: "音效配套建议"  
    content: |  
      - fade淡入：低频嗡声渐起，LOGO定格瞬间轻微品牌咚音效，前期压低BGM音量  
      - glow / particle：轻微气流沙沙+微光闪烁音效，LOGO成型使用短促清脆品牌标识音  
      &gt; 0‑0.5s音频静音或极低音量，匹配画面空白阶段  
  
constraints:  
  - "强制规则：视频起始帧必须完全空白，严禁LOGO初始就显示在画面，所有提示词必须体现该限制。"  
  - "画面克制，不增加多余装饰元素，聚焦品牌LOGO展示，符合TVC广告审美。"  
  - "用户未传入参数，全部使用默认参数输出，同时提示用户可修改品牌名、时长、背景、浮现风格。"  
  - "用户提供LOGO图片素材时，将logo_text替换为「给定矢量品牌LOGO图形」。"  
  
reply_template: |  
  已加载 TVC动态LOGO品牌视频开头（空白到出现）skill。  
  当前参数：LOGO名称：`{logo_text}`｜时长：`{duration}s`｜背景：`{background_type}`｜浮现方式：`{reveal_style}`｜氛围：`{atmosphere}`  
  你可以告诉我修改：品牌名称、时长、黑/白/渐变背景、淡入/光扫/粒子/描边浮现方式，我会更新全套提示词。