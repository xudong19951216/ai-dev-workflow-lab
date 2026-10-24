"""待办状态转换纯函数。

唯一业务函数为 ``transition_status``，依据架构文档中确认的转换矩阵
判断一次状态转换是否合法。
"""

# 合法状态（精确字符串，不 trim、不忽略大小写、不隐式转换）。
VALID_STATES = ("todo", "in_progress", "done")

# 转换矩阵：matrix[current][target] = True 表示允许。
# 依据 docs/architecture.md 的 3x3 矩阵：
#   todo        -> todo / in_progress
#   in_progress -> todo / in_progress / done
#   done        -> done
_TRANSITIONS = {
    "todo": {"todo": True, "in_progress": True, "done": False},
    "in_progress": {"todo": True, "in_progress": True, "done": True},
    "done": {"todo": False, "in_progress": False, "done": True},
}


def transition_status(current: str, target: str) -> str:
    """判断一次待办状态转换是否合法。

    参数：
        current: 当前状态。
        target:  目标状态。

    返回：
        转换合法时返回与 target 值相等的字符串。

    异常：
        TypeError: current 或 target 不是字符串（字符串子类允许）。
        ValueError: current 或 target 是字符串但不是合法状态，
                    或转换被矩阵禁止。
    """
    # 1. 类型检查优先：两参数都必须为字符串（允许 str 子类）。
    #    两个都不合类型时先报告 current；即便 current 是未知字符串而
    #    target 非字符串，也先报告 target 的 TypeError。
    if not isinstance(current, str):
        raise TypeError("current 必须是字符串")
    if not isinstance(target, str):
        raise TypeError("target 必须是字符串")

    # 2. 类型通过后，依次检查 current、target 是否为合法状态。
    if current not in VALID_STATES:
        raise ValueError("未知状态：current={!r}".format(current))
    if target not in VALID_STATES:
        raise ValueError("未知状态：target={!r}".format(target))

    # 3. 两状态都合法后，检查矩阵；不允许的组合抛 ValueError。
    if not _TRANSITIONS[current][target]:
        raise ValueError(
            "不允许从 {!r} 转换到 {!r}".format(current, target)
        )

    # 4. 成功时直接返回 target（与目标值相等的字符串）。
    return target
