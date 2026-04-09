# DevWatch — Poster Board Brief

Use this document to build the poster. Everything your teammate needs is here.

---

## 1. PROJECT TITLE

**DevWatch: AI-Powered Child Development Video Analysis**

Tagline: *"Helping parents understand their child's cognitive growth through video."*

---

## 2. PROBLEM STATEMENT

Parents and caregivers want to understand how their child is developing, but interpreting everyday interactions — play, movement, verbal exchanges — requires specialized training in developmental psychology. Professional behavioral coding (like DPICS-IV) is expensive, time-consuming, and inaccessible to most families.

**The question:** Can AI observe a caregiver-child interaction video and provide meaningful, research-grounded developmental insights that are useful to parents?

---

## 3. WHAT DEVWATCH DOES

DevWatch is a web application where a parent or researcher can:

1. **Paste a YouTube link** of a caregiver-child interaction video
2. **AI watches the actual video** using Google Gemini's multimodal vision capabilities
3. **Get a structured developmental report** that includes:
   - What motor/movement behaviors were observed in the child
   - How the caregiver is communicating (classified using DPICS-IV categories)
   - Whether learning support/scaffolding is happening
   - Safety observations
   - **What these behaviors mean for cognitive development**
   - **What developmental stage the child appears to be in**
   - **How the caregiver's communication style impacts development**
   - **Specific, actionable tips for supporting growth**

**Live website:** https://ckolarov.github.io/caregiver-video-coding-agent/

---

## 4. RESEARCH FOUNDATION

### Primary Paper
**Zamfirescu-Pereira et al. (2024).** "Artificial intelligence–powered 3D analysis of video-based caregiver-child interactions." *Science Advances*, 10.
- DOI: https://www.science.org/doi/10.1126/sciadv.adp4422
- Introduced the **HARMONI** framework for AI-powered analysis of caregiver-child interactions from observational video
- Showed that AI can capture meaningful interaction patterns that relate to developmental outcomes

### Behavioral Coding Frameworks Used

**DPICS-IV (Dyadic Parent-Child Interaction Coding System)**
- Gold standard for coding parent communication during therapy
- 10 categories we trained the AI to recognize:

| Code | Category | Example |
|------|----------|---------|
| LP | Labeled Praise | "Great job stacking those blocks!" |
| UP | Unlabeled Praise | "Good!" "Nice!" |
| RF | Reflection | Repeating child's words back |
| BD | Behavior Description | "You're pushing the car." |
| IQ | Information Question | "What color is that?" |
| DQ | Descriptive Question | "Is that a big one?" |
| IC | Indirect Command | "Can you clean up now?" |
| DC | Direct Command | "Clean up now." |
| NTA | Negative Talk | Critical or disapproving statements |
| TA | Neutral Talk | General conversation |

