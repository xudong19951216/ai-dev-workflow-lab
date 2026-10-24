# 试验仓库落地方案 v0.1

## 当前状态

- 私有仓库 xudong19951216/ai-dev-workflow-lab，默认分支 main。
- 已合并 PR：#1（协作文档与模板）、#3（状态转换设计）、#4（状态转换实现与测试）、#5（CI 工作流）。
- CI 已启用：`.github/workflows/ci.yml`，在 PR 与 main push 时运行，覆盖 Python 3.11、3.12、3.13 的标准库测试。
- Codex 自动审查已开启；Grok 已创建事件触发 Routine。两者的自动触发效果待本次新 PR 验证，当前不视为已验证。
- WorkBuddy 仍由用户发消息启动；收到修复指令时直接读取 PR 上的审查意见，不依赖用户逐条转述。
- 最终合并由用户确认。

## 推荐仓库结构

```text
AGENTS.md
docs/architecture.md
docs/workflow.md
docs/review-format.md
.github/workflows/ci.yml
.github/ISSUE_TEMPLATE/task.md
.github/pull_request_template.md
README.md
```

AGENTS.md 为仓库根目录协作规则。docs/architecture.md 为状态转换模块设计。审查结果、修复清单与交接格式保存在 docs/review-format.md。CI 工作流位于 .github/workflows/ci.yml。Issue 与 PR 模板分别位于 .github/ISSUE_TEMPLATE/task.md 与 .github/pull_request_template.md。

## 交接状态与触发方式

任务状态：待设计 → 待用户确认 → 可开发 → 开发中 → 待双审 → 待修复 → 待复审 → 待合并 → 完成。
任何阶段均可记录“受阻”及原因、负责人、下一步。状态先写在 Issue 顶部，不依赖额外看板或标签配置。

- 用户向 WorkBuddy 发消息启动任务；WorkBuddy 收到后拉取最新 main、读取 AGENTS.md 与关联 Issue 再开工。
- 用户向 WorkBuddy 发修复指令；WorkBuddy 直接读取 PR 上的审查意见逐条处理。
- Codex 自动审查、Grok 事件触发 Routine 的自动触发效果待本次新 PR 验证。

## 已完成验证

- 文档轮：私有仓库读取、Git 推送、PR 创建、意见回写与修复闭环（PR #1）。
- 代码轮：待办状态转换函数与 15 个标准库测试，本地 `python -m unittest discover -s tests -v` 全过（PR #4）。
- CI：Python 3.11 / 3.12 / 3.13 矩阵测试（PR #5）。

## 合并约束

不预设两个独立 GitHub 审查账号；同一账号下使用署名审查记录，由用户查看验收证据并手动决定合并。最终合并由用户确认。
后续如需平台强制执行双审，应采用可区分的应用身份或可靠的检查结果，明确绑定最新 SHA，并核实仓库套餐和保护规则可用性。
