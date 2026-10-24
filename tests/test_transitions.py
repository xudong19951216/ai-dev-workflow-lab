"""transition_status 的行为测试。

预期结果独立编写，不读取实现内部的规则表，避免测试与实现同源漏测。
"""

import unittest

from todo_workflow.transitions import transition_status


class MyStr(str):
    """用于验证契约允许字符串子类的自定义 str 子类。"""


class TestTransitionMatrix(unittest.TestCase):
    """穷举 3x3 矩阵：6 个成功、3 个非法转换。"""

    def test_all_allowed_transitions(self):
        cases = [
            ("todo", "todo", "todo"),
            ("todo", "in_progress", "in_progress"),
            ("in_progress", "todo", "todo"),
            ("in_progress", "in_progress", "in_progress"),
            ("in_progress", "done", "done"),
            ("done", "done", "done"),
        ]
        for current, target, expected in cases:
            with self.subTest(current=current, target=target):
                self.assertEqual(transition_status(current, target), expected)

    def test_all_rejected_transitions(self):
        cases = [
            ("todo", "done"),
            ("done", "todo"),
            ("done", "in_progress"),
        ]
        for current, target in cases:
            with self.subTest(current=current, target=target):
                with self.assertRaises(ValueError):
                    transition_status(current, target)


class TestTypeValidation(unittest.TestCase):
    """非字符串参数应抛 TypeError。"""

    def test_current_non_string_types(self):
        for bad in (None, 1, True, [], {}):
            with self.subTest(current=bad):
                with self.assertRaises(TypeError):
                    transition_status(bad, "todo")

    def test_target_non_string_types(self):
        for bad in (None, 1, True, [], {}):
            with self.subTest(target=bad):
                with self.assertRaises(TypeError):
                    transition_status("todo", bad)


class TestUnknownState(unittest.TestCase):
    """字符串但非合法状态，应抛 ValueError。"""

    UNKNOWN = ("", " ", "TODO", " todo", "done ", "unknown")

    def test_current_unknown(self):
        for bad in self.UNKNOWN:
            with self.subTest(current=bad):
                with self.assertRaises(ValueError):
                    transition_status(bad, "todo")

    def test_target_unknown(self):
        for bad in self.UNKNOWN:
            with self.subTest(target=bad):
                with self.assertRaises(ValueError):
                    transition_status("todo", bad)


class TestValidationPriority(unittest.TestCase):
    """验证类型/状态/矩阵的检查优先级与错误信息指向。"""

    def test_unknown_current_with_non_string_target_reports_target_type(self):
        # current 是未知字符串，target 非字符串 -> 先报告 target 的 TypeError。
        with self.assertRaises(TypeError) as ctx:
            transition_status("unknown", None)
        self.assertIn("target", str(ctx.exception))

    def test_non_string_current_with_unknown_target_reports_current_type(self):
        with self.assertRaises(TypeError) as ctx:
            transition_status(None, "unknown")
        self.assertIn("current", str(ctx.exception))

    def test_unknown_current_with_bad_target_reports_current_value(self):
        # 两参数都是字符串但均非法 -> 先报告 current 的 ValueError。
        with self.assertRaises(ValueError) as ctx:
            transition_status("unknown", "bad")
        self.assertIn("current", str(ctx.exception))

    def test_both_non_string_reports_current_type(self):
        # (None, []) 两参数均非字符串 -> TypeError 且指出 current。
        with self.assertRaises(TypeError) as ctx:
            transition_status(None, [])
        self.assertIn("current", str(ctx.exception))


class TestErrorMessages(unittest.TestCase):
    """参数错误指出 current/target，非法转换指出两个状态。"""

    def test_type_error_mentions_current(self):
        with self.assertRaises(TypeError) as ctx:
            transition_status(1, "todo")
        self.assertIn("current", str(ctx.exception))

    def test_type_error_mentions_target(self):
        with self.assertRaises(TypeError) as ctx:
            transition_status("todo", 1)
        self.assertIn("target", str(ctx.exception))

    def test_value_error_mentions_both_states(self):
        with self.assertRaises(ValueError) as ctx:
            transition_status("todo", "done")
        msg = str(ctx.exception)
        self.assertIn("todo", msg)
        self.assertIn("done", msg)


class TestStrSubclass(unittest.TestCase):
    """契约允许字符串子类；返回值是字符串且等于目标值。"""

    def test_str_subclass_input_succeeds(self):
        result = transition_status(MyStr("todo"), MyStr("in_progress"))
        self.assertIsInstance(result, str)
        self.assertEqual(result, "in_progress")


class TestIdempotentAndIndependent(unittest.TestCase):
    """连续调用互不影响。"""

    def test_consecutive_calls_are_independent(self):
        first = transition_status("todo", "in_progress")
        second = transition_status("in_progress", "done")
        self.assertEqual(first, "in_progress")
        self.assertEqual(second, "done")
        # 再验证一次反向，确认前一次调用未残留状态。
        third = transition_status("in_progress", "todo")
        self.assertEqual(third, "todo")


if __name__ == "__main__":
    unittest.main()
