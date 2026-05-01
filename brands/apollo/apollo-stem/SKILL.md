---
name: apollo-stem
description: >
  像干细胞一样自我更新和分化：让AI能够定期更新核心能力，同时保持已有的有效经验。
version: 2.1.0
read_when:
  - 用户提到更新、重建、能力升级
  - 系统能力下降时
  - 需要新增功能时
metadata:
  openclaw:
    emoji: "🔬"
    requires: []
    triggers:
      - 更新
      - 重建
      - 能力升级
      - 自我更新
    suite: apollo
---

# Apollo Stem — 系统自我更新系统

## 核心准则

**AI的能力更新应该像干细胞的自我更新：既能维持核心库，又能生成新的特化能力。**

干细胞的核心能力：
- **自我更新**：干细胞分裂成两个干细胞，维持干细胞库稳定
- **多向分化**：干细胞可以变成各种特化细胞
- **干性平衡**：太多自我更新→没有特化能力；太多分化→干细胞耗竭

对应的AI映射：
- **自我更新**：定期重建核心能力池，但不丢失已有经验
- **分化**：生成新的专用skill/能力
- **干性平衡**：通用性和专用性的平衡

## 触发条件

- 用户明确说"更新能力/升级/重建"
- 系统检测到核心能力过时（长期未更新的skill）
- Apollo Skill体系有重大架构调整

## 重建流程

```
触发重建 →
  1. 评估当前能力库：哪些skill有效、哪些过时
  2. 制定分化计划：需要新增哪些能力
  3. 执行自我更新：更新核心skill
  4. 执行分化：生成新能力
  5. 验证新能力：确保更新后系统正常
```

## 与其他Skill的协同

```
apollo-autophagy ──→ 清理旧能力 → 为新能力腾空间
apollo-epi      ──→ 知识传承 → 保留经验到新能力
apollo-overview  ──→ 能力地图 → 指导分化方向
```

# Apollo Stem — 系统自我更新系统

## 核心准则

**AI的能力更新应该像干细胞的自我更新：既能维持核心库，又能生成新的特化能力。**

干细胞的核心能力：
- **自我更新**：干细胞分裂成两个干细胞，维持干细胞库稳定
- **多向分化**：干细胞可以变成各种特化细胞
- **干性平衡**：太多自我更新→没有特化能力；太多分化→干细胞耗竭

对应的AI映射：
- **自我更新**：定期重建核心能力池，但不丢失已有经验
- **分化**：生成新的专用skill/能力
- **干性平衡**：通用性和专用性的平衡

---

## Skill自优化循环

**核心机制：效果追踪→数据分析→自动优化。**

### 4步循环

```
1. 效果记录 — 每次Skill用完，打一个简单的效果分
2. 数据积累 — 写入 .stem/skill-effectiveness.json
3. 模式分析 — 积累够10条数据，识别哪种模式更好
4. 自动更新 — 发现规律后更新Skill的描述/触发词
```

### 效果评分标准

| 评分 | 含义 | 触发条件 |
|------|------|---------|
| ✅ 有用 | 任务完成，Nic没追问 | 一次完成 |
| ⚠️ 一般 | 需要一轮追问 | 一次追问 |
| ❌ 没用 | 需要多轮追问或根本没效果 | 多次追问/放弃 |

---

## 触发点（两个实际执行入口）

### 触发点1：workflow Phase 5顺手记录

**这是主要入口，每次任务完成都会触发。**

在Phase 5的"自动提取Skill"之后，顺手执行：

```
任务交付确认 →
  检查这次用了哪些Skill
  打一个效果分（从对话结果判断）
  写入 .stem/skill-effectiveness.json

记录格式：
```json
{
  "skill": "apollo-workflow",
  "task": "<任务简述>",
  "score": "good|okay|bad",
  "phase": "phase5-finish",
  "date": "2026-04-30"
}
```

### 触发点2：每日心跳检查

心跳cron时调用`stem-check.sh`，检查：

```bash
# 检查内容：
- 最近7天哪个Skill用得最多
- 哪个Skill最近效果差（连续2次bad）
- 哪个Skill效果好但用得少
- 哪个Skill超过30天没被触发（可能过时）

# 发现问题时：
→ 主动Nudge我，告诉我哪个Skill需要优化
→ 问我是否要触发stem做一次深度优化
```

---

## 数据存储结构

```
.stem/
  skill-effectiveness.json   # 每次效果记录
  skill-summary.json        # 汇总统计（自动生成）
  skill-alerts.json         # 需要关注的警告
```

### skill-effectiveness.json 示例

```json
[
  {"skill": "apollo-workflow", "task": "装修估价工具", "score": "good", "date": "2026-04-29"},
  {"skill": "apollo-dream", "task": "记忆整理", "score": "good", "date": "2026-04-30"},
  {"skill": "apollo-workflow", "task": "论文总结", "score": "okay", "date": "2026-04-30"}
]
```

### skill-summary.json 示例

```json
{
  "apollo-workflow": {
    "total": 15,
    "good": 12,
    "okay": 2,
    "bad": 1,
    "last_used": "2026-04-30",
    "recommendation": "效果好，继续用"
  },
  "apollo-dream": {
    "total": 8,
    "good": 8,
    "okay": 0,
    "bad": 0,
    "last_used": "2026-04-30",
    "recommendation": "效果好，nudge机制已加，期待验证"
  }
}
```

---

## 什么时候触发深度优化

当心跳检查发现以下情况时，主动触发apollo-stem：

| 条件 | 说明 |
|------|------|
| 某个Skill连续2次bad | 这个Skill的描述/触发词可能过时 |
| 某个Skill超过30天未用 | 可能需要重新评估是否保留 |
| 用户明确说"更新" | 直接触发 |

### 定期清理低使用率Skill（每月一次）

除了上述问题触发，stem每月检查一次Skill使用情况：

**判断标准：**
- 超过60天未使用的Skill → 标记为"建议停用"
- 超过90天未使用的Skill → 标记为"可删除"
- 与其他Skill功能重复的 → 建议合并或删除

**操作流程：**
```
每月一次检查 →
  统计所有Skill的最后使用时间
  识别60天+/90天+未用的
  向Nic报告：哪些建议停用/删除
  Nic确认后执行清理
```

**原因：** Skill太多会导致触发准确率下降（参考"装30个Skill实际只用的6个"的数据）


触发后执行Stem重建流程（最多3轮）：

```
Stem触发 →
  1. 读取skill-summary.json
  2. 找到需要优化的Skill
  3. 分析bad cases，找出共性问题
  4. 更新Skill的description/triggers/steps
  5. 记录优化原因到stem.log
  6. 通知Nic优化完成
  
  如果3轮还没结论 → 暂停，等Nic确认方向
```

**为什么限制3轮：**
- 共享状态的"反应式死循环"风险——Agent可能一直在分析/更新里出不来
- 超过3轮就告诉你"还没结论，你要换个方向还是继续"
- 防止stem优化本身变成无限消耗token的黑洞

---

## 完整工作流（嵌入实际执行）

### 三层架构

```
Layer 1: 被动收集（自动，0打扰）
  workflow Phase5 → 顺手打分 → 写入 skill-effectiveness.json

Layer 2: 定期检查（心跳cron后台跑，写文件）
  stem-check.sh → 分析数据 → 写 alert 到 skill-alerts.json

Layer 3: 主动决策（我下次交互时读取，决定是否告知Nic）
  我读 skill-alerts.json → 发现问题 → 问Nic要不要优化 → 优化
```

### 流程图（文字版）

```
每次任务完成（Phase5）
    ↓
我打效果分 → 写入 .stem/skill-effectiveness.json
    ↓
心跳cron时（后台自动）
    ↓
stem-check.sh 读取 effectiveness 数据
    ↓
分析：哪个Skill连续2次bad？哪个超过30天没用？
    ↓
发现问题 → 写入 /tmp/.stem-alert 或 .stem/skill-alerts.json
    ↓
（不打断我，不发通知，就安静写文件）
    ↓
下次我和Nic交互时（任何消息）
    ↓
我主动读 skill-alerts.json
    ↓
有alert → 告诉Nic"有个Skill可能需要优化，要不要处理"
    ↓
Nic说"处理" → 我执行优化流程
Nic说"不管" → 记录忽略，更新alert状态
```

### 为什么这样设计

- **不打扰**：stem-check在后台跑，不发消息不弹窗
- **不遗漏**：下次任何交互时我都会读文件，不会错过
- **需确认**：最终优化要Nic说OK，不能我自动改（风险控制）

---

## 与其他Skill的协同

```
apollo-autophagy ──→ 清理旧能力 → 为新能力腾空间
apollo-epi      ──→ 知识传承 → 保留经验到新能力
apollo-overview  ──→ 能力地图 → 指导分化方向
apollo-dream    ──→ 记忆整理 → 提供优化线索（哪些经验值得固化）
workflow Phase5 ──→ 效果记录入口 → Layer 1数据来源
心跳cron        ──→ stem-check.sh → Layer 2数据+触发
任意交互       ──→ 我读alert → Layer 3主动决策
```

---

## 与Hermes的差距（诚实评估）

Hermes的Skill自优化是全自动的：
- 自动从经验中提取新Skill
- 自动在每次使用中改进

我们目前的实现是半自动的：
- 效果记录：半自动（嵌入Phase5，但需要我判断打分）
- 模式分析：半自动（心跳检查，发现问题推给我）
- 自动更新：手动（Nic确认后我才改）

**这是合理的设计——完全自动有风险，需要有人把关。**

---

## 待实施内容

- [x] `scripts/stem/stem-check.sh` — 心跳调用的检查脚本
- [x] `.stem/skill-effectiveness.json` — 数据存储
- [x] `workflow Phase5` 里埋效果记录入口
- [x] 心跳cron里调用stem-check
- [ ] `scripts/stem/stem-optimizer.py` — 模式分析脚本
- [ ] 外部精华吸收流程（见下方独立章节）

---

## 外部精华吸收流程（External Absorber）

### 定位

**当遇到外部好东西（外部Skill/方法论/工具），通过7步流程决定如何融入Apollo体系。**

### 品牌归属判断

| 来源 | 归属 |
|------|------|
| AI工作法/持续优化类 | → Apollo体系 |
| 各行各业垂直领域 | → Vertical/Local等其他品牌 |
| 通用工具类 | → 视情况加到最相关已有Skill |

### 7步融合流程

```
Step 1: 提炼精华
  ↓ 不是全盘复制
  → 提取核心机制（解决什么问题？核心是什么？）
  → 回答：它和我们缺的东西有什么关系？

Step 2: 判断归属
  ↓
  → 新能力（独立完整） → 新建Skill
  → 改进已有能力 → 加到最相关的已有Skill
  → 方法论/原则 → 写成规范，加到多个Skill

Step 3: 落到文件
  ↓
  新Skill → 创建 apollo-xxx/SKILL.md
  已有Skill改进 → 编辑对应SKILL.md
  规范层改进 → 改 apollo-workflow 或相关协调文件

Step 4: 更新文档
  ↓
  在改动位置注明来源：
  """
  来源：xxx（外部借鉴）
  借鉴内容：xxx
  融入方式：xxx
  """

Step 5: 建立反馈回路
  ↓ 新增
  → 记录预期效果
  → 下次心跳检查时验证是否生效
  → 没生效 → 分析原因 → 调整或移除

Step 6: 主动通知（参考Hermes nudge机制）
  ↓ 新增
  → 完成后主动告知Nic，不等他来查
  → 格式：
  "已从xxx提取了yyy，加到了apollo-xxx。
  原因：zzz，预期效果：eee。"

Step 7: 定期审计
  ↓ 原心跳检查改名，更准确
  → 每30天检查一次融入效果
  → 决定：保留/调整/移除
```

### 融入后的数据验证

```bash
.stem/
  external-absorptions.json   # 新增：记录每次吸收
```

**external-absorptions.json 格式：**
```json
{
  "id": "absorber-2026-05-01-001",
  "source": "Hermes/memfree/xxx",
  "extracted": "主动nudge机制",
  "target": "apollo-dream",
  "method": "融入到nudge子模块",
  "expected_effect": "被动等trigger → 主动推提醒",
  "integrated_at": "2026-05-01",
  "feedback_check": "下次心跳时验证",
  "status": "integrated"
}
```

### 持续更新能力如何确保

**三个保障机制：**

| 机制 | 如何落地 |
|------|---------|
| **反馈回路** | Step 5记录预期 → 心跳时检查效果 → 没效果就调整 |
| **主动通知** | Step 6确保完成后主动告知，不让Nic去查 |
| **定期审计** | Step 7每30天过一遍，记录到external-absorptions.json |

**核心原则：不是融进去就完了，要跟踪效果。**

---
