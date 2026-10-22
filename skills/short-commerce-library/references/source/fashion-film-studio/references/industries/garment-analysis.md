
# 服装资产解析与面料质感词库

> 可适配的模式与句式，按场景改写，不要逐字照搬。

## 服装结构化解析维度

当用户提供服装图片或参考视频时，重点提取以下结构化信息：

### 款式与剪裁轮廓（Silhouette）
- 廓形类型：H型 / A型 / X型 / O型 / T型 / 花苞型 / 直筒 / 伞摆
- 领口：圆领 / V领 / 方领 / 立领 / 翻领 / 一字领 / 抹胸 / 堆堆领
- 袖型：无袖 / 短袖 / 七分袖 / 长袖 / 泡泡袖 / 喇叭袖 / 灯笼袖 / 飞飞袖 / 落肩袖
- 裙摆/裤型：A字裙 / 百褶裙 / 鱼尾裙 / 直筒裤 / 阔腿裤 / 喇叭裤 / 锥形裤

### 面料材质词库

| 质地类型 | 光泽度 | 透明度 | 厚重感 | 动态物理特征 |
|---|---|---|---|---|
| 真丝/缎面 | 高光泽 | 半透 | 轻薄 | flowing liquid drape, light-catching sheen；垂坠如水，运动中漂浮回弹慢 |
| 毛呢/粗花呢 | 哑光 | 不透 | 厚重 | dense woven texture, structured weight, matte surface；形变迟滞，保持廓形 |
| 皮革/PU | 高光泽 | 不透 | 中等偏重 | high-gloss specular, tight grain, stiff silhouette；硬挺，折角锐利 |
| 雪纺/纱 | 微光 | 半透至透明 | 极轻薄 | airy translucent layers, wind-responsive drift；随风飘动，层叠透光 |
| 针织/毛线 | 哑光 | 不透 | 中等 | ribbed knit relief, soft stretch, micro-loop texture；弹性形变，贴合身体曲线 |
| 棉麻 | 哑光 | 不透 | 中等 | natural matte weave, breathable texture, organic creases；自然褶皱，质朴触感 |
| 丝绒/天鹅绒 | 变色光泽 | 不透 | 厚重 | depth-shifting pile, directional light response, plush surface；光线方向改变时色相偏移 |
| 亮片/钉珠 | 高闪烁 | 不透 | 偏重 | faceted specular scatter, prismatic refraction, weighted drape；点状散射光晕，运动惯性大 |
| 涤纶/化纤 | 中等光泽 | 不透 | 轻薄至中等 | smooth synthetic surface, static cling tendency；顺滑但易静电贴身 |
| 牛仔 | 哑光偏磨 | 不透 | 厚重 | rugged twill weave, fading gradient, rigid hold；硬朗保形，磨白渐变 |

### 色彩特征
- 主色：色相 + 明度 + 饱和度
- 辅色：与主色的对比/调和关系
- 图案/纹样：几何/花卉/条纹/格纹/波点/渐变/扎染；色相与饱和度特点

### 动态物理预判
为镜头动态描述提供依据，预判面料在不同运动状态下的表现：

- **垂坠感**：面料受重力作用的下垂形态（真丝如水垂坠 vs 毛呢保持廓形 vs 纱质飘浮）
- **摆动惯性**：运动后回弹的速度与幅度（真丝回弹慢且幅度大，毛呢几乎不回弹，针织弹性回缩）
- **风力响应**：面料对气流的敏感度（雪纺/纱极度敏感，皮革/毛呢几乎不响应）
- **折射光谱**：光泽面料在光线下的折射特征（丝绸的镜面反射，亮片的棱镜散射，丝绒的方向性变色）

## 面料质感强调词组速查

生成提示词时按面料类型选用对应词组：

- 真丝 → flowing liquid drape, light-catching sheen, liquid mercury flow
- 毛呢 → dense woven texture, structured weight, matte surface
- 皮革 → high-gloss specular, tight grain, stiff silhouette
- 针织 → ribbed knit relief, soft stretch, micro-loop texture
- 雪纺/纱 → airy translucent layers, wind-responsive drift, layered opacity
- 丝绒 → depth-shifting pile, directional light response, plush surface
- 亮片 → faceted specular scatter, prismatic refraction, weighted drape
- 棉麻 → natural matte weave, breathable texture, organic creases
- 牛仔 → rugged twill weave, fading gradient, rigid hold

## 落 prompt 前自检

- 面料类型是否已识别并匹配对应质感词组？
- 动态物理预判是否写入提示词（垂坠/摆动/风力响应/折射）？
- 色彩描述是否包含主色 + 辅色 + 饱和度特征？
- 廓形描述是否精确到领口/袖型/裙摆或裤型？