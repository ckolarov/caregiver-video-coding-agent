---
name: caregiver-video-coding-agent
description: Use this skill when a researcher wants help analyzing caregiver-child interaction videos, creating first-pass behavioral coding summaries, segmenting long videos into smaller clips, or comparing AI-generated codes with human-coded labels for developmental psychology research.
trigger_words:
  - caregiver child video
  - infant behavior coding
  - developmental psychology
  - behavioral coding
  - scaffolding
  - video segmentation
  - human coder comparison
---

# Overview

This skill supports a developmental psychology workflow in which researchers analyze caregiver-child interaction videos and produce structured behavioral codes. It is designed for a demo-ready AI system that accepts a video or clip description, suggests segmentation for long recordings, generates first-pass behavioral coding, and compares AI outputs against human-coded labels.

This skill is meant to support human researchers, not replace them.

# Step-by-Step Instructions

1. Identify the input type:
   - video URL
   - hosted video file
   - clip transcript
   - researcher summary of a clip

2. If the source video is long, segment it into short clips before analysis.
   - Default segment size: 1 to 2 minutes
   - Preserve clip IDs and time windows

3. Apply the project rubric:
   - motor_development
   - caregiver_behavior
   - safety_issue
   - scaffolding

4. Restrict coding to observable evidence.

5. If a category is ambiguous, especially scaffolding, label it as uncertain and explain why.

6. When human-coded labels are available, compare AI output against the human codes.

7. Return a structured result that a research assistant can review quickly.

# Output Format

Return results in this structure:

```json
{
  "video_id": "string",
  "clip_id": "string",
  "clip_window": "start-end",
  "clip_summary": "short neutral description",
  "rubric_codes": {
    "motor_development": "present | absent | uncertain",
    "caregiver_behavior": "present | absent | uncertain",
    "safety_issue": "present | absent | uncertain",
    "scaffolding": "present | absent | uncertain"
  },
  "evidence_notes": {
    "motor_development": "why",
    "caregiver_behavior": "why",
    "safety_issue": "why",
    "scaffolding": "why"
  },
  "comparison_to_human": {
    "agreement": "high | medium | low | not_available",
    "differences": []
  },
  "review_flags": []
}
```

# Rules and Edge Cases

- Only describe observable behavior.
- Do not diagnose a child or infer mental states as facts.
- Treat scaffolding as a high-uncertainty category unless teaching behavior is clearly visible.
- If the clip is too short or too blurry, return `uncertain` instead of guessing.
- If the user requests a definitive safety or developmental diagnosis, refuse and redirect to expert human review.

# Safety Guardrail

This skill is for research assistance and structured observation only. It must not be used to make medical, developmental, legal, or child-safety determinations without qualified human oversight.

# Files

- `references/sample-input-output.md` contains a sample use case
- `templates/coding-output-template.json` contains a reusable output template
- `templates/report-template.md` contains a short reporting template
- `scripts/rubric_notes.py` contains the starter rubric used by the prototype
