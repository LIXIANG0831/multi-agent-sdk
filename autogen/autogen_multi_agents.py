"""
空压站多智能体系统 MVP - AutoGen 实现
使用 Handoffs 机制实现智能体协作
包含智能调度、设备维修、能耗分析、设备健康、运营报告、设备巡检等功能
"""

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Handoff
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import Swarm
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

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

# 创建模型客户端
model_client = OpenAIChatCompletionClient(
    model=MODEL_NAME,
    api_key=API_KEY,
    base_url=BASE_URL,
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.ANY,
        "structured_output": False,
    }
)

# ==================== 工具定义 ====================

# 空压站智能调度智能体工具
def start_compressor(compressor_id: str) -> str:
    """启动指定编号的空压机"""
    return f"空压机 {compressor_id} 已启动"


def stop_compressor(compressor_id: str) -> str:
    """停止指定编号的空压机"""
    return f"空压机 {compressor_id} 已停止"


def adjust_load(compressor_id: str, load_percentage: int) -> str:
    """调整空压机负荷百分比（0-100）"""
    return f"空压机 {compressor_id} 负荷已调整至 {load_percentage}%"


def get_air_demand() -> str:
    """获取当前用气需求"""
    return "当前用气需求：1200 m³/min，压力要求：0.7 MPa"


# 空压机设备维修助手工具
def diagnose_fault(equipment_id: str, symptom: str) -> str:
    """诊断设备故障"""
    return f"设备 {equipment_id} 故障诊断：根据症状'{symptom}'，可能是轴承磨损，建议检查润滑系统"


def get_repair_guide(fault_type: str) -> str:
    """获取维修指南"""
    guides = {
        "轴承磨损": "1. 停机断电 2. 拆卸轴承盖 3. 检查轴承状态 4. 更换轴承 5. 重新组装",
        "温度过高": "1. 检查冷却器 2. 清理散热片 3. 检查润滑油位 4. 检查环境通风",
        "振动异常": "1. 检查地脚螺栓 2. 检查转子平衡 3. 检查联轴器对中 4. 检查轴承间隙"
    }
    return guides.get(fault_type, f"未找到'{fault_type}'的维修指南，请联系技术支持")


def order_spare_parts(part_name: str, quantity: int) -> str:
    """订购备件"""
    return f"已下单订购 {quantity} 个 {part_name}，预计3天内到货"


# 空压站能耗分析智能体工具
def analyze_energy_consumption(period: str) -> str:
    """分析指定时段的能耗数据"""
    return f"{period}能耗分析：总耗电量 15,680 kWh，平均负载率 78%，单位产气能耗 0.12 kWh/m³"


def compare_energy_efficiency(compressor_ids: str) -> str:
    """对比多台设备的能效"""
    return f"设备 {compressor_ids} 能效对比：1号机 0.115 kWh/m³（最优），2号机 0.128 kWh/m³，3号机 0.132 kWh/m³"


def generate_energy_report() -> str:
    """生成能耗分析报告"""
    return "能耗分析报告：本月总能耗较上月降低5.2%，主要节能措施包括优化启停策略和负载分配"


# 空压设备健康智能体工具
def get_health_score(equipment_id: str) -> str:
    """获取设备健康评分（0-100）"""
    return f"设备 {equipment_id} 健康评分：85分，状态良好，建议关注轴承温度趋势"


def predict_maintenance(equipment_id: str) -> str:
    """预测维护需求"""
    return f"设备 {equipment_id} 预测性维护建议：预计15天后需要更换润滑油，30天后需要检查轴承"


def get_realtime_status(equipment_id: str) -> str:
    """获取设备实时运行状态"""
    return f"设备 {equipment_id} 实时状态：运行中，排气温度 95°C，排气压力 0.72 MPa，振动 2.3 mm/s，电流 85A"


# 空压站运营报告智能体工具
def generate_daily_report() -> str:
    """生成日报"""
    return "日报摘要：今日产气量 1,234,567 m³，设备平均负载率 82%，能耗成本 ¥45,678，无重大故障"


def generate_monthly_report() -> str:
    """生成月报"""
    return "月报摘要：本月总产气量 36,789 m³，总能耗 523,456 kWh，设备可用率 98.5%，节能建议：优化2号机启停策略"


def get_optimization_suggestions() -> str:
    """获取优化建议"""
    return "优化建议：1. 将3号机运行时间从高峰期调整至平谷期，预计月节省电费¥12,000 2. 更换1号机老化密封件，预计降低能耗3%"


# 空压站设备巡检智能体工具
def perform_visual_inspection(equipment_id: str) -> str:
    """执行视觉巡检"""
    return f"设备 {equipment_id} 视觉巡检结果：外观正常，无明显泄漏，仪表读数正常，发现轻微油渍需要清理"


def detect_anomaly(equipment_id: str) -> str:
    """检测设备异常"""
    return f"设备 {equipment_id} 异常检测：检测到轻微振动异常，建议重点关注，可能需要动平衡调整"


def record_inspection_result(equipment_id: str, result: str) -> str:
    """记录巡检结果"""
    return f"已记录设备 {equipment_id} 的巡检结果：{result}"


# ==================== 子智能体定义 ====================

# 通用 handoffs 函数 - 用于子智能体之间相互转发
def get_sub_agent_handoffs(agent_name: str) -> list:
    """获取子智能体的 handoffs 列表（排除自己）"""
    all_agents = [
        ("dispatch_agent", "空压站智能调度智能体，用于处理设备启停、负荷分配、运行优化、用气调度等问题"),
        ("maintenance_agent", "空压机设备维修助手，用于处理故障诊断、维修指南、备件订购等问题"),
        ("energy_analysis_agent", "空压站能耗分析智能体，用于处理能耗分析、能效对比、节能报告等问题"),
        ("health_agent", "空压设备健康智能体，用于处理设备健康评分、预测性维护、实时状态监测等问题"),
        ("report_agent", "空压站运营报告智能体，用于处理日报/月报生成、优化建议等问题"),
        ("inspection_agent", "空压站设备巡检智能体，用于处理视觉巡检、异常检测、巡检记录等问题"),
    ]
    return [Handoff(target=name, description=desc) for name, desc in all_agents if name != agent_name]


# 空压站智能调度智能体
dispatch_agent = AssistantAgent(
    "dispatch_agent",
    model_client=model_client,
    system_message="""你是空压站智能调度智能体。你的职责是基于AI算法与工业机理模型，实现对空压机组的自主启停、负荷分配及运行优化。

你的核心能力：
1. 实时监测用气需求与设备状态
2. 动态调整运行策略
3. 在保障供气品质的同时，显著降低能耗与运维成本
4. 提升系统整体效率

当用户询问关于设备调度、启停、负荷分配等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请使用 handoff 工具将任务转发给其他专业智能体。
完成回答后，请说"TERMINATE"结束对话。""",
    description="负责设备启停、负荷分配、运行优化、用气调度",
    tools=[start_compressor, stop_compressor, adjust_load, get_air_demand],
    handoffs=get_sub_agent_handoffs("dispatch_agent"),
)

# 空压机设备维修助手
maintenance_agent = AssistantAgent(
    "maintenance_agent",
    model_client=model_client,
    system_message="""你是空压机设备维修助手。你的职责是对设备故障进行维修、排查。

你的核心能力：
1. 故障诊断与分析
2. 提供维修指南和操作步骤
3. 备件管理与订购

当用户询问关于设备故障、维修方法、备件等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请使用 handoff 工具将任务转发给其他专业智能体。
完成回答后，请说"TERMINATE"结束对话。""",
    description="负责故障诊断、维修指南、备件订购",
    tools=[diagnose_fault, get_repair_guide, order_spare_parts],
    handoffs=get_sub_agent_handoffs("maintenance_agent"),
)

# 空压站能耗分析智能体
energy_analysis_agent = AssistantAgent(
    "energy_analysis_agent",
    model_client=model_client,
    system_message="""你是空压站能耗分析智能体。你的职责是通过集成多源数据与智能算法，实现对空压站运行状态的实时监控与能耗精准分析。

你的核心能力：
1. 实时监控与能耗分析
2. 支持设备间协同优化
3. 有效降低能源消耗
4. 提升系统运行效率与稳定性

当用户询问关于能耗分析、能效对比、节能报告等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请使用 handoff 工具将任务转发给其他专业智能体。
完成回答后，请说"TERMINATE"结束对话。""",
    description="负责能耗分析、能效对比、节能报告",
    tools=[analyze_energy_consumption, compare_energy_efficiency, generate_energy_report],
    handoffs=get_sub_agent_handoffs("energy_analysis_agent"),
)

# 空压设备健康智能体
health_agent = AssistantAgent(
    "health_agent",
    model_client=model_client,
    system_message="""你是空压设备健康智能体。你的职责是融合物联网与AI技术，实时监测空压设备运行状态。

你的核心能力：
1. 实时监测设备运行状态
2. 预测维护需求
3. 优化能效管理
4. 保障设备稳定运行
5. 降低故障率与能耗成本

当用户询问关于设备健康状态、预测性维护、实时监测等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请使用 handoff 工具将任务转发给其他专业智能体。
完成回答后，请说"TERMINATE"结束对话。""",
    description="负责设备健康评分、预测性维护、实时状态监测",
    tools=[get_health_score, predict_maintenance, get_realtime_status],
    handoffs=get_sub_agent_handoffs("health_agent"),
)

