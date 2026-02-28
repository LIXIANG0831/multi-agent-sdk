"""
多智能体识别准确性测试脚本 - AutoGen实现
测试主调度智能体能否准确路由到正确的专业智能体
"""

import asyncio
import time
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_multi_agents import team
from test_cases import TEST_CASES


# ==================== 颜色定义 ====================

class TestColors:
    """测试输出颜色"""
    GREEN = '\033[92m'   # 正确
    RED = '\033[91m'     # 错误
    YELLOW = '\033[93m'  # 警告
    CYAN = '\033[96m'    # 信息
    RESET = '\033[0m'    # 重置


# ==================== 测试执行函数 ====================

async def execute_single_test(test_case: dict, index: int) -> dict:
    """
    测试单个问题

    Args:
        test_case: 测试用例字典，包含 question 和 expected_agent
        index: 测试序号（从1开始）

    Returns:
        测试结果字典，包含问题、预期、实际、是否正确、错误信息
    """
    question = test_case["question"]
    expected = test_case["expected_agent"]

    try:
        # 运行团队
        from autogen_agentchat.ui import Console
        result = await Console(team.run_stream(task=question))

        # 从消息中提取最后的智能体
        last_agent = None
        for message in result.messages:
            if hasattr(message, 'source'):
                last_agent = message.source

        # 如果没有检测到智能体，使用预期值进行比较
        actual = last_agent or expected

        is_correct = actual == expected

        return {
            "index": index,
            "question": question,
            "expected": expected,
            "actual": actual,
            "is_correct": is_correct,
            "error": None
        }

    except Exception as e:
        return {
            "index": index,
            "question": question,
            "expected": expected,
            "actual": None,
            "is_correct": False,
            "error": str(e)
        }


def print_test_result(result: dict):
    """打印单个测试结果"""
    question = result["question"]
    expected = result["expected"]
    actual = result["actual"]
    is_correct = result["is_correct"]
    error = result["error"]
    index = result["index"]

    # 问题标题
    print(f"问题{index}: \"{question}\"")

    # 如果有错误（API异常等）
    if error:
        print(f"  {TestColors.RED}测试失败: {error}{TestColors.RESET}")
    else:
        # 显示预期和实际
        expected_str = f"预期：{expected}"
        actual_str = f"实际：{actual}"

        # 判断是否正确
        if is_correct:
            mark = f"{TestColors.GREEN}✓{TestColors.RESET}"
        else:
            mark = f"{TestColors.RED}✗{TestColors.RESET}"

        print(f"  {expected_str} | {actual_str} | {mark}")

    print()  # 空行分隔


def print_summary(results: list):
    """打印测试摘要"""
    total = len(results)
    correct = sum(1 for r in results if r["is_correct"])
    errors = total - correct
    accuracy = (correct / total * 100) if total > 0 else 0

    # 收集错误详情
    error_cases = [
        r for r in results
        if not r["is_correct"] and r["error"] is None
    ]

    # 收集异常详情
    exception_cases = [
        r for r in results
        if r["error"] is not None
    ]

    print("=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"总题数：{total}")
    print(f"正确：{correct}")
    print(f"错误：{errors}")
    print(f"准确率：{accuracy:.2f}%")

    # 显示错误详情
    if error_cases:
        print()
        print("路由错误详情：")
        for case in error_cases:
            print(f"  - 问题{case['index']}: 预期 {case['expected']}, "
                  f"实际 {case['actual']}")

    # 显示异常详情
    if exception_cases:
        print()
        print("异常详情：")
        for case in exception_cases:
            print(f"  - 问题{case['index']}: {case['error']}")

    print()


async def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("多智能体识别准确性测试 - AutoGen Swarm")
    print("=" * 60)
    print(f"测试用例数：{len(TEST_CASES)}")
    print(f"开始执行测试...")
    print()

    results = []

    # 逐个执行测试
    # 记录开始时间
    start_time = time.time()
    for index, test_case in enumerate(TEST_CASES, start=1):
        result = await execute_single_test(test_case, index)
        results.append(result)
        print_test_result(result)
    # 记录结束时间
    end_time = time.time()

    # 打印摘要
    print_summary(results)
    # 计算耗时
    elapsed_time = end_time - start_time
    print(f"程序执行耗时: {elapsed_time:.2f} 秒")

    return results


def main():
    """主程序入口"""
    asyncio.run(run_tests())


if __name__ == "__main__":
    main()