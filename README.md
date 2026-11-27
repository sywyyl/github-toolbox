# GitHub 工具箱（Toolbox）

把 GitHub 当成个人工具箱：**脚本 + Skill + 一张需求索引**都放在这个仓库里。
以后你只要说出需求，我会先查 `registry.json`，按触发词匹配出最合适的 2–3 个 Skill / 脚本并推荐给你，而不是每次从零开始想。

## 目录结构

```
github-toolbox/
├── README.md                 # 本文件：人看的索引
├── registry.json             # 机器读的索引：需求触发词 → Skill/脚本
├── skills/                   # 真正的 Skill（每个一个目录 + SKILL.md）
│   └── toolbox-router/       # 元技能：教我如何用这个工具箱推荐 Skill
├── scripts/                  # 可独立运行的脚本
│   └── validate_registry.py  # 校验索引完整性（本地 / Actions 都能跑）
├── .github/workflows/
│   └── validate.yml          # 推送或每周自动校验索引
└── .gitignore
```

## 三种用法

1. **让我推荐**：直接说需求，例如“我想每天盯竞品价格”。我读取 `registry.json`，按 `triggers` 匹配，优先本地 Skill，再推荐市场 Skill。
2. **本地调用**：把 `skills/<name>` 复制或软链到工作区的 `.workbuddy/skills/` 下，我就能直接调用它。
3. **自动运行**：`.github/workflows/validate.yml` 在每次推送和每周一校验索引；后续可往这里加定时抓数据、生成日报等工作流。

## 添加一个工具

1. 在 `skills/` 下新建目录，写 `SKILL.md`，frontmatter 至少包含 `name` 和 `description`。
2. 在 `registry.json` 加一条记录，填 `id / name / source / triggers / best_for`。
3. 提交推送，Actions 自动校验；本地也可运行 `python scripts/validate_registry.py`。

## registry.json 字段

| 字段 | 含义 |
| --- | --- |
| `id` | 唯一标识，推荐时引用 |
| `name` | 展示名称（Skill 用 display_name） |
| `source` | `local`（仓库内）或 `marketplace`（技能市场） |
| `path` | local 项的 SKILL.md 相对路径；marketplace 为 `null` |
| `triggers` | 触发词/短语，用来匹配用户需求 |
| `best_for` | 适用场景，用于生成推荐理由 |
| `install` | 安装或启用方式 |

## 已安装 Skill（2026-11-27）

| 需求 | 推荐 Skill | 状态 |
| --- | --- | --- |
| 找/搜/推荐/安装 Skill | 技能发现神器-FindSkills-WB | 已安装 |
| 不确定该用哪个 Skill | 技能猎人 | 已安装 |
| Git/GitHub 日常操作 | Git 工作流 | 已安装 |
| 每天/每周自动跑任务 | 定时任务编排模板生成器 | 已安装 |

> 原计划的「仓库运维 批处理脚本 效率工具」「定时任务场景模板库」不在技能市场目录，安装接口拒绝；已用同类的「Git 工作流」「定时任务编排模板生成器」替代。
