# 《雨后的天空》室内生活与做饭验收报告

- 验收时间：2026-09-12
- 页面：`http://localhost:8060/index.html`
- 验收范围：`HOUSE-ACT-01`、`COOK-01`、`HOUSE-ACT-STABILITY`
- 结论：**PASS（3/3）**

## HOUSE-ACT-01 [关键]

- **判定：PASS**
- 17 座住宅逐栋点击进入均成功。
- 每座住宅都有可见小朋友，四类活动为写作业、看书、搭积木和吃饭。
- 雨天疏散完成后，24 名公园人物仍保持可见；进入建筑的人不再直接隐藏。
- 证据：`qa/shots-phase3/HOUSE-ACT-01-house-1.png`、`HOUSE-ACT-01-house-14.png`、`HOUSE-ACT-01-house-17.png`、`HOUSE-ACT-01-rain-visible-inside.png`。

## COOK-01 [关键]

- **判定：PASS**
- 17 座住宅的锅旁均有可见人物持续翻炒，锅内有炒饭并有蒸汽动画。
- 餐厅厨师持续炒饭；小顾客完整经历 buying、collecting、carrying、eating 四个状态。
- 证据：`qa/shots-phase3/COOK-01-restaurant.png`、`COOK-01-buying-meal.png`。

## HOUSE-ACT-STABILITY

- **判定：PASS**
- WebGL canvas 正常，17 座住宅点击结果全部为 true。
- 完整雨天疏散后桥上、山上和钓鱼区仍保持清空。
- 浏览器控制台与页面异常数均为 0。

## 汇总

| ID | 结果 |
|---|---|
| HOUSE-ACT-01 | PASS |
| COOK-01 | PASS |
| HOUSE-ACT-STABILITY | PASS |
