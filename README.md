# DevWatch: AI-Powered Child Development Video Analysis

> **[Click here to view the live website](https://ckolarov.github.io/caregiver-video-coding-agent/)** | **[View the Code Demo (assignment5.py)](assignment5.py)**

---

## Authors

| | Name | GitHub | Email |
|---|---|---|---|
| ![Connor](images/connor.jpg) | **Connor Kolarov** | [@ckolarov](https://github.com/ckolarov) | cdkolarov@wm.edu |
| ![Zoe](images/zoe.jpg) | **Zoe Zung** | [@zoezung](https://github.com/zoezung) | zzung@wm.edu |
| ![Julia](images/julia.jpg) | **Julia Levy** | [@julialevy](https://github.com/julialevy) | jdlevy@wm.edu |
| ![Trey](images/trey.jpg) | **Trey McDonald** | [@treymcdonald](https://github.com/treymcdonald) | fmcdonald@wm.edu |

**William & Mary MSBA — AI Class — Spring 2026**

---

## Project Scope

DevWatch is a narrowly focused AI tool that does one thing well: **it watches a video of a caregiver interacting with a child and produces a structured developmental analysis grounded in established behavioral coding frameworks.** It is not a general-purpose child development platform, not a diagnostic tool, and not a replacement for professional evaluation. It is a first-pass observation assistant for parents and researchers.

The system accepts a YouTube video URL, sends it to Google Gemini's multimodal video API, and returns analysis structured around two research-validated frameworks: DPICS-IV (for caregiver communication) and PC-SCP (for scaffolding and play support). The output explains what behaviors were observed, what they mean for cognitive development, and what the caregiver can do to support growth.

---

## Why This Matters

Understanding child development is critical for parents, educators, and clinicians — but interpreting everyday caregiver-child interactions requires specialized training. Professional behavioral coding systems like DPICS-IV are the gold standard in developmental psychology, but they require trained human coders, are expensive, and are inaccessible to most families.

Recent research has shown that AI can meaningfully analyze these interactions. The **HARMONI** framework (Zamfirescu-Pereira et al., 2024, *Science Advances*) demonstrated that AI-powered 3D analysis of observational videos can capture patterns in caregiver-child interactions that relate to developmental outcomes. Separately, work on automated DPICS coding (FIU, 2023) achieved 72-80% accuracy in classifying parent utterances, and the Qwen2.5VL play assessment study (2026) showed feasibility of video-based behavioral scoring.

DevWatch brings these research advances together into an accessible tool that any parent can use.

---

## How It Works

```
┌──────────────────┐     ┌───────────────────────────┐     ┌──────────────────────┐
│                  │     │                           │     │                      │
│  1. Paste a      │────>│  2. Gemini Watches the    │────>│  3. Structured       │
│  YouTube URL     │     │  Video (multimodal AI)    │     │  Developmental       │
│                  │     │                           │     │  Report              │
└──────────────────┘     └───────────────────────────┘     └──────────────────────┘
                                    │
                         ┌──────────┴──────────┐
                         │  Expert Prompt with  │
                         │  DPICS-IV + PC-SCP   │
                         │  frameworks embedded │
                         └─────────────────────┘
```

### What the AI observes in the child:
- **Gross motor**: crawling, walking, climbing, pulling to stand, cruising
- **Fine motor**: reaching, grasping (palmar vs pincer), stacking, pointing, object transfer
- **Exploratory**: mouthing, dropping/throwing to test gravity, opening containers
- **Social-emotional**: eye contact, social referencing, joint attention, turn-taking, imitation
- **Verbal/pre-verbal**: babbling, word attempts, pointing + vocalizing, responding to name

### What the AI observes in the caregiver (DPICS-IV):

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

### What the AI assesses in the interaction (PC-SCP):
- Scaffolding quality — is the caregiver adjusting difficulty to match the child?
- Joint attention — are caregiver and child focused on the same thing?
- Turn-taking — are there back-and-forth exchanges?
- Child autonomy — is the child allowed to explore freely?

### How behaviors connect to cognitive development:

| Observed Behavior | Cognitive Development Link |
|---|---|
| Reaching & grasping | Hand-eye coordination, foundation for problem-solving |
| Object exploration | Cause-and-effect reasoning, early scientific thinking |
| Crawling & walking | Spatial reasoning and memory |
| Joint attention | Foundation for language and theory of mind |
| Caregiver behavior descriptions | Vocabulary development |
| Labeled praise | Self-regulation skills |
| Reflections | Speech and communication development |
| Scaffolding | Zone of proximal development, accelerated cognitive growth |
| Negative talk | Can hinder executive function development |

---

## Project Details

### Architecture

The project has two main components:

**1. DevWatch Web App (`index.html`)** — A single-file dashboard application hosted on GitHub Pages. No frameworks, no build tools, no server. Users paste a YouTube URL, the app sends it to the Gemini API with a research-grounded expert prompt, and displays structured results.

**2. Multi-Agent Pipeline (`assignment5.py`)** — A Python-based LangChain/LangGraph system with four specialized agents:
- **Clip Coding Agent**: Segments long videos and generates first-pass behavioral codes using the project rubric
- **Validation Agent**: Compares AI-generated codes against human-coded labels and computes agreement rates
- **Orchestration Agent**: Coordinates the sub-agents and produces final researcher-facing reports
- **Memory Agent**: Retains project context across multi-turn conversations

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Single-file HTML/CSS/JavaScript (vanilla, no frameworks) |
| AI Model | Google Gemini 2.5 Flash (multimodal video analysis) |
| Video Input | YouTube URL via Gemini fileData API |
| Hosting | GitHub Pages (auto-deploys from main) |
| Data Storage | Browser localStorage (analysis history) |
| Agent Framework | Python + LangChain + LangGraph |
| External Search | Tavily API (for agent web search) |
| Model Fallback | Automatic: gemini-2.5-flash → 2.5-flash-lite → 2.0-flash |

### Key Features

1. **Multimodal video analysis** — Gemini actually watches the video frames, not just reading a URL as text
2. **DPICS-IV classification** — Caregiver communication classified into 10 research-validated categories
3. **Cognitive development insights** — Explains what observed behaviors mean for brain development
4. **Caregiver impact analysis** — How the parent's communication style affects the child's growth
5. **Actionable tips** — Specific suggestions based on what was observed, not generic advice
6. **Analysis history** — Past analyses saved in browser localStorage for tracking over time
7. **Embedded YouTube preview** — Video loads in the dashboard when URL is pasted
8. **Honest assessments** — If a child is distressed or caregiver is disengaged, the AI says so
9. **Automatic model fallback** — Cycles through multiple Gemini models if one is overloaded
10. **Zero setup** — No account, no install. Open the website, paste an API key, go.

### File Structure

```
caregiver-video-coding-agent/
├── README.md                               # This report
├── assignment5.py                          # Multi-agent LangChain pipeline (8 sections)
├── index.html                              # DevWatch web app (single-file)
├── report.md                               # Technical project report
├── images/                                 # Team headshots
│   ├── connor.jpg
│   ├── zoe.jpg
│   ├── julia.jpg
│   └── trey.jpg
└── caregiver-video-coding-agent/           # Skill folder
    ├── SKILL.md                            # Skill definition and instructions
    ├── references/
    │   └── sample-input-output.md          # Sample use case with expected output
    ├── templates/
    │   ├── coding-output-template.json     # Reusable JSON output template
    │   └── report-template.md              # Mini-report template
    └── scripts/
        └── rubric_notes.py                 # Starter behavioral rubric
```

---

## Setup & Running

### Web App (index.html)

1. Visit the live site: **https://ckolarov.github.io/caregiver-video-coding-agent/**
2. Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. Paste the key in the yellow banner bar at the top
4. Paste a YouTube URL of a caregiver-child interaction
5. Click **Analyze Video**

### Code Demo (assignment5.py)

```bash
# Install dependencies
pip install langchain langchain-core langchain-google-genai langgraph tavily-python

# Set environment variables
export GEMINI_API_KEY="your-gemini-api-key"
export TAVILY_API_KEY="your-tavily-api-key"

# Run
python assignment5.py
```

The script runs all 8 sections sequentially with graceful fallbacks if API quotas are exceeded.

---

## What's Next

- **Direct video upload** — Support uploading video files directly, not just YouTube URLs, using the Gemini File API
- **Speech-to-text layer** — Add OpenAI Whisper for more accurate transcription and verbal interaction analysis, reducing reliance on Gemini's audio interpretation
- **Longitudinal tracking** — Compare analyses across weeks and months to visualize developmental progress over time
- **Human coder validation** — Compare AI outputs against trained DPICS-IV human coders to measure real-world accuracy on our specific use case
- **Fine-tuned video model** — Explore Qwen2.5-VL for specialized behavioral scoring, as demonstrated in the 2026 ScienceDirect feasibility study
- **Multi-language support** — Extend analysis to non-English caregiver-child interactions
- **Exportable reports** — Generate PDF summaries that parents can share with pediatricians

---

## Responsible AI Considerations

DevWatch is designed with several safety guardrails:

- **Not a diagnostic tool.** The system explicitly states it provides observations, not diagnoses. Every analysis includes a reminder to consult a pediatrician for developmental concerns.
- **Observable behavior only.** The AI is instructed to describe only what it can see and hear. It does not infer mental states, make medical claims, or speculate about conditions.
- **Honest over positive.** Unlike many consumer AI tools that default to encouraging output, DevWatch is designed to be truthful. If a child appears distressed or a caregiver is disengaged, the system reports what it observes rather than hallucinating positive results.
- **Scaffolding flagged as uncertain.** Scaffolding (intentional teaching behavior) requires inferring caregiver intent, which AI cannot reliably do. The system flags this category as high-uncertainty by default.
- **No data collection.** API keys and analysis results are stored only in the user's browser (localStorage). Nothing is sent to our servers — because we don't have any. The only external call is directly from the browser to the Gemini API.
- **Safety filtering.** Gemini's built-in content safety filters remain active. Videos flagged by Google's safety systems will not be analyzed.
- **Privacy by design.** No user accounts, no tracking, no analytics. The tool is a static HTML file hosted on GitHub Pages.

---

## Limitations

| Limitation | Details |
|------------|---------|
| **Not a diagnostic tool** | Provides observations only. Professional evaluation always recommended for concerns. |
| **Video quality dependent** | Low resolution, poor lighting, or heavy background noise reduces accuracy. |
| **Voiceover videos unreliable** | Videos with narrator voiceover (not natural parent-child dialogue) confuse the verbal interaction analysis. |
| **YouTube only** | Currently only supports YouTube links. No direct file upload. |
| **API rate limits** | Free Gemini tier has usage limits. During high demand, analysis may temporarily fail (automatic retry is built in). |
| **No ground truth validation** | We have not compared DevWatch outputs against trained DPICS-IV human coders on our specific use case. Published research shows 72-80% accuracy on text classification and 38-61% on video behavioral scoring. |
| **Scaffolding is hard for AI** | Inferring caregiver intent from video is the most unreliable category across all published research. |
| **Single interaction snapshot** | One video does not represent a child's full developmental profile. Longitudinal observation is always better. |
| **Prompt engineering, not fine-tuning** | We embedded research frameworks into the prompt rather than fine-tuning a model. This is effective but less robust than a purpose-trained model. |

---

## References

1. Zamfirescu-Pereira, J.D., et al. (2024). "Artificial intelligence-powered 3D analysis of video-based caregiver-child interactions." *Science Advances*, 10. [doi:10.1126/sciadv.adp4422](https://www.science.org/doi/10.1126/sciadv.adp4422)

2. Barnett, M.L., et al. (2023). "Assessment of Parent-Child Interaction Quality from Dyadic Dialogue." *Applied Sciences*. Florida International University. NSF-funded. [SpecialTime Dataset — Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/C5Z3SC)

3. AI-powered play assessment approach using video language models: A feasibility study. (2026). *Computers & Education: Artificial Intelligence*. [doi:10.1016/j.caeai.2025.100935](https://doi.org/10.1016/j.caeai.2025.100935)

4. Eyberg, S.M., & Funderburk, B.W. (2011). *Parent-Child Interaction Therapy Protocol.* PCIT International.

5. Google Gemini API — Video Understanding Documentation. [ai.google.dev/gemini-api/docs/video-understanding](https://ai.google.dev/gemini-api/docs/video-understanding)

6. LangChain + LangGraph Documentation. [python.langchain.com](https://python.langchain.com/) | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)

---

## Demo Video

Default demo video used during development and testing:
https://www.youtube.com/watch?v=_YR1WeOBc0E

---

## License

This project was created for academic purposes as part of the William & Mary MSBA AI Class, Spring 2026.
