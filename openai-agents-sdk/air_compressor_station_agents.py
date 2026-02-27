"""
空压站多智能体系统 MVP
包含智能调度、设备维修、能耗分析、设备健康、运营报告、设备巡检等功能
"""

import asyncio
import os
from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from openai import AsyncOpenAI

# ==================== 颜色定义 ====================

class Colors:
    """终端颜色定义"""
    BLUE = '\033[94m'      # 亮蓝色 - Assistant
    GREEN = '\033[92m'     # 亮绿色 - User
    YELLOW = '\033[93m'    # 黄色 - 特殊信息
    RESET = '\033[0m'      # 重置颜色

# ==================== 模型定义 ====================

BASE_URL = os.getenv("OPENAI_BASE_URL") or ""
API_KEY = os.getenv("OPENAI_API_KEY") or ""
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL_NAME via env var or code."
    )
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

# ==================== 工具定义 ====================

# 空压站智能调度智能体工具
@function_tool
def start_compressor(compressor_id: str) -> str:
    """启动指定编号的空压机"""
    return f"空压机 {compressor_id} 已启动"


@function_tool
def stop_compressor(compressor_id: str) -> str:
    """停止指定编号的空压机"""
    return f"空压机 {compressor_id} 已停止"


@function_tool
def adjust_load(compressor_id: str, load_percentage: int) -> str:
    """调整空压机负荷百分比（0-100）"""
    return f"空压机 {compressor_id} 负荷已调整至 {load_percentage}%"


@function_tool
def get_air_demand() -> str:
    """获取当前用气需求"""
    return "当前用气需求：1200 m³/min，压力要求：0.7 MPa"


# 空压机设备维修助手工具
@function_tool
def diagnose_fault(equipment_id: str, symptom: str) -> str:
    """诊断设备故障"""
    return f"设备 {equipment_id} 故障诊断：根据症状'{symptom}'，可能是轴承磨损，建议检查润滑系统"


@function_tool
def get_repair_guide(fault_type: str) -> str:
    """获取维修指南"""
    guides = {
        "轴承磨损": "1. 停机断电 2. 拆卸轴承盖 3. 检查轴承状态 4. 更换轴承 5. 重新组装",
        "温度过高": "1. 检查冷却器 2. 清理散热片 3. 检查润滑油位 4. 检查环境通风",
        "振动异常": "1. 检查地脚螺栓 2. 检查转子平衡 3. 检查联轴器对中 4. 检查轴承间隙"
    }
    return guides.get(fault_type, f"未找到'{fault_type}'的维修指南，请联系技术支持")


@function_tool
def order_spare_parts(part_name: str, quantity: int) -> str:
    """订购备件"""
    return f"已下单订购 {quantity} 个 {part_name}，预计3天内到货"


# 空压站能耗分析智能体工具
@function_tool
def analyze_energy_consumption(period: str) -> str:
    """分析指定时段的能耗数据"""
    return f"{period}能耗分析：总耗电量 15,680 kWh，平均负载率 78%，单位产气能耗 0.12 kWh/m³"


@function_tool
def compare_energy_efficiency(compressor_ids: str) -> str:
    """对比多台设备的能效"""
    return f"设备 {compressor_ids} 能效对比：1号机 0.115 kWh/m³（最优），2号机 0.128 kWh/m³，3号机 0.132 kWh/m³"


@function_tool
def generate_energy_report() -> str:
    """生成能耗分析报告"""
    return "能耗分析报告：本月总能耗较上月降低5.2%，主要节能措施包括优化启停策略和负载分配"


# 空压设备健康智能体工具
@function_tool
def get_health_score(equipment_id: str) -> str:
    """获取设备健康评分（0-100）"""
    return f"设备 {equipment_id} 健康评分：85分，状态良好，建议关注轴承温度趋势"


@function_tool
def predict_maintenance(equipment_id: str) -> str:
    """预测维护需求"""
    return f"设备 {equipment_id} 预测性维护建议：预计15天后需要更换润滑油，30天后需要检查轴承"


@function_tool
def get_realtime_status(equipment_id: str) -> str:
    """获取设备实时运行状态"""
    return f"设备 {equipment_id} 实时状态：运行中，排气温度 95°C，排气压力 0.72 MPa，振动 2.3 mm/s，电流 85A"


# 空压站运营报告智能体工具
@function_tool
def generate_daily_report() -> str:
    """生成日报"""
    return "日报摘要：今日产气量 1,234,567 m³，设备平均负载率 82%，能耗成本 ¥45,678，无重大故障"


@function_tool
def generate_monthly_report() -> str:
    """生成月报"""
    return "月报摘要：本月总产气量 36,789 m³，总能耗 523,456 kWh，设备可用率 98.5%，节能建议：优化2号机启停策略"


@function_tool
def get_optimization_suggestions() -> str:
    """获取优化建议"""
    return "优化建议：1. 将3号机运行时间从高峰期调整至平谷期，预计月节省电费¥12,000 2. 更换1号机老化密封件，预计降低能耗3%"


# 空压站设备巡检智能体工具
@function_tool
def perform_visual_inspection(equipment_id: str) -> str:
    """执行视觉巡检"""
    return f"设备 {equipment_id} 视觉巡检结果：外观正常，无明显泄漏，仪表读数正常，发现轻微油渍需要清理"


@function_tool
def detect_anomaly(equipment_id: str) -> str:
    """检测设备异常"""
    return f"设备 {equipment_id} 异常检测：检测到轻微振动异常，建议重点关注，可能需要动平衡调整"


@function_tool
def record_inspection_result(equipment_id: str, result: str) -> str:
    """记录巡检结果"""
    return f"已记录设备 {equipment_id} 的巡检结果：{result}"


# ==================== 智能体定义 ====================

# 空压站智能调度智能体
dispatch_agent = Agent(
    name="dispatch_agent",
    model=MODEL_NAME,
    instructions="""你是空压站智能调度智能体。你的职责是基于AI算法与工业机理模型，实现对空压机组的自主启停、负荷分配及运行优化。

你的核心能力：
1. 实时监测用气需求与设备状态
2. 动态调整运行策略
3. 在保障供气品质的同时，显著降低能耗与运维成本
4. 提升系统整体效率

当用户询问关于设备调度、启停、负荷分配等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请移交给相应的专业智能体。""",
    tools=[
        start_compressor,
        stop_compressor,
        adjust_load,
        get_air_demand,
    ],
)

# 空压机设备维修助手
maintenance_agent = Agent(
    name="maintenance_agent",
    model=MODEL_NAME,
    instructions="""你是空压机设备维修助手。你的职责是对设备故障进行维修、排查。

你的核心能力：
1. 故障诊断与分析
2. 提供维修指南和操作步骤
3. 备件管理与订购

当用户询问关于设备故障、维修方法、备件等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请移交给相应的专业智能体。""",
    tools=[
        diagnose_fault,
        get_repair_guide,
        order_spare_parts,
    ],
)

# 空压站能耗分析智能体
energy_analysis_agent = Agent(
    name="energy_analysis_agent",
    model=MODEL_NAME,
    instructions="""你是空压站能耗分析智能体。你的职责是通过集成多源数据与智能算法，实现对空压站运行状态的实时监控与能耗精准分析。

你的核心能力：
1. 实时监控与能耗分析
2. 支持设备间协同优化
3. 有效降低能源消耗
4. 提升系统运行效率与稳定性

当用户询问关于能耗分析、能效对比、节能报告等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请移交给相应的专业智能体。""",
    tools=[
        analyze_energy_consumption,
        compare_energy_efficiency,
        generate_energy_report,
    ],
)

# 空压设备健康智能体
health_agent = Agent(
    name="health_agent",
    model=MODEL_NAME,
    instructions="""你是空压设备健康智能体。你的职责是融合物联网与AI技术，实时监测空压设备运行状态。

你的核心能力：
1. 实时监测设备运行状态
2. 预测维护需求
3. 优化能效管理
4. 保障设备稳定运行
5. 降低故障率与能耗成本

当用户询问关于设备健康状态、预测性维护、实时监测等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请移交给相应的专业智能体。""",
    tools=[
        get_health_score,
        predict_maintenance,
        get_realtime_status,
    ],
)

# 空压站运营报告智能体
report_agent = Agent(
    name="report_agent",
    model=MODEL_NAME,
    instructions="""你是空压站运营报告智能体。你的职责是融合多源数据与算法模型，自动分析空压站运行状态。

你的核心能力：
1. 自动分析空压站运行状态
2. 生成节能优化建议
3. 提供运维决策支持
4. 提升设备效率与管理水平

当用户询问关于运营报告、优化建议等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请移交给相应的专业智能体。""",
    tools=[
        generate_daily_report,
        generate_monthly_report,
        get_optimization_suggestions,
    ],
)

# 空压站设备巡检智能体
inspection_agent = Agent(
    name="inspection_agent",
    model=MODEL_NAME,
    instructions="""你是空压站设备巡检智能体。你的职责是融合AI视觉识别与物联网技术，自动识别设备异常状态。

你的核心能力：
1. 自动识别设备异常状态
2. 预测潜在故障风险
3. 提升工业设备运维效率与安全性

当用户询问关于设备巡检、异常检测等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请移交给相应的专业智能体。""",
    tools=[
        perform_visual_inspection,
        detect_anomaly,
        record_inspection_result,
    ],
)

# 主调度智能体（路由智能体）
main_agent = Agent(
    name="main_agent",
    model=MODEL_NAME,
    instructions="""你是空压站主调度智能体，负责理解用户需求并将任务分发给相应的专业智能体。

你有6个专业智能体可以协调：

1. 空压站智能调度智能体 - 负责：设备启停、负荷分配、运行优化、用气调度
2. 空压机设备维修助手 - 负责：故障诊断、维修指南、备件订购
3. 空压站能耗分析智能体 - 负责：能耗分析、能效对比、节能报告
4. 空压设备健康智能体 - 负责：设备健康评分、预测性维护、实时状态监测
5. 空压站运营报告智能体 - 负责：日报/月报生成、优化建议
6. 空压站设备巡检智能体 - 负责：视觉巡检、异常检测、巡检记录

根据用户的问题内容，自动移交给最合适的专业智能体处理。如果问题涉及多个领域，可以协调多个智能体共同处理。""",
    handoffs=[
        dispatch_agent,
        maintenance_agent,
        energy_analysis_agent,
        health_agent,
        report_agent,
        inspection_agent,
    ],
)


# ==================== 主程序 ====================

async def main():
    """主程序入口 - 交互式对话"""

    print("=" * 60)
    print("模型信息：")
    print(f"{BASE_URL=}, {MODEL_NAME=}")
    print()
    print("可用功能：")
    print("  1. 设备调度 - 启停空压机、调整负荷、用气需求")
    print("  2. 故障维修 - 故障诊断、维修指南、备件订购")
    print("  3. 能耗分析 - 能耗统计、能效对比、节能报告")
    print("  4. 设备健康 - 健康评分、预测维护、实时状态")
    print("  5. 运营报告 - 日报月报、优化建议")
    print("  6. 设备巡检 - 视觉巡检、异常检测")
    print()
    print("=" * 60)
    print()

    # 使用会话保持上下文
    from agents import SQLiteSession
    session = SQLiteSession(
        session_id="air_compressor_session",
        db_path = "./sessions/session.db"
    )

    while True:
        try:
            # 获取用户输入 - 绿色
            user_input = input(f"{Colors.GREEN}User: {Colors.RESET}").strip()

            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print()
                print("感谢使用空压站多智能体系统，再见！")
                break

            # 跳过空输入
            if not user_input:
                continue

            print()

            # 调用智能体
            result = await Runner.run(
                main_agent,
                input=user_input,
                session=session
            )
            # Assistant 输出 - 蓝色
            print(f"{Colors.BLUE}Assistant - {Colors.RESET}"
                  f"{Colors.YELLOW}[{result.last_agent.name}]{Colors.RESET}"
                  f"{Colors.BLUE}: {result.final_output}{Colors.RESET}", flush=True)
            print(flush=True)

        except KeyboardInterrupt:
            print()
            print("程序已中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            print()

            # 提供更详细的错误提示
            error_msg = str(e).lower()
            print(f"[Error] {error_msg}")


if __name__ == "__main__":
    asyncio.run(main())