# DevWatch — Child Development Video Analysis

> **[Click here to view the live website](https://ckolarov.github.io/caregiver-video-coding-agent/)**

An AI-powered tool that analyzes caregiver-child interaction videos and provides research-grounded developmental insights for parents. Built with Google Gemini's multimodal video analysis, grounded in the DPICS-IV and PC-SCP behavioral coding frameworks.

## What It Does

- Segments long caregiver-child interaction videos into analyzable clips
- Generates first-pass behavioral coding across four rubric categories: motor development, caregiver behavior, safety issues, and scaffolding
- Compares AI-generated codes against human-coded labels to measure agreement
- Provides a browser-based research tool where researchers can paste a YouTube URL and receive structured behavioral coding output powered by the Gemini API

## File Structure

```
caregiver-video-coding-agent/
├── assignment5.py                          # Multi-agent LangChain pipeline (8 sections)
├── index.html                              # Single-file browser research interface
├── report.md                               # Project report
├── README.md                               # This file
└── caregiver-video-coding-agent/           # Skill folder
    ├── SKILL.md                            # Skill definition and instructions
    ├── references/
    │   └── sample-input-output.md          # Sample use case
    ├── templates/
    │   ├── coding-output-template.json     # Reusable output template
    │   └── report-template.md              # Mini-report template
    └── scripts/
        └── rubric_notes.py                 # Starter behavioral rubric
```

## Setup: assignment5.py

### 1. Install dependencies

```bash
pip install langchain langchain-core langchain-google-genai langgraph tavily-python
```

### 2. Set environment variables

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

### 3. Run the script

```bash
python assignment5.py
```

The script runs through all 8 required sections sequentially. If the Gemini free-tier quota is exceeded, each section will gracefully fall back to a printed message.

## Setup: index.html

### 1. Get a Gemini API key

Visit [Google AI Studio](https://aistudio.google.com/apikey) and create an API key.

### 2. Insert your key

Open `index.html` in a text editor and replace `YOUR_API_KEY_HERE` with your actual key:

```javascript
const GEMINI_API_KEY = "your-actual-key-here";
```

### 3. Open in a browser

Simply open `index.html` in any modern web browser. No server required.

## Demo Video

The default demo video used for this project:

https://www.youtube.com/watch?v=_YR1WeOBc0E

## Team

Zoe, Julia, Connor, Trey — William & Mary MSBA AI Class, Spring 2026