**PC-SCP (Parent/Caregiver Support of Children's Playfulness)**
- Rates how well a caregiver supports a child's playful engagement
- We use this to assess scaffolding quality, joint attention, and child autonomy

### Key Research Connections (for poster visuals)

| Observed Behavior | Cognitive Development Link |
|---|---|
| Reaching & grasping | Hand-eye coordination → problem-solving |
| Object exploration (mouthing, banging) | Cause-and-effect reasoning |
| Crawling & walking | Spatial reasoning & memory |
| Joint attention | Foundation for language & theory of mind |
| Caregiver behavior descriptions | Vocabulary development |
| Labeled praise | Self-regulation skills |
| Caregiver reflections | Speech & communication development |
| Scaffolding | Zone of proximal development → accelerated cognitive growth |
| Negative talk | Can hinder executive function development |
| Turn-taking | Social cognition & language processing |

---

## 5. HOW WE BUILT IT

### Architecture Overview

```
[YouTube Video URL]
        ↓
[Google Gemini API — Multimodal Video Analysis]
        ↓
[Research-Grounded Expert Prompt]
  (DPICS-IV + PC-SCP frameworks embedded)
        ↓
[Structured JSON Response]
        ↓
[DevWatch Dashboard — Single-File HTML App]
  - At a Glance cards (color-coded)
  - Detailed observations
  - Cognitive development insights
  - Caregiver communication analysis
  - Actionable parent tips
  - Analysis history (localStorage)
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Single-file HTML/CSS/JavaScript (no frameworks) |
| AI Model | Google Gemini 2.5 Flash (multimodal video) |
| Video Input | YouTube URL → Gemini fileData API |
| Hosting | GitHub Pages (free, auto-deploys) |
| Data Storage | Browser localStorage (analysis history) |
| Backend Agent | Python + LangChain/LangGraph (assignment5.py) |

### Key Technical Decisions

- **Single-file architecture**: The entire website is one `index.html` file — no build tools, no server, no dependencies. Anyone can open it in a browser.
- **Multimodal video analysis**: Gemini actually watches the video frames (not just reading the URL as text). This enables real observation of movements, facial expressions, and interactions.
- **Research-grounded prompt engineering**: Instead of fine-tuning a model, we embedded the DPICS-IV and PC-SCP frameworks directly into the system prompt. This gives the AI expert-level knowledge about what to look for and how to interpret it.
- **Automatic model fallback**: If one Gemini model is overloaded, the system automatically tries alternatives (2.5-flash → 2.5-flash-lite → 2.0-flash) with both video and text-only modes.
- **In-browser API key management**: Users paste their own Gemini API key — no server needed, keys stored in localStorage.

---

## 6. COOL FEATURES (for poster highlights)

1. **Actually watches the video** — not just reading a URL. Gemini's multimodal AI processes the video frames to observe real behaviors.

2. **DPICS-IV classification** — Classifies caregiver communication into 10 research-validated categories (praise types, commands, reflections, behavior descriptions, etc.)

3. **Cognitive development connections** — Doesn't just describe what it sees. Explains WHY each behavior matters for brain development (e.g., "reaching builds hand-eye coordination, a precursor to problem-solving").

4. **Caregiver impact analysis** — Tells parents how their specific communication style affects their child's development, with both positive feedback and constructive suggestions.

5. **Embedded YouTube preview** — Paste a URL and the video loads right in the dashboard.

6. **Analysis history** — All past analyses saved locally so parents can track development over time.

7. **Honest assessments** — Unlike generic AI tools, DevWatch is designed to be honest. If a child is distressed or a caregiver is disengaged, it says so (gently).

8. **Zero setup** — No account needed, no app to install. Just open the website, paste an API key, and go.

---

## 7. AGENTIC CAPABILITIES

### Multi-Agent Python Pipeline (assignment5.py)
- **Clip Coding Agent**: Segments long videos and generates first-pass behavioral codes
- **Validation Agent**: Compares AI codes against human-coded labels, computes agreement rates
- **Orchestration Agent**: Coordinates the other two agents and produces a final researcher-facing report
- **Memory Agent**: Retains project context across multi-turn conversations
- Built with **LangChain + LangGraph** using Google Gemini as the LLM
- Uses **Tavily API** for web search when agents need external research context

### Web App (index.html)
- Agentic model selection: automatically cycles through multiple AI models
- Structured prompt engineering grounded in real behavioral coding frameworks
- Multimodal video understanding via Gemini API

---

## 8. LIMITATIONS

| Limitation | Explanation |
|------------|-------------|
| **Not a diagnostic tool** | DevWatch provides observations, not diagnoses. Professional evaluation is always recommended for concerns. |
| **Video quality matters** | Low-resolution, poor lighting, or heavy background noise reduces accuracy. |
| **Voiceover videos are hard** | Videos with narrator voiceover (not natural parent-child dialogue) make verbal interaction analysis unreliable. |
| **YouTube only** | Currently only supports YouTube links — no direct file upload. |
| **API rate limits** | Free Gemini API tier has usage limits. During high demand, analysis may temporarily fail. |
| **No ground truth validation** | We haven't compared AI outputs against human DPICS-IV coders on our specific use case. Published research shows ~72-80% accuracy on text classification, ~38-61% on video behavioral scoring. |
| **Scaffolding is hard for AI** | Scaffolding requires inferring caregiver intent, which is inherently difficult from video alone. This is the most unreliable category. |
| **Single interaction snapshot** | One video doesn't represent a child's full developmental profile. Longitudinal observation is always better. |

---

## 9. FUTURE WORK

- **Direct video upload** (not just YouTube) using Gemini File API
- **Speech-to-text layer** (OpenAI Whisper) for more accurate verbal interaction analysis
- **Longitudinal tracking** — compare analyses over weeks/months to show developmental progress
- **Human coder comparison** — validate AI outputs against trained DPICS-IV coders
- **Fine-tuned video model** — use Qwen2.5-VL for specialized behavioral scoring (per the ScienceDirect 2026 paper)

---

## 10. TEAM

| Name | Email |
|------|-------|
| Connor Kolarov | cdkolarov@wm.edu |
| Zoe Zung | zzung@wm.edu |
| Julia Levy | jdlevy@wm.edu |
| Trey McDonald | fmcdonald@wm.edu |

**William & Mary MSBA — AI Class — Spring 2026**

---

## 11. POSTER LAYOUT SUGGESTION

```
┌─────────────────────────────────────────────────────┐
│                    DEVWATCH                          │
│   AI-Powered Child Development Video Analysis       │
│   W&M MSBA · AI Class · Spring 2026                │
├──────────────────┬──────────────────────────────────┤
│                  │                                  │
│  PROBLEM         │  HOW IT WORKS                    │
│  STATEMENT       │  (3-step flow diagram)           │
│                  │  1. Paste URL                    │
│                  │  2. AI Watches Video             │
│                  │  3. Get Insights                 │
│                  │                                  │
├──────────────────┼──────────────────────────────────┤
│                  │                                  │
│  RESEARCH        │  KEY FEATURES                    │
│  FOUNDATION      │  - DPICS-IV classification       │
│  - HARMONI paper │  - Cognitive dev connections     │
│  - DPICS-IV      │  - Caregiver impact analysis     │
│  - PC-SCP        │  - Honest assessments            │
│                  │  - Analysis history              │
│                  │                                  │
├──────────────────┼──────────────────────────────────┤
│                  │                                  │
│  BEHAVIOR →      │  WEBSITE SCREENSHOT              │
│  COGNITION       │  (dashboard + results view)      │
│  TABLE           │                                  │
│  (visual)        │                                  │
│                  │                                  │
├──────────────────┼──────────────────────────────────┤
│                  │                                  │
│  TECH STACK &    │  LIMITATIONS &                   │
│  ARCHITECTURE    │  FUTURE WORK                     │
│  DIAGRAM         │                                  │
│                  │                                  │
├──────────────────┴──────────────────────────────────┤
│  TEAM: Connor · Zoe · Julia · Trey                  │
│  [headshot] [headshot] [headshot] [headshot]         │
│  Live: ckolarov.github.io/caregiver-video-coding-agent │
└─────────────────────────────────────────────────────┘
```

---

## 12. QR CODE

Generate a QR code pointing to the live site for the poster:
**https://ckolarov.github.io/caregiver-video-coding-agent/**

(Use any free QR generator like qr-code-generator.com)

---

## 13. DEMO SCRIPT (for judges)

1. Open the live site on a laptop
2. Show the dashboard — explain the 3-step flow
3. Paste a YouTube video of a real caregiver-child interaction
4. Click Analyze — while it loads, explain the research frameworks (DPICS-IV, HARMONI)
5. Walk through the results: observations, cognitive insights, caregiver impact, tips
6. Show analysis history — "parents can track development over time"
7. Show the About page — research foundation, team
8. Mention limitations honestly — "this is a first-pass tool, not a replacement for professionals"
