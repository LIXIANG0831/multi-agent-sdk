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

