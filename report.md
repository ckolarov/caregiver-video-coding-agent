# Caregiver Video Coding Agent — Project Report

## System Overview

This project implements a multi-agent AI system for developmental psychology research. The platform analyzes caregiver-child interaction videos and produces structured behavioral coding output across four rubric categories: motor development, caregiver behavior, safety issues, and scaffolding. The system is built with LangChain and LangGraph in Python, uses Google Gemini as the underlying LLM, and includes a browser-based research interface powered by the Gemini API.

The prototype is designed to assist human researchers with first-pass behavioral coding, not to replace expert judgment. All outputs include confidence notes and review flags to ensure qualified human oversight remains central to the workflow.

## Agent Architecture

The system uses three specialized agents coordinated through a multi-agent orchestration pattern:

**Clip Coding Agent** — Responsible for video segmentation planning and first-pass behavioral coding. This agent has access to the rubric template tool and the video segmentation tool. It produces structured output containing clip summaries, observed behaviors, rubric codes, and confidence notes. It is instructed to stay grounded in observable behavior and to flag uncertainty, especially for scaffolding.

**Validation Agent** — Compares AI-generated behavioral codes against human-coded labels. This agent uses the comparison tool to compute exact-match agreement rates and identify category-level mismatches. It also has access to web search for retrieving external best practices or research context when requested. It is designed to be conservative and methodical.

**Orchestration Agent** — Acts as the top-level coordinator. It delegates coding and segmentation tasks to the Clip Coding Agent and evaluation tasks to the Validation Agent, then combines their outputs into a single researcher-facing answer. This pattern allows each sub-agent to specialize while the orchestrator manages workflow sequencing.

## Tools and External Integration

The system defines four custom tools and one external API integration:

- **propose_video_segments** — Divides a long video into fixed-length clips for sequential analysis. Includes a safety guardrail stating it does not infer behavior or make diagnostic claims.
- **rubric_template** — Returns the project's four-category behavioral coding rubric as a structured dictionary.
- **compare_ai_to_human_codes** — Computes exact-match agreement between AI and human labels across rubric categories, returning matches, mismatches, and an agreement rate.
- **web_search** — Uses the Tavily API to retrieve supporting research or implementation guidance from the web.
- **call_clip_coding_agent / call_validation_agent** — Wrapper tools that allow the orchestration agent to delegate tasks to sub-agents by passing natural-language instructions.

API keys for Gemini and Tavily are loaded from environment variables. No keys are hardcoded.

## Skill Folder Design

The project includes a structured skill folder (`caregiver-video-coding-agent/`) that packages the behavioral coding workflow as a reusable skill. The folder contains:

- **SKILL.md** — Defines the skill metadata, trigger words, step-by-step instructions, output format, rules, edge cases, and safety guardrails.
- **references/sample-input-output.md** — Provides a concrete example of input (video URL and human labels) and expected output (structured JSON with codes, evidence, comparison, and review flags).
- **templates/coding-output-template.json** — A blank JSON template matching the output schema for reuse across analyses.
- **templates/report-template.md** — A markdown mini-report template for documenting individual clip analyses.
- **scripts/rubric_notes.py** — Contains the starter behavioral rubric dictionary used by the prototype.

## Design Decisions

- **Low temperature (0.1)** was chosen to maximize consistency and reproducibility in behavioral coding output, minimizing creative drift in structured observation tasks.
- **Scaffolding is treated as high-uncertainty by default** because it requires inferring caregiver intent, which is inherently difficult from video observation alone and is the category most prone to inter-rater disagreement.
- **Safety guardrails are embedded at the tool level**, not just the prompt level, ensuring that even direct tool invocations include disclaimers about the limitations of AI-generated behavioral codes.
- **The orchestration pattern uses tool-based delegation** rather than direct function calls, allowing the LLM to decide when and how to route tasks between sub-agents based on the user's request.
- **The browser interface (index.html) uses direct Gemini API calls** rather than a backend server, keeping the demo self-contained and easy to deploy as a single file.
- **Agent memory (Section 7)** demonstrates that the system can retain project context across conversational turns, which is important for multi-session research workflows.
