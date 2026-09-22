# Langchain-Multi-Agent-Research


# 🔍 Multi-Agent Research System (LangChain & Gemini)

An automated research and report-generation pipeline built with a **Multi-Agent architecture** and a critique-refinement loop (*Writer – Critic – Refiner*). The system natively handles cross-lingual queries and is fully optimized for both Vietnamese and English inputs/outputs.

---

## 🚀 Key Features

- **Coordinated Multi-Agent Architecture:**
  - **Search Agent:** Discovers recent, relevant articles and URLs across the web via the Tavily API.
  - **Reader Agent:** Deeply extracts primary content from target URLs using multi-tier fallback strategies (Trafilatura, Readability-lxml, BeautifulSoup4).
  - **Writer Chain:** Synthesizes raw research into a structured draft covering Introduction, Key Findings, Conclusions, and Source Citations.
  - **Critic Chain:** Performs rigorous evaluation on a 10-point scale, highlighting strengths and concrete areas for improvement.
  - **Rewrite Chain:** Iteratively polishes and refines the draft based on critical feedback into a definitive final version.
- **Multilingual Support:** Preserves language consistency with the user prompt, ensuring proper formatting and Vietnamese tone.
- **Interactive Web Interface:** Streamlit UI displaying end-to-end execution, expandable step-by-step traces, and segmented report tabs.
- **Production & CI/CD Ready:** Pre-configured for seamless automated deployment to Render.

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **LLM:** Google Gemini (`gemini-1.5-flash` via Google AI Studio)
- **Frameworks:** LangChain, LangChain-Core, LangGraph
- **Search & Web Extraction:** Tavily API, Trafilatura, Readability-lxml, BeautifulSoup4
- **Interface:** Streamlit

---

## 📁 Repository Structure

```text
Langchain-Multi-Agent-Research/
│
├── src/
│   ├── agents/
│   │   └── agents.py          # Search & Reader agents, Writer, Critic, and Rewrite chains
│   ├── pipelines/
│   │   └── pipelines.py       # Orchestration pipeline executing the 5-step workflow
│   └── tools/
│       └── tools.py           # Web search (Tavily) and URL scraping tools
│
├── app.py                     # Streamlit web application
├── main.py                    # CLI execution script
├── requirements.txt           # Project dependencies
├── render.yaml                # Render automated deployment config
├── .env.example               # Template for environment variables
└── README.md                  # Project documentation
