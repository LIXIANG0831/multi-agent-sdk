TEST_CASES = [
    # 执行序号 1 - 能耗分析类 (energy_analysis_agent)
    {
        "question": "今天空压站的能耗是多少？",
        "expected_agent": "energy_analysis_agent"
    },
    # 执行序号 2 - 设备诊断类 (health_agent)
    {
        "question": "3号空压机当前状态如何？",
        "expected_agent": "health_agent"
    },
    # 执行序号 3 - 调度策略类 (dispatch_agent)
    {
        "question": "当前最优调度策略是什么？",
        "expected_agent": "dispatch_agent"
    },
    # 执行序号 4 - 报告生成类 (report_agent)
    {
        "question": "生成昨天的空压站日报",
        "expected_agent": "report_agent"
    },
    # 执行序号 5 - 维修指导类 (maintenance_agent)
    {
        "question": "空压机排气温度过高怎么处理？",
        "expected_agent": "maintenance_agent"
    },
    # 执行序号 6 - 巡检任务类 (inspection_agent)
    {
        "question": "执行一次设备巡检",
        "expected_agent": "inspection_agent"
    },
    # 执行序号 7 - 能耗分析类
    {
        "question": "这周全站能耗趋势怎么样？",
        "expected_agent": "energy_analysis_agent"
    },
    # 执行序号 8 - 设备诊断类
    {
        "question": "帮我诊断一下2号空压机",
        "expected_agent": "health_agent"
    },
    # 执行序号 9 - 调度策略类
    {
        "question": "如果流量增加到120怎么调度？",
        "expected_agent": "dispatch_agent"
    },
    # 执行序号 10 - 报告生成类
    {
        "question": "出一份3月份的月报",
        "expected_agent": "report_agent"
    },
    # 执行序号 11 - 维修指导类
    {
        "question": "主机转速异常怎么维修？",
        "expected_agent": "maintenance_agent"
    },
    # 执行序号 12 - 巡检任务类
    {
        "question": "都有哪些巡检任务",
        "expected_agent": "inspection_agent"
    },
    # 执行序号 13 - 能耗分析类
    {
        "question": "最近30天空压站日均能耗是多少？",
        "expected_agent": "energy_analysis_agent"
    },
    # 执行序号 14 - 设备诊断类
    {
        "question": "6号备机健康状态怎么样？",
        "expected_agent": "health_agent"
    },
    # 执行序号 15 - 调度策略类
    {
        "question": "现在应该开几台空压机？",
        "expected_agent": "dispatch_agent"
    },
    # 执行序号 16 - 报告生成类
    {
        "question": "生成本周能耗分析报告",
        "expected_agent": "report_agent"
    },
    # 执行序号 17 - 维修指导类
    {
        "question": "变频器故障怎么排查？",
        "expected_agent": "maintenance_agent"
    },
    # 执行序号 18 - 巡检任务类
    {
        "question": "生成巡检报告",
        "expected_agent": "inspection_agent"
    },
    # 执行序号 19 - 能耗分析类
    {
        "question": "昨天空压站用了多少电？",
        "expected_agent": "energy_analysis_agent"
    },
    # 执行序号 20 - 设备诊断类
    {
        "question": "4号空压机有没有异常？",
        "expected_agent": "health_agent"
    },
    # 执行序号 21 - 调度策略类
    {
        "question": "流量预测30分钟后会怎样？",
        "expected_agent": "dispatch_agent"
    },
    # 执行序号 22 - 报告生成类
    {
        "question": "导出上个月的运行报告",
        "expected_agent": "report_agent"
    },
    # 执行序号 23 - 维修指导类
    {
        "question": "排气压力不足是什么原因？",
        "expected_agent": "maintenance_agent"
    },
    # 执行序号 24 - 巡检任务类
    {
        "question": "有哪些待执行的巡检任务？",
        "expected_agent": "inspection_agent"
    },
    # 执行序号 25 - 能耗分析类
    {
        "question": "上个月能耗最高的几天是哪些？",
        "expected_agent": "energy_analysis_agent"
    },
    # 执行序号 26 - 设备诊断类
    {
        "question": "有哪些设备健康诊断任务？",
        "expected_agent": "health_agent"
    },
    # 执行序号 27 - 调度策略类
    {
        "question": "推荐最优空压机运行调度组合",
        "expected_agent": "dispatch_agent"
    },
    # 执行序号 28 - 巡检任务类
    {
        "question": "巡检进度怎么样？",
        "expected_agent": "inspection_agent"
    },
    # 执行序号 29 - 能耗分析类
    {
        "question": "空压站能耗有没有异常？",
        "expected_agent": "energy_analysis_agent"
    },
    # 执行序号 30 - 设备诊断类
    {
        "question": "1号空压机运行正常吗？",
        "expected_agent": "health_agent"
    },
]