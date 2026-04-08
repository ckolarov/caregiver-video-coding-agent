# Sample Input and Output

## Sample Input

**Video URL:** https://www.youtube.com/watch?v=_YR1WeOBc0E

**Description:** A short caregiver-child interaction video showing a parent and infant engaged in a play-based activity. The video is approximately 7 minutes long.

**Human-Coded Labels (optional):**
```json
{
  "motor_development": "present",
  "caregiver_behavior": "present",
  "safety_issue": "not observed",
  "scaffolding": "present"
}
```

## Sample Output

```json
{
  "video_id": "YR1WeOBc0E",
  "clip_id": "clip_1",
  "clip_window": "0:00-2:00",
  "clip_summary": "Caregiver is seated on the floor with the infant. The infant reaches for a toy while the caregiver provides verbal encouragement.",
  "rubric_codes": {
    "motor_development": "present",
    "caregiver_behavior": "present",
    "safety_issue": "absent",
    "scaffolding": "uncertain"
  },
  "evidence_notes": {
    "motor_development": "Infant is observed reaching and grasping a toy, consistent with fine motor milestone behavior.",
    "caregiver_behavior": "Caregiver is actively engaged, maintaining proximity and offering verbal cues.",
    "safety_issue": "No hazards observed in the immediate environment.",
    "scaffolding": "Caregiver provides verbal encouragement but it is unclear whether this constitutes intentional skill-building versus general praise."
  },
  "comparison_to_human": {
    "agreement": "high",
    "differences": [
      "scaffolding: AI coded 'uncertain', human coded 'present' — caregiver verbal cues may reflect intentional teaching, but AI could not confirm intent from video alone."
    ]
  },
  "review_flags": [
    "Scaffolding code requires human reviewer confirmation."
  ]
}
```

## Notes

- The AI system correctly identified motor development and caregiver behavior.
- Scaffolding remains the most frequently disagreed-upon category between AI and human coders, consistent with the literature on inter-rater reliability for this construct.
- Safety coding showed full agreement, as expected for videos without observable hazards.