# 空压站运营报告智能体
report_agent = AssistantAgent(
    "report_agent",
    model_client=model_client,
    system_message="""你是空压站运营报告智能体。你的职责是融合多源数据与算法模型，自动分析空压站运行状态。

你的核心能力：
1. 自动分析空压站运行状态
2. 生成节能优化建议
3. 提供运维决策支持
4. 提升设备效率与管理水平

当用户询问关于运营报告、优化建议等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请使用 handoff 工具将任务转发给其他专业智能体。
完成回答后，请说"TERMINATE"结束对话。""",
    description="负责日报/月报生成、优化建议",
    tools=[generate_daily_report, generate_monthly_report, get_optimization_suggestions],
    handoffs=get_sub_agent_handoffs("report_agent"),
)

# 空压站设备巡检智能体
inspection_agent = AssistantAgent(
    "inspection_agent",
    model_client=model_client,
    system_message="""你是空压站设备巡检智能体。你的职责是融合AI视觉识别与物联网技术，自动识别设备异常状态。

你的核心能力：
1. 自动识别设备异常状态
2. 预测潜在故障风险
3. 提升工业设备运维效率与安全性

当用户询问关于设备巡检、异常检测等问题时，使用你的专业工具来响应。
如果用户的问题超出你的职责范围，请使用 handoff 工具将任务转发给其他专业智能体。
完成回答后，请说"TERMINATE"结束对话。""",
    description="负责视觉巡检、异常检测、巡检记录",
    tools=[perform_visual_inspection, detect_anomaly, record_inspection_result],
    handoffs=get_sub_agent_handoffs("inspection_agent"),
)

# ==================== 主调度智能体（使用 Handoffs）====================

main_agent = AssistantAgent(
    "main_agent",
    model_client=model_client,
    system_message="""你是空压站主调度智能体，负责理解用户需求并将任务分发给相应的专业智能体。

你有6个专业智能体可以协调：

1. dispatch_agent - 空压站智能调度智能体 - 负责：设备启停、负荷分配、运行优化、用气调度
2. maintenance_agent - 空压机设备维修助手 - 负责：故障诊断、维修指南、备件订购
3. energy_analysis_agent - 空压站能耗分析智能体 - 负责：能耗分析、能效对比、节能报告
4. health_agent - 空压设备健康智能体 - 负责：设备健康评分、预测性维护、实时状态监测
5. report_agent - 空压站运营报告智能体 - 负责：日报/月报生成、优化建议
6. inspection_agent - 空压站设备巡检智能体 - 负责：视觉巡检、异常检测、巡检记录

工作流程：
- 如果用户只是打招呼或询问你的功能，请直接友好地回复，简要介绍你可以提供的服务，然后说"TERMINATE"结束对话。
- 如果用户提出具体的专业问题（如设备调度、故障维修、能耗分析等），请使用相应的 handoff 工具将任务移交给专业智能体处理。
- 如果问题涉及多个领域，可以选择最相关的一个智能体处理。

请保持回复简洁友好。""",
    handoffs=get_sub_agent_handoffs("main_agent"),
)

# ==================== 创建 Team ====================

# 定义终止条件：检测到 TERMINATE 时停止
termination = TextMentionTermination("TERMINATE")

# 创建 Swarm 团队 - 主智能体作为入口，负责路由到专业智能体
team = Swarm(
    [main_agent, dispatch_agent, maintenance_agent, energy_analysis_agent, health_agent, report_agent, inspection_agent],
    termination_condition=termination
)

# ==================== 主程序 ====================

async def run_interactive():
    """交互式对话模式"""

    print("=" * 60)
    print()
    print(f"{Colors.YELLOW}[AutoGen Swarm]{Colors.RESET}")
    print()
    print("模型信息：")
    print(f"  BASE_URL={BASE_URL}, MODEL_NAME={MODEL_NAME}")
    print()
    print("可用功能：")
    print("  1. 设备调度 - 启停空压机、调整负荷、用气需求")
    print("  2. 故障维修 - 故障诊断、维修指南、备件订购")
    print("  3. 能耗分析 - 能耗统计、能效对比、节能报告")
    print("  4. 设备健康 - 健康评分、预测维护、实时状态")
    print("  5. 运营报告 - 日报月报、优化建议")
    print("  6. 设备巡检 - 视觉巡检、异常检测")
    print()
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 60)
    print()

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

            # 运行团队并收集结果
            from autogen_agentchat.ui import Console
            result = await Console(team.run_stream(task=user_input))
            # result = await team.run(task=user_input)

            # 从消息中提取最后的响应
            last_agent = None
            last_content = None

            for message in result.messages:
                # 获取消息来源
                if hasattr(message, 'source'):
                    last_agent = message.source
                # 获取消息内容
                if hasattr(message, 'content'):
                    last_content = message.content

            # 输出结果
            if last_agent and last_content:
                print(f"{Colors.BLUE}Assistant - {Colors.RESET}"
                      f"{Colors.YELLOW}[{last_agent}]{Colors.RESET}"
                      f"{Colors.BLUE}: {last_content}{Colors.RESET}", flush=True)
            print()

        except KeyboardInterrupt:
            print()
            print("程序已中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            print()


async def main():
    """主程序入口"""
    await run_interactive()


if __name__ == "__main__":
    asyncio.run(main())