# =========================
# 0. Imports and setup
# =========================
import os
import json
import time
from typing import Dict, Any, List, Optional
from pprint import pprint


def pretty_print_message_content(content):
    """Helper to print message content regardless of format."""
    if isinstance(content, str):
        print(content)
    elif isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
        print("".join(text_parts))
    else:
        print(content)


from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from tavily import TavilyClient

# =========================
# 1. LLM INITIALIZATION
# =========================
MODEL_NAME = os.getenv("LC_MODEL", "google_genai:gemini-2.5-flash")
DEMO_VIDEO_URL = os.getenv(
    "DEMO_VIDEO_URL",
    "https://www.youtube.com/watch?v=_YR1WeOBc0E",
)

llm_precise = init_chat_model(
    model=MODEL_NAME,
    temperature=0.1,
)

direct_prompt = HumanMessage(
    content=(
        "We are building a developmental psychology video analysis prototype. "
        "In one short paragraph, explain why a low-temperature model is useful "
        "for structured behavioral coding."
    )
)

print("\n=== SECTION 1: Direct LLM Invocation ===")
try:
    direct_response = llm_precise.invoke([direct_prompt])
    print(direct_response.content)
except Exception:
    print(
        "Section 1 could not fully complete because the Gemini free-tier "
        "quota was exceeded during the demo."
    )

# =========================
# 2. CUSTOM TOOLS
# =========================
BEHAVIOR_RUBRIC = {
    "motor_development": "Evidence of infant motor behavior or milestone-related movement.",
    "caregiver_behavior": "Observable caregiver actions toward the child.",
    "safety_issue": "Potential physical or situational safety concern.",
    "scaffolding": "Caregiver intentionally supporting skill learning or guided development.",
}


@tool
def propose_video_segments(
    video_length_minutes: float, segment_size_minutes: int = 2
) -> List[Dict[str, float]]:
    """
    Create a simple segmentation plan for a long caregiver-child video.

    Args:
        video_length_minutes: Total length of the source video in minutes.
        segment_size_minutes: Desired size of each clip in minutes.

    Returns:
        A list of dictionaries, where each dictionary contains:
        - clip_id: clip number
        - start_minute: segment start
        - end_minute: segment end

    Safety guardrail:
        This tool only creates a segment plan. It does not infer behavior,
        diagnose development, or make claims about abuse or neglect.
    """
    if video_length_minutes <= 0:
        return []

    segments: List[Dict[str, float]] = []
    start = 0.0
    clip_id = 1

    while start < video_length_minutes:
        end = min(start + segment_size_minutes, video_length_minutes)
        segments.append(
            {
                "clip_id": clip_id,
                "start_minute": round(start, 2),
                "end_minute": round(end, 2),
            }
        )
        start = end
        clip_id += 1

    return segments


@tool
def compare_ai_to_human_codes(
    ai_codes: Dict[str, str],
    human_codes: Dict[str, str],
) -> Dict[str, Any]:
    """
    Compare AI-generated behavioral codes to human-coded labels.

    Args:
        ai_codes: Dictionary of rubric categories mapped to AI observations.
        human_codes: Dictionary of rubric categories mapped to human observations.

    Returns:
        Dictionary containing:
        - matches: exact category matches
        - mismatches: category-by-category differences
        - agreement_rate: exact-match agreement ratio from 0 to 1

    Safety guardrail:
        This tool is for research comparison only. It does not replace expert review.
    """
    keys = sorted(set(ai_codes.keys()) | set(human_codes.keys()))
    matches = {}
    mismatches = {}
    same_count = 0

    for key in keys:
        ai_val = str(ai_codes.get(key, "")).strip().lower()
        human_val = str(human_codes.get(key, "")).strip().lower()
        if ai_val == human_val and ai_val != "":
            matches[key] = {"ai": ai_codes.get(key), "human": human_codes.get(key)}
            same_count += 1
        else:
            mismatches[key] = {"ai": ai_codes.get(key), "human": human_codes.get(key)}

    agreement_rate = same_count / len(keys) if keys else 0.0
    return {
        "matches": matches,
        "mismatches": mismatches,
        "agreement_rate": round(agreement_rate, 3),
    }


@tool
def rubric_template() -> Dict[str, str]:
    """
    Return the project's initial behavioral coding rubric.

    Returns:
        A dictionary mapping rubric categories to short descriptions.
    """
    return BEHAVIOR_RUBRIC


# =========================
# 3. EXTERNAL API TOOL
# =========================
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> Dict[str, Any]:
    """
    Search the web for supporting research or implementation guidance.

    Args:
        query: Search query string.

    Returns:
        Tavily search results as a dictionary.
    """
    return tavily_client.search(query=query, max_results=3)


# =========================
# 4. AGENT CREATION
# =========================
clip_coding_agent = create_react_agent(
    model=llm_precise,
    tools=[rubric_template, propose_video_segments],
    prompt="""
You are the Clip Coding Agent for a developmental psychology research platform.

Your job:
1. Use the rubric_template tool when needed.
2. Help turn a video or clip description into structured behavioral codes.
3. Stay grounded in observable behavior only.
4. If scaffolding is unclear, explicitly say it is uncertain.

Output format:
- clip_summary
- observed_behaviors
- rubric_codes
- confidence_notes

Do not diagnose a child. Do not overclaim hidden intentions.
""",
)

validation_agent = create_react_agent(
    model=llm_precise,
    tools=[compare_ai_to_human_codes, web_search],
    prompt="""
You are the Validation Agent for a developmental psychology AI prototype.

Your job:
1. Compare AI-produced behavioral codes against human-coded labels.
2. Flag likely disagreement areas, especially scaffolding.
3. Use web_search only when the user asks for external context or best practices.
4. Explain what should be reviewed by a human coder.

Be conservative and methodical.
""",
)

# =========================
# 5. MESSAGE HANDLING
# =========================
print("\n=== SECTION 5: Multi-turn Message Handling ===")

multi_turn_messages = [
    HumanMessage(
        content=(
            "We have a 7-minute caregiver-child interaction video. "
            "Please think about a good segmentation plan before coding."
        )
    ),
    AIMessage(
        content=(
            "A short segmentation strategy is useful because long videos may exceed "
            "token or upload constraints and may mix different interaction contexts."
        )
    ),
    HumanMessage(
        content=(
            "Now produce a first-pass plan for segmenting the video and remind me "
            "which categories are hardest for AI."
        )
    ),
]

try:
    multi_turn_response = clip_coding_agent.invoke({"messages": multi_turn_messages})
    pretty_print_message_content(multi_turn_response["messages"][-1].content)
except Exception:
    print(
        "Section 5 could not fully complete because the Gemini free-tier "
        "quota was exceeded during the demo."
    )

# =========================
# 6. STREAMING OUTPUT
# =========================
print("\n=== SECTION 6: Streaming Output ===")

stream_prompt = HumanMessage(
    content=(
        "Given our project, explain a researcher-friendly workflow from video input "
        "to behavioral coding output."
    )
)

try:
    for token, metadata in clip_coding_agent.stream(
        {"messages": [stream_prompt]},
        stream_mode="messages",
    ):
        content = getattr(token, "content", None)

        if isinstance(content, str):
            print(content, end="", flush=True)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    print(item.get("text", ""), end="", flush=True)

    print()
except Exception:
    print(
        "Section 6 could not fully complete because the Gemini free-tier "
        "quota was exceeded during the demo."
    )

# =========================
# 7. AGENT MEMORY
# =========================
memory_enabled_agent = create_react_agent(
    model=llm_precise,
    tools=[rubric_template],
    checkpointer=MemorySaver(),
    prompt="""
You are the Memory Agent for the video analysis prototype.
Remember important project context from earlier turns in the same thread.
""",
)

config = {"configurable": {"thread_id": "video-analysis-demo-thread"}}

print("\n=== SECTION 7: Agent Memory ===")
try:
    memory_enabled_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Remember that our hardest category is scaffolding and our demo input "
                        "is a YouTube caregiver-child interaction video."
                    )
                )
            ]
        },
        config=config,
    )

    memory_follow_up = memory_enabled_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What key project details did I ask you to remember?"
                )
            ]
        },
        config=config,
    )
    pretty_print_message_content(memory_follow_up["messages"][-1].content)
except Exception:
    print(
        "Section 7 could not fully complete because the Gemini free-tier "
        "quota was exceeded during the demo."
    )

# =========================
# 8. MULTI-AGENT ORCHESTRATION
# =========================


@tool
def call_clip_coding_agent(task: str) -> str:
    """
    Ask the Clip Coding Agent to help with coding or segmentation.

    Args:
        task: Natural-language instruction for the clip coding agent.

    Returns:
        The clip coding agent's text response.
    """
    response = clip_coding_agent.invoke({"messages": [HumanMessage(content=task)]})
    return response["messages"][-1].content


@tool
def call_validation_agent(task: str) -> str:
    """
    Ask the Validation Agent to help compare AI and human coding results.

    Args:
        task: Natural-language instruction for the validation agent.

    Returns:
        The validation agent's text response.
    """
    response = validation_agent.invoke({"messages": [HumanMessage(content=task)]})
    return response["messages"][-1].content


orchestration_agent = create_react_agent(
    model=llm_precise,
    tools=[call_clip_coding_agent, call_validation_agent],
    prompt="""
You are the Orchestration Agent for the AI Video Analysis Platform.

Workflow:
1. Delegate coding and segmentation questions to call_clip_coding_agent.
2. Delegate agreement-checking and evaluation tasks to call_validation_agent.
3. Combine both outputs into a final researcher-facing answer.

Final answers should be practical, concise, and aligned with the developmental
psychology research workflow.
""",
)

print("\n=== SECTION 8: Multi-Agent Orchestration ===")

orchestration_prompt = HumanMessage(
    content=(
        "We are demoing one caregiver-child video. Create a small plan that includes "
        "segmentation, first-pass coding, and comparison against human labels."
    )
)

try:
    time.sleep(5)
    orchestration_response = orchestration_agent.invoke(
        {"messages": [orchestration_prompt]}
    )
    pretty_print_message_content(orchestration_response["messages"][-1].content)
except Exception:
    print(
        "Section 8 could not fully complete because the Gemini free-tier "
        "quota was exceeded during the demo."
    )

# =========================
# 9. OPTIONAL DEMO PAYLOADS
# =========================
demo_ai_codes = {
    "motor_development": "present",
    "caregiver_behavior": "present",
    "safety_issue": "not observed",
    "scaffolding": "uncertain",
}

demo_human_codes = {
    "motor_development": "present",
    "caregiver_behavior": "present",
    "safety_issue": "not observed",
    "scaffolding": "present",
}

print("\n=== OPTIONAL: Tool Demo ===")
pprint(
    propose_video_segments.invoke(
        {"video_length_minutes": 7, "segment_size_minutes": 2}
    )
)
pprint(
    compare_ai_to_human_codes.invoke(
        {"ai_codes": demo_ai_codes, "human_codes": demo_human_codes}
    )
)
