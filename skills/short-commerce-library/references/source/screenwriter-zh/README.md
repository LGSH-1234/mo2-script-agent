
# 编剧技能——快速入门

面向编剧的通用工具技能。不绑定特定故事。可在 Claude / Cowork / Claude Code 中作为技能文件夹使用。

---

## 内容清单

- **`SKILL.md`** — 技能主要描述（第一个读）。
- **`methodology.md`** — 麦基 + 坎贝尔 + 亚里士多德。
- **`style-rules.md`** — 好莱坞格式写作规则。
- **`workflow.md`** — 工作模式。
- **`timing-and-cutting.md`** — 银幕时间估算与长度削减。
- **`templates/`** — 你的故事的空白模板。
- **`tools/`** — .docx 生成器（剧本、双语版、分集表）。

---

## 如何开始

### 第一步。安装

将 `screenwriter-zh/` 文件夹复制到合适的位置：Claude Code 项目内、Cowork 中作为用户技能（`~/.claude/skills/screenwriter-zh/`），或直接放在工作文件旁边。

### 第二步。告诉 Claude

> "加载 screenwriter-zh 技能，我们开始。"

Claude 将阅读 SKILL.md、方法论、写作规则和工作模式。

### 第三步。带来你的材料

以下任一种方式：

**A. 你已经有大纲/分集表/场景草稿。**
发送文件——Claude 会读取并询问从哪里开始。

**B. 你只有一个想法。**
用一两段话描述。Claude 会提问并帮你建立大纲，然后是分集表，然后是场景。

**C. 你只有标题和类型。**
填写 `templates/synopsis.template.md` 和 `templates/characters.template.md`。然后迭代进行。

### 第四步。逐场戏工作

标准循环：
1. 你根据分集表要求一场戏。
2. Claude 给出一个版本；仅在用户要求时说明理由。
3. 你给出修改意见。
4. Claude 精准修改。
5. 用户要求文档时，通过 `tools/build_screenplay.js` 导出为 .docx；否则只交付剧本文本。

---

## 导出工具

### 剧本（好莱坞格式）
```bash
cp tools/build_screenplay.js my_scene.js
# 打开 my_scene.js，通过 slug/action/character/dial/trans 填写 screenplay 数组
node my_scene.js
# 得到 screenplay.docx
```

### 双语版（对话 + 译文）
```bash
cp tools/build_bilingual.js my_bilingual.js
# 通过 ...dialB("主语言", "译文") 填写
node my_bilingual.js
# 得到 screenplay-bilingual.docx
```

### 分集表
```bash
cp tools/build_treatment.js my_treatment.js
# 通过 scene("标题", "内容", "[可选] 审核标签") 填写
node my_treatment.js
# 得到 treatment.docx
```

---

## 典型的技能调用请求

| 请求 | Claude 做什么 |
|---|---|
| "写第5场戏" | 读取分集表 → 写一个版本；仅在用户要求时说明理由 |
| "这不对" | 问一个窄化的二元问题 → 新版本 |
| "做成双语版" | 使用 `tools/build_bilingual.js` |
| "做因果审核" | 逐场用 ⚠ 标签审查分集表 |
| "会有多少分钟？" | 按场景类型计算（见 `timing-and-cutting.md`） |
| "控制在X分钟内" | 给出含具体数字的剪切方案 |
| "让Y角色的声音与X不同" | 对比台词，提出修改建议 |

---

## Claude 不做的三件事

1. **不写5个版本** — 给一个版本，按需解释。
2. **不"顺便优化"相邻台词** — 只改被要求改的内容。
3. **不靠空泛情绪词** — 用可拍的动作、表演及必要视听细节呈现。

如果 Claude 违反了这些规则——说："一个版本，不是五个"或"只改X"。

---

## 个性化技能

如果你大量写同一类型的作品——可以派生这个技能并添加：

- **`reference-films.md`** — 参考影片列表及场景分析。
- **`my-style.md`** — 你个人的风格偏好（例如"不喜欢闪回"、"总是在沉默中结尾"）。
- **`recurring-tropes.md`** — 你反复使用的技巧。

技能变成你的，而不是通用的。