# Legal-rights-assitance (ML) — Employee Legal Assistance (Streamlit + Model)

**AI-powered Streamlit backend for Employee Legal Assistance**  
This repository contains the model+backend used to analyze plain-language workplace queries, retrieve relevant laws, produce simple explanations, and generate complaint templates. Designed to run in Google Colab (GPU) or on a small VM. The Streamlit app provides the core UI for the ML pipeline and template downloads.

---

## Demo
Live landing website (front-end): https://legal-rights-assistance.vercel.app/  
(Click **Ask Query** on the landing site to open the Streamlit app.)

**Streamlit app** is hosted separately (Streamlit Cloud) — link in the landing site or in project description.

---

## Features
- Natural language classification of employment issues (salary delay, harassment, termination, benefits, overtime)
- Plain-language explanations with cited snippets
- Action steps, required documents, official portal links
- Draft complaint/email generation and downloadable templates

---

## Tech stack
- Python 3.9+
- Streamlit (UI)
- SentenceTransformers (embeddings) + FAISS (retriever)
- python-docx (template generation)
- Google Colab for GPU runtime (development)

---

## Quick start (Colab / local)

> **Recommended:** Run the model in Google Colab (GPU) and keep Streamlit on Streamlit Cloud for production/demo. If you use Colab for live inference, expose endpoints via ngrok **only for demo**.
```
### empowr-legal-ml/
├─ app.py                 # Streamlit UI (main)
├─ FINAL.ipynb            # Colab notebook (model + optional Flask server)
├─ requirements.txt
├─ action.json
├─ salary_laws.json
├─ termination_laws.json
├─ harassment_laws.json
├─ benefits_laws.json
├─ overtime_laws.json
└─ README.md
```bash
empowr-legal-ml/
├─ app.py                 # Streamlit UI (main)
├─ FINAL.ipynb            # Colab notebook (model + optional Flask server)
├─ requirements.txt
├─ action.json
├─ salary_laws.json
├─ termination_laws.json
├─ harassment_laws.json
├─ benefits_laws.json
├─ overtime_laws.json
└─ README.md
