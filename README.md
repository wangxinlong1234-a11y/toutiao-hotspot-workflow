# 今日头条热点采集与原创文章工作台

本工作台用于：发现今日头条公开热点 → 评分筛选选题 → 事实核查 → 原创撰写 → 配图与 Word 排版 → 本地/ GitHub 归档。**所有文章仅生成草稿，不自动发布。**

## 一、环境要求（已验证 2026-10-28）
- Windows 10 专业版（Build 19045）
- Python 3.13.14（建议 3.11+）
- Node.js v22.22.2 / npm 10.9.7（仅 Agent Browser 需要）
- Git 2.55.0.windows.3
- WorkBuddy 5.9.3（内置 WebSearch、workbuddy-docx、workbuddy-sheet-generation）

## 二、目录结构
```
toutiao-hotspot-workflow/
├── README.md
├── requirements.txt
├── .gitignore
├── config/example_config.yaml      # 配置示例（复制为 config.yaml 后填写）
├── data/topics_template.csv         # 选题采集模板
├── scripts/
│   ├── score_topics.py              # 选题多维度评分与排名
│   └── generate_word.py             # 由草稿 JSON 生成 Word
├── templates/article_template.md    # 文章排版模板
├── output/
│   ├── topics/                      # 选题 CSV 结果
│   ├── drafts/                      # 文章草稿
│   └── images/                      # 配图
├── tests/test_score.py              # 评分逻辑单元测试
└── .workbuddy/skills/toutiao-hotspot-workflow/SKILL.md  # 工作流技能
```

## 三、安装
1. 创建虚拟环境并安装依赖：
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. （可选）安装 Agent Browser 浏览器自动化：
   ```bash
   npm install -g agent-browser
   agent-browser install
   ```

## 四、使用流程
1. **采集候选**：用 WorkBuddy 的 WebSearch（或 Agent Browser）访问公开热榜，按 `data/topics_template.csv` 字段记录 10–20 条候选，保存到 `output/topics/candidates.csv`。
2. **评分筛选**：`python scripts/score_topics.py output/topics/candidates.csv 3` 输出前 3 推荐。
3. **事实核查与写作**：对选定选题多源搜索，整理事实与来源，原创撰写后保存为草稿 JSON。
4. **生成 Word**：`python scripts/generate_word.py output/drafts/<选题>.json output/drafts/<选题>.docx`。
5. **运行测试**：`python tests/test_score.py`。

## 五、合规约束
- 不把榜单排名/热度冒充单篇阅读量。
- 不绕过验证码/登录限制；无法读取时由你手动提供资料。
- 不编造新闻事实、数据、引用或阅读量。
- GitHub 仅在你确认后提交，排除凭证与未公开草稿。

## 六、已验证状态（2026-10-28）
- WebSearch 可用，已成功返回真实头条/热榜数据。
- workbuddy-docx 可生成 Word。
- Agent Browser 二进制安装中（后台），若受限以 WebSearch 替代。
- Git 全局身份为空，需你授权配置后再提交。
- GitHub 当前账号无公开仓库，需你确认新建或指定仓库。
