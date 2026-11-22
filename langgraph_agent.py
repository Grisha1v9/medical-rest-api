from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict, total=False):
    age: int
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int
    temperature: float
    symptoms: Optional[str]
    risk_level: str
    recommendation: str


def analyze_node(state: AgentState) -> AgentState:
    """Определяем уровень риска по правилам."""
    score = 0
    if state["age"] > 60:
        score += 1
    if state["systolic_bp"] > 140 or state["diastolic_bp"] > 90:
        score += 2
    if state["heart_rate"] > 100 or state["heart_rate"] < 60:
        score += 1
    if state["temperature"] > 37.5:
        score += 1

    if score >= 3:
        risk = "HIGH"
    elif score == 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    return {**state, "risk_level": risk}


def recommend_node(state: AgentState) -> AgentState:
    """Формируем рекомендацию в зависимости от риска."""
    recs = {
        "LOW": "Состояние стабильное. Рекомендован плановый осмотр.",
        "MEDIUM": "Требуется консультация терапевта в ближайшие дни.",
        "HIGH": "Высокий риск. Необходима срочная госпитализация.",
    }
    return {**state, "recommendation": recs[state["risk_level"]]}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("analyze", analyze_node)
    graph.add_node("recommend", recommend_node)
    graph.set_entry_point("analyze")
    graph.add_edge("analyze", "recommend")
    graph.add_edge("recommend", END)
    return graph.compile()


agent = build_graph()


def run_agent(data: dict) -> dict:
    return agent.invoke(data)