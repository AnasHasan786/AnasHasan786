<div align="center">

<h1>Anas Hasan</h1>

<p><b>Python Developer &nbsp;·&nbsp; Agentic AI Engineer</b></p>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&duration=3000&pause=800&color=00BFFF&center=true&vCenter=true&width=700&lines=Designing+Autonomous+AI+Systems;LangGraph+%C2%B7+CrewAI+%C2%B7+Advanced+RAG+%C2%B7+FAISS;Multi-Agent+Orchestration+%C2%B7+Self-Correcting+Workflows)](https://git.io/typing-svg)

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230A66C2.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anas-hasan-a5546524b/)
[![LeetCode](https://img.shields.io/badge/LeetCode-%23FFA116.svg?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/AnasHasan786/)
[![Gmail](https://img.shields.io/badge/Gmail-%23D14836.svg?style=for-the-badge&logo=gmail&logoColor=white)](mailto:anas.hassan9417@gmail.com)
[![Medium](https://img.shields.io/badge/Medium-%2312100E.svg?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@anas.hassan9417)

</div>


## About Me

I'm a **Python Developer specializing in Agentic AI**, freshly graduated with a B.E. in **Computer Science & AI/ML (2025)**. My focus is on building systems where LLMs don't just respond — they *reason, evaluate, and self-correct*.

I work at the intersection of software engineering and Generative AI: designing stateful multi-agent networks, graph-based execution workflows, and hallucination-resilient RAG pipelines that hold up in production.

> *"Not just prompting models — engineering the scaffolding that makes them trustworthy."*


## Technical Stack

**Agentic AI & Generative Systems**

![LangGraph](https://img.shields.io/badge/LangGraph-000000?style=flat-square&logo=langchain&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-FF4B4B?style=flat-square&logo=gitbook&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=flat-square&logo=langchain&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-6A0DAD?style=flat-square&logo=stackshare&logoColor=white)
![Advanced RAG](https://img.shields.io/badge/Advanced_RAG-4B0082?style=flat-square&logo=googlescholar&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-0052CC?style=flat-square&logo=meta&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI%20%2F%20Anthropic-00A1E4?style=flat-square&logo=openai&logoColor=white)

**Backend & Infrastructure**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-00A896?style=flat-square&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![N8N](https://img.shields.io/badge/N8N_Automation-FF6F00?style=flat-square&logo=n8n&logoColor=white)


## Featured Projects

### 🔮 deepscholar-ai — Autonomous Multi-Agent Research Pipeline

> Stateful, graph-driven scientific paper exploration with cross-document validation — built strictly against hallucination.

```
PDF Corpus ──▶ FAISS Vector Store ──▶ LangGraph Execution Graph
                                              │
                                    ┌─────────▼─────────┐
                                    │   Research Agent  │
                                    └─────────┬─────────┘
                                              │
                                    ┌─────────▼─────────┐
                                    │   Critic Agent    │──── REJECT ──┐
                                    └─────────┬─────────┘              │
                                         ACCEPT                        │
                                    ┌─────────▼─────────┐              │
                                    │  Improver Agent   │◀─────────────┘
                                    └─────────┬─────────┘
                                              │
                                       Verified Output
```

**Key architecture:** LangGraph multi-agent cycle with Research → Critic → Improver nodes. Critic node rejects and re-routes suboptimal outputs automatically. Local FAISS vector context for high-precision document grounding.

![LangGraph](https://img.shields.io/badge/LangGraph-Core-00BFFF?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-RAG-green?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square)
&nbsp;&nbsp;**[→ View Repository](https://github.com/AnasHasan786/deepscholar-ai)**


### 🤖 traceagent — Production Multi-Agent Orchestration Engine

> Enterprise-grade orchestration framework for deterministic workflow tracking and linear execution safety across autonomous task workers.

```
Raw Stack Trace / Telemetry Data
                      │
                      ▼
        ┌───────────────────────────┐
        │     FastAPI Ingest API    │  <-- /api/v1/incidents (POST)
        └─────────────┬─────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │      AWS SQS Queue        │  <-- Asynchronous Buffer
        └─────────────┬─────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │   Incident Worker Loop    │  <-- background/workers/
        └─────────────┬─────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │     Analyzer Service      │  <-- app/services/analyzer.py
        │   (Root Cause & Action)   │
        └─────────────┬─────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │    MongoDB Compass        │  <-- ErrorLog / Workspace Documents
        └───────────────────────────┘
```

**Key architecture:** Specialized agent backstories for high-efficiency task assignment. Full transparency — every LLM token, decision branch, and intermediate state shift is logged. Optimized Python execution engine with robust connection pooling.

![CrewAI](https://img.shields.io/badge/CrewAI-Framework-FF4B4B?style=flat-square)
![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-API-00A896?style=flat-square)
&nbsp;&nbsp;**[→ View Repository](https://github.com/AnasHasan786/traceagent)**


## Engineering Philosophy

```python
class AnasHasan:

    degree      = "B.E. CSE — Artificial Intelligence & Machine Learning (2025)"
    expertise   = ["Agentic AI Architecture", "Multi-Agent Orchestration",
                   "Advanced RAG Pipelines", "Self-Correcting LLM Workflows"]

    def build(self, problem):
        # Understand the failure modes before the happy path
        identify_hallucination_risks(problem)
        design_feedback_loops(problem)
        enforce_determinism_where_it_matters(problem)
        return ship_to_production(problem)
```


## GitHub Stats

<div align="center">

[![GitHub Streak](https://streak-stats.demolab.com?user=AnasHasan786&theme=tokyonight&hide_border=true)](https://git.io/streak-stats)

</div>


## Currently

- 🔬 &nbsp; Building and exploring self-correcting agent architectures and LLM evaluation frameworks
- 🛠️ &nbsp; Deepening expertise in production-grade Agentic AI systems
- 🤝 &nbsp; Open to engineering collaborations, AI systems design discussions, and full-time opportunities


<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=14&duration=4000&pause=1000&color=00BFFF&center=true&vCenter=true&width=550&lines=Let%27s+build+deterministic+intelligence+together.;Not+just+AI+%E2%80%94+AI+that+earns+trust.)](https://git.io/typing-svg)

</div>
