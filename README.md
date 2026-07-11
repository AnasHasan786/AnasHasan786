<div align="center">

<h1>Hey, I'm Anas Hasan 👋</h1>

<p><b>AI/ML Engineer &nbsp;·&nbsp; Building Agentic Systems with LangGraph &amp; RAG &nbsp;·&nbsp; B.E. CSE (AI/ML) &rsquo;25</b></p>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&duration=3000&pause=800&color=00BFFF&center=true&vCenter=true&width=700&lines=Building+with+LangGraph+%2B+RAG+%2B+FAISS;FastAPI+%C2%B7+AWS+%C2%B7+Multi-Agent+Pipelines;Open+to+AI%2FBackend+Engineer+Roles)](https://git.io/typing-svg)

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230A66C2.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anas-hasan-a5546524b/)
[![LeetCode](https://img.shields.io/badge/LeetCode-%23FFA116.svg?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/AnasHasan786/)
[![Gmail](https://img.shields.io/badge/Gmail-%23D14836.svg?style=for-the-badge&logo=gmail&logoColor=white)](mailto:anas.hassan9417@gmail.com)
[![Medium](https://img.shields.io/badge/Medium-%2312100E.svg?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@anas.hassan9417)

</div>


## About Me

I'm an AI/ML Engineer focused on agentic systems — multi-agent pipelines, RAG, and the infrastructure around them.

I graduated in 2025 and have hands-on industry experience with FastAPI services, Amazon Bedrock, and AWS infrastructure (ECS, ECR, SQS). Since then, I've been building projects end-to-end and contributing to open source to sharpen my ability to write production-grade code, not just prototypes.

What I care about most is the part of AI systems that's easy to skip in a demo — error handling, retries, evaluation, and making sure an agent fails safely instead of confidently making things up.



## Technical Stack

**Agentic AI & LLM Systems**

![LangGraph](https://img.shields.io/badge/LangGraph-000000?style=flat-square&logo=langchain&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=flat-square&logo=langchain&logoColor=white)
![LangSmith](https://img.shields.io/badge/LangSmith-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![RAG Pipelines](https://img.shields.io/badge/RAG_Pipelines-4B0082?style=flat-square&logo=googlescholar&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-0052CC?style=flat-square&logo=meta&logoColor=white)

**Languages & ML Frameworks**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)

**Backend & Infrastructure**

![FastAPI](https://img.shields.io/badge/FastAPI-00A896?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white)


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
                                    ┌─────────▼─────────┐
                                    │  Streamlit UI     │
                                    └───────────────────┘
```

**Key architecture:** LangGraph multi-agent cycle with Research → Critic → Improver nodes. Critic node rejects and re-routes suboptimal outputs automatically. Local FAISS vector store for document grounding, with Groq-hosted Llama models for generation. Streamlit frontend for interactive paper querying and result exploration. Containerized with Docker and deployed on AWS.

![LangGraph](https://img.shields.io/badge/LangGraph-Core-00BFFF?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama-orange?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-RAG-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-Deploy-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square)
&nbsp;&nbsp;**[→ View Repository](https://github.com/AnasHasan786/deepscholar-ai)**


### 🤖 traceagent — AI Debugging & Incident Diagnosis Tool

> Ingests stack traces and telemetry, routes them through an async pipeline, and produces a root-cause analysis with a dashboard to review it.

```
Raw Stack Trace / Telemetry Data
              │
              ▼
┌─────────────────────────────┐
│     FastAPI Ingest API      │  ◀── POST /api/v1/incidents
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       AWS SQS Queue         │  ◀── Async Buffer
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Incident Worker Loop     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   n8n Auth & Orchestration  │  ◀── Workflow Automation
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Analyzer Service       │  ◀── Root Cause + Action Plan
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     MongoDB  ·  Next.js     │  ◀── Incident Dashboard & Logs UI
└─────────────────────────────┘
```

**Key architecture:** FastAPI ingest API buffers incoming incidents through AWS SQS, with n8n handling auth and workflow orchestration between services. Every LLM decision and intermediate state is logged so you can trace how a root-cause conclusion was reached. Next.js dashboard surfaces incident timelines and reports in real time. Deployed on AWS EC2.

![FastAPI](https://img.shields.io/badge/FastAPI-API-00A896?style=flat-square)
![Next.js](https://img.shields.io/badge/Next.js-Dashboard-000000?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Storage-47A248?style=flat-square)
![Python](https://img.shields.io/badge/Python-Backend-3776AB?style=flat-square)
![AWS EC2](https://img.shields.io/badge/AWS_EC2-Deploy-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)
&nbsp;&nbsp;**[→ View Repository](https://github.com/AnasHasan786/traceagent)**


## Engineering Philosophy

```python
class AnasHasan:

    degree      = "B.E. CSE — Artificial Intelligence & Machine Learning (2025)"
    focus_areas = ["Multi-Agent Systems (LangGraph)", "RAG Pipelines",
                    "FastAPI Backends", "AWS Infrastructure"]

    def build(self, problem):
        # Understand the failure modes before the happy path
        identify_edge_cases(problem)
        design_feedback_loops(problem)
        write_tests(problem)
        return ship_it(problem)
```


## GitHub Analytics Dashboard

<div align="center">

<img src="assets/dashboard/kpi_cards.svg" width="100%" alt="GitHub Analytics Overview" />

<br/>

<sub>⚡ Live · Auto Updated Nightly via GitHub Actions</sub>

<br/>

<img src="assets/dashboard/weekly_activity.svg" width="49%" alt="Weekly Activity" />
<img src="assets/dashboard/commit_trend.svg" width="49%" alt="Commit Trend" />

<br/>

<img src="assets/dashboard/language_distribution.svg" width="49%" alt="Language Distribution" />
<img src="assets/dashboard/repo_growth.svg" width="49%" alt="Repository Growth" />

<br/>

<img src="assets/dashboard/contribution_calendar.svg" width="100%" alt="Contribution Calendar" />

<br/>

<sub>Generated locally with Python · No third-party stat cards · Refreshes every night at 00:00 UTC</sub>

</div>



## Currently

- 🔬 &nbsp; Contributing to open source projects and writing more code independently, less AI-assisted
- 🧠 &nbsp; Practicing DSA (NeetCode 150 in C++) for interviews
- 🤝 &nbsp; Open to full-time AI Engineer, Backend Engineer, and Software Engineer roles


<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=14&duration=4000&pause=1000&color=00BFFF&center=true&vCenter=true&width=550&lines=Let%27s+build+deterministic+intelligence+together.;Not+just+AI+%E2%80%94+AI+that+earns+trust.)](https://git.io/typing-svg)

</div>
