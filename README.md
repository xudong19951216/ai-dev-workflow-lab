# ai-dev-workflow-lab

验证 Codex 架构设计、WorkBuddy 实现及 Codex/Grok Bot 双重审查的协作流程。

## 文档导航

- [AGENTS.md](AGENTS.md) — AI 开发协作规则（角色权责、开发流程、审查规则、合并条件、权限与凭证、触发方式）。
- [docs/workflow.md](docs/workflow.md) — 试验仓库落地方案（仓库结构、任务状态、分轮验证计划、合并约束）。
- [docs/review-format.md](docs/review-format.md) — 审查结果、修复清单与交接格式。
- [.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md) — 开发任务 Issue 模板。
- [.github/pull_request_template.md](.github/pull_request_template.md) — PR 描述模板。

## 待办状态转换模块

一个无网络、无第三方依赖的纯函数，用于验证代码开发与测试的协作闭环。

设计依据：[docs/architecture.md](docs/architecture.md)。

### 要求

- Python 3.11 或更新版本。
- 仅使用标准库，无额外安装依赖。

### 使用示例

```python
from todo_workflow.transitions import transition_status

# 合法转换：返回目标状态
transition_status("todo", "in_progress")   # -> "in_progress"
transition_status("in_progress", "done")   # -> "done"

# 非法转换：抛出 ValueError
transition_status("todo", "done")          # -> ValueError
```

### 测试

从仓库根目录运行：

```bash
python -m unittest discover -s tests -v
```

预期结果为 15 个测试方法全部通过、退出码 0。
