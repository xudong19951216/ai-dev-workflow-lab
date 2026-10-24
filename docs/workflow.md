# 试验仓库落地方案 v0.1

## 当前状态

- 私有仓库 xudong19951216/ai-dev-workflow-lab 已创建，默认分支 main，README 可读。
- Codex 已通过连接器实际读取仓库与 README（此前 404 为连接未打通，非仓库不存在）。
- WorkBuddy 已通过 gh 完成旧 Token 撤销与重新登录，凭证已替换；私有仓库读写、PR 操作在本次文档任务中已实际验证。
- 本文件随首个文档 PR（docs/bootstrap-workflow）纳入仓库。

## 推荐仓库结构

```text
AGENTS.md
docs/workflow.md
docs/review-format.md
.github/ISSUE_TEMPLATE/task.md
.github/pull_request_template.md
README.md
# 后续/按需（进入代码设计时再由 Codex 提供，不预先创建空文件）：
docs/architecture.md
docs/decisions/
```

AGENTS.md 为仓库根目录协作规则。审查结果、修复清单与交接格式保存在 docs/review-format.md。Issue 与 PR 模板分别位于 .github/ISSUE_TEMPLATE/task.md 与 .github/pull_request_template.md。docs/architecture.md 与 docs/decisions/ 为后续/按需产物，待代码设计轮由 Codex 提供后创建。

## 交接状态

任务状态：待设计 → 待用户确认 → 可开发 → 开发中 → 待双审 → 待修复 → 待复审 → 待合并 → 完成。
任何阶段均可记录“受阻”及原因、负责人、下一步。状态先写在 Issue 顶部，不依赖额外看板或标签配置。

用户只需向对应工具发送仓库链接与 Issue/PR 链接；工具自行读取上下文。尚无跨工具自动通知保证。

## 分两轮验证

第一轮：文档 PR。WorkBuddy 添加规则与模板，在独立分支 docs/bootstrap-workflow 提交；Codex 和 Grok Bot 审查同一提交，WorkBuddy 修复，用户确认合并。验证私有仓库读取、Git 推送、PR 创建、意见回写和修复闭环。纯文档轮不声称验证了自动测试能力。

第二轮：小型代码任务。建议实现一个无网络、无依赖的 Python 待办状态转换函数，用标准库 unittest 验证正常转换、非法状态和禁止转换。Codex 先出函数契约和验收标准，用户确认后才交 WorkBuddy 实现。此轮验证测试证据及缺陷修复流程。

GitHub Actions 在选择运行环境并确认权限后再配置。没有 workflow scope 不等于所有已有 Actions 都不能运行；具体能力须按操作和仓库设置判断。

## 起步阶段的合并约束

不预设两个独立 GitHub 审查账号；同一账号下使用署名审查记录，由用户查看验收证据并手动决定合并。
后续如需平台强制执行双审，应采用可区分的应用身份或可靠的检查结果，明确绑定最新 SHA，并核实仓库套餐和保护规则可用性。
