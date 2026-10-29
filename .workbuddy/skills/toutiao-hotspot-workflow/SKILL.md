---
name: toutiao-hotspot-workflow
slug: toutiao-hotspot-workflow
displayName: 今日头条热点采集与原创文章工作台
version: 1.0.0
description: 从今日头条公开热榜发现热点、评分筛选选题、核查事实、原创撰写文章并生成 Word 草稿的完整工作流。当用户需要"采集头条热点、筛选选题、写头条文章、生成文章草稿、做选题评分"时触发。
license: MIT
metadata:
  requires:
    anyBins: ["python"]
---

# 今日头条热点采集与原创文章工作台

## 适用场景
用户需要从今日头条公开网页/热榜发现热点、评分筛选选题、核查事实、原创撰写文章并生成 Word 草稿，供审核后发布。

## 工作流
1. **热点采集**：使用 WebSearch 或 Agent Browser 访问公开热榜，按 `data/topics_template.csv` 字段采集 10–20 个候选（标题、链接、采集时间、榜单排名、页面可见指标、来源、备注）。
2. **评分筛选**：运行 `scripts/score_topics.py <candidates.csv> 3`，对时效性/热度信号/读者兴趣/资料可靠性/原创空间打分，输出前 3 推荐及理由。
3. **事实核查**：对选定选题多源搜索，整理事实清单与来源链接，明确标注无法确认的数字、时间、人物言论。
4. **原创写作**：设计独立大纲，生成 5 个标题备选、导语、正文、小标题、结尾，禁止逐句替换或复制受版权保护表达。
5. **配图与排版**：提出 2–3 张配图并记录来源/授权；用 `scripts/generate_word.py` 或 workbuddy-docx 生成 Word（标题/导语/正文/小标题/图片/图注/资料来源/审核清单）；同时导出选题 CSV。
6. **GitHub 归档**：仅在你确认后提交代码、Skill、测试与说明；排除密码、Cookie、令牌、个人凭证与未公开草稿。

## 约束（强制）
- 不把话题热度、点赞量或榜单排名冒充单篇文章真实阅读量。
- 不绕过验证码、登录限制或平台访问限制；无法读取时请用户手动提供标题/链接/资料。
- 不编造新闻事实、数据、引用或阅读量。
- 仅生成草稿，不自动发布。

## 依赖
Python 3.11+，python-docx、pandas、requests；可选 Agent Browser（npm i -g agent-browser）。
