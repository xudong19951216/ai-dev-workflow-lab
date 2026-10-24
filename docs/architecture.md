# 待办状态转换模块设计 v0.1

设计者：Codex。任务：[Issue #2](https://github.com/xudong19951216/ai-dev-workflow-lab/issues/2)。
本版为设计提案。是否确认以设计 PR 中用户的确认记录为准；用户确认且设计合并后 WorkBuddy 才开始实现。

## 目标与边界

以一个无网络、无第三方依赖的小模块验证代码开发与测试的协作闭环。用户传入当前状态和目标状态，函数判断转换是否合法，返回新状态或抛出异常。
这只是试验业务对象的状态机，不是 GitHub Issue 或团队协作流程状态机。
不包含 UI、存储、HTTP、任务 ID、并发更新、权限、历史记录、CLI 程序、自动调度或 CI 配置。

## 模块结构

```text
todo_workflow/
  __init__.py            # 包入口；可以为空，公开导入路径固定见下文
  transitions.py         # 唯一业务函数
tests/
  test_transitions.py    # unittest 行为测试
README.md                # Python 要求、使用示例、测试命令
```

使用 Python 3.11 或更新版本；标准库 unittest，不增加依赖或安装要求。从仓库根目录即可导入和测试。运行环境若不具备 Python，先报告现状，不自动安装整套开发环境。
调用关系：调用者 / 测试 → transitions.transition_status；无外部系统依赖、无文件读写、无网络访问、无可变的业务全局状态。
输入仅两个字符串，输出一个字符串；无需数据库与持久化数据模型。

## 函数契约

公开导入路径：`from todo_workflow.transitions import transition_status`。
签名：`transition_status(current: str, target: str) -> str`。
合法状态仅为精确字符串 `todo`、`in_progress`、`done`。
成功时返回与 target 值相等的字符串，不约束返回对象与 target 的身份（is）或是否保留 str 子类；直接返回 target 即可满足契约。不修改输入或其他状态，连续调用应互不影响。

转换矩阵为唯一业务依据：

| current \\ target | todo | in_progress | done |
|---|---|---|---|
| todo | 返回 todo | 返回 in_progress | ValueError |
| in_progress | 返回 todo | 返回 in_progress | 返回 done |
| done | ValueError | ValueError | 返回 done |

设计选择：同状态转换幂等成功；允许进行中退回待办；禁止待办直接完成；已完成状态不能重开。这些是本试验的明确业务约定，不宣称适用于所有项目。

### 输入验证与优先级

1. 先检查两参数均为字符串（isinstance(value, str)；字符串子类允许），否则 TypeError。两个都不合类型时先报告 current；即便 current 是未知字符串而 target 非字符串，也先报告 target 的 TypeError。
2. 两参数类型都通过后，依次检查 current、target 是否为合法状态；否则 ValueError。
3. 两状态都合法后才检查矩阵；不允许的组合抛 ValueError。
4. 不 trim、不忽略大小写、不隐式转换。空串、空白、`TODO`、` todo`、`done `、未知状态都属于未知状态。
5. 错误信息必须非空；参数错误指出 current 或 target，非法转换指出两个状态。措辞由实现者决定，测试不锁定整段文字。

例子：`transition_status("todo", "in_progress")` 返回 `"in_progress"`；`transition_status("todo", "done")` 抛 ValueError；`transition_status([], "todo")` 抛 TypeError。
以上为契约样例，不是已运行结果。

## 验收测试

由 WorkBuddy 独立编写预期结果，不从业务实现内部规则表生成预期。可用 unittest.subTest 表达参数组合，避免重复测试代码。

- 穷举矩阵 9 个组合，覆盖 6 个成功结果和 3 个非法转换。
- current 与 target 分别覆盖 None、整数、布尔值、列表、字典，均抛 TypeError；尤其不能因列表/字典不可哈希而在错误阶段意外报错。
- 两参数分别覆盖空串、空白、大小写错误、前后空格、unknown，均抛 ValueError；另一参数使用合法状态。
- 优先级：("unknown", None) 抛 TypeError 且错误信息指出 target；(None, "unknown") 指出 current；("unknown", "bad") 抛 ValueError 且指出 current；(None, []) 两参数均非字符串时抛 TypeError 且指出 current。
- 验证参数错误消息包含参数名、非法转换消息包含两个状态；不比较整段固定文本。
- 至少一个自定义 str 子类成功案例，验证契约允许字符串子类；断言返回值是字符串且 == 目标值，不断言对象身份或具体子类。
- 独立连续调用覆盖两个合法转换，确认前一次调用不改变后一次结果。

不要求生产函数有额外扩展、复杂类层次、覆盖率工具或专用测试框架。

## 实现与验证步骤

1. 设计经用户确认并合并后，WorkBuddy 从最新 main 创建 `feat/2-status-transitions`。
2. 开始前记录 Python 版本和代码基线。仓库尚无测试时如实注明，不把零测试当成业务通过。
3. 实现上述函数、标准库测试和 README 运行说明；按需新增最小 .gitignore 忽略 Python 缓存，不提交缓存文件。
4. 从仓库根目录运行 `python -m unittest discover -s tests -v`。Windows 若使用 `py -3`，记录实际等价命令与 Python 版本。
5. 必须确认测试被发现并实际执行、退出码为 0；记录测试方法数量与参数覆盖情况（subTest 不一定增加方法计数）。
6. 在现有 README 追加 Python 模块小节，保留原有项目介绍和全部文档导航，增加设计文档链接；给出一条成功示例、一条异常示例、测试命令，用运行结果验证示例。
7. 创建实现 PR，正文使用仓库模板并填写 `Closes #2`，提供实际测试结果与完整 Head SHA，等待同 SHA 双审。
8. 两位审查者可各自在自己的可用环境运行测试；没有执行条件时如实注明静态审查，不假称运行。用户确认后合并。

本轮不配置 Actions 或部署；本地测试与测试证据不等于平台强制检查已开启。模板 UI 的真实展示可在后续通过 GitHub 页面创建任务时核验；本 Issue 由 API 创建，不声称验证了页面模板。

## 权限、风险和回退

遵守 [AGENTS.md](../AGENTS.md)。允许改动只包括本设计指定的模块、测试、README 和最小 .gitignore。
接口/状态矩阵/异常行为有变更时，按协作规则更新设计与任务并取得用户确认；实现内部的常规选择由 WorkBuddy 自行决定。
审查重点：不小心放行 todo→done 或 done 重开、先查集合导致错误类型、测试与实现共用规则产生同源漏测。
不故意植入缺陷来演示审查。若首次代码审查无问题，直接进入确认，不人为制造修复循环。
合并前可关闭实现 PR；合并后以单独回退 PR 撤销该模块及相关说明，避免影响已建立的协作文档。
