
# 皮肤材质与去油词库

## 真实皮肤正面描述词

### 漫反射与毛孔
- 柔和漫反射、自然毛孔、细微纹理、轻微凹凸
- 肤色层次不均、淡淡红润、局部暗沉
- 真实阴影过渡、细微颗粒感、皮肤微纹理
- 骨骼结构受光、贴合骨骼的真实皮肤高光（极弱、分散）

### 部位覆盖
额头、鼻梁、鼻头、鼻翼、脸颊、苹果肌、下巴、脖子、锁骨、肩膀、胸口、手臂、手部

### 去油压暗比例
强反光、水光肌、玻璃皮、油膜感、湿亮皮肤、蜡质高光 → 压暗 80%-90%

## 假感负面描述词（需去除）

### 油腻类
oily skin, greasy shine, wet glossy skin, 油亮反光, 湿亮水光, 油膜感, 涂油感, 打蜡感

### 材质类
glass skin（玻璃皮）, waxy skin（蜡像感）, plastic skin（塑料皮）, rubber skin（橡胶皮肤）, porcelain skin（瓷娃娃）, silicone skin（硅胶皮肤）

### AI感类
airbrushed skin（磨皮）, over-smoothed face（过度平滑）, fake AI face（AI假脸）, doll-like face（人偶脸）, CGI skin（CG皮肤）, beauty filter（美颜滤镜）, 3D假材质

### 过度修饰类
excessive highlights（过曝高光）, glossy forehead/nose/cheeks/neck/collarbone（各部位油亮）, no pores（无毛孔）, fake skin texture（假皮肤纹理）

## 去油优先模式要点

当用户反馈结果仍油腻时，去油优先级高于：
- 电影感、高级感
- 夕阳高光、皮肤光泽
- 嘴唇润泽
- 美容灯、戏剧性高光

只保留光影图案和明暗结构，不保留皮肤上的镜面反光。高光只允许是极弱、分散、贴合骨骼结构的真实皮肤受光。

## 嘴唇处理

保留：唇纹、自然颜色
去除：塑料亮面、湿亮反光、唇釉光泽感