"""
多智能体识别准确性测试脚本
测试主调度智能体能否准确路由到正确的专业智能体
"""

import asyncio
from agents import Runner
from air_compressor_station_agents import main_agent


# ==================== 颜色定义 ====================

class TestColors:
    """测试输出颜色"""
    GREEN = '\033[92m'   # 正确
    RED = '\033[91m'     # 错误
    YELLOW = '\033[93m'  # 警告
    CYAN = '\033[96m'    # 信息
    RESET = '\033[0m'    # 重置


# ==================== 测试用例定义 ====================

TEST_CASES = [
    # dispatch_agent 测试用例 (4个)
    {
        "question": "如何启动1号空压机？",
        "expected_agent": "dispatch_agent"
    },
    {
        "question": "停止3号空压机运行",
        "expected_agent": "dispatch_agent"
    },
    {
        "question": "将2号空压机负荷调整到80%",
        "expected_agent": "dispatch_agent"
    },
    {
        "question": "当前用气需求是多少？",
        "expected_agent": "dispatch_agent"
    },

    # maintenance_agent 测试用例 (3个)
    {
        "question": "1号空压机出现异常振动，怎么诊断故障？",
        "expected_agent": "maintenance_agent"
    },
    {
        "question": "温度过高怎么维修？需要什么步骤？",
        "expected_agent": "maintenance_agent"
    },
    {
        "question": "订购5个轴承备件",
        "expected_agent": "maintenance_agent"
    },

    # energy_analysis_agent 测试用例 (3个)
    {
        "question": "分析本月的能耗数据",
        "expected_agent": "energy_analysis_agent"
    },
    {
        "question": "对比1号和2号空压机的能效",
        "expected_agent": "energy_analysis_agent"
    },
    {
        "question": "生成节能分析报告",
        "expected_agent": "energy_analysis_agent"
    },

    # health_agent 测试用例 (3个)
    {
        "question": "查询1号空压机的健康评分",
        "expected_agent": "health_agent"
    },
    {
        "question": "预测2号空压机的维护需求",
        "expected_agent": "health_agent"
    },
    {
        "question": "获取3号空压机的实时运行状态",
        "expected_agent": "health_agent"
    },

    # report_agent 测试用例 (4个)
    {
        "question": "生成今天的运营日报",
        "expected_agent": "report_agent"
    },
    {
        "question": "生成本月的运营月报",
        "expected_agent": "report_agent"
    },
    {
        "question": "提供一些优化建议",
        "expected_agent": "report_agent"
    },
    {
        "question": "分析当前运营状况并给出建议",
        "expected_agent": "report_agent"
    },

    # inspection_agent 测试用例 (3个)
    {
        "question": "对1号空压机进行视觉巡检",
        "expected_agent": "inspection_agent"
    },
    {
        "question": "対2号空压机进行巡检，检测是否有异常",
        "expected_agent": "inspection_agent"
    },
    {
        "question": "记录3号空压机的巡检结果：设备正常",
        "expected_agent": "inspection_agent"
    },
]


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
        # 使用会话保持上下文
        from agents import SQLiteSession
        session = SQLiteSession(
            session_id="recognition_test",
            db_path="./sessions/recognition_test.db"
        )
        # 调用智能体
        result = await Runner.run(
            main_agent,
            input=question,
            session=session
        )

        actual = result.last_agent.name
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

    print("=" * 60)
    print("测试摘要")
    print("=" * 60)
    print(f"总题数：{total}")
    print(f"正确：{correct}")
    print(f"错误：{errors}")
    print(f"准确率：{accuracy:.2f}%")
    print()

    # 显示错误详情
    if error_cases:
        print("错误详情：")
        for case in error_cases:
            print(f"- 问题{case['index']}: 预期 {case['expected']}, "
                  f"实际 {case['actual']}")
        print()

    print("测试完成！")


async def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("多智能体识别准确性测试")
    print("=" * 60)
    print(f"测试用例数：{len(TEST_CASES)}")
    print(f"开始执行测试...")
    print()

    results = []

    # 逐个执行测试
    for index, test_case in enumerate(TEST_CASES, start=1):
        result = await execute_single_test(test_case, index)
        results.append(result)
        print_test_result(result)

    # 打印摘要
    print_summary(results)

    return results


def main():
    """主程序入口"""
    asyncio.run(run_tests())


if __name__ == "__main__":
    main()