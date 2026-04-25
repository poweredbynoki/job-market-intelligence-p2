# Job Market Intelligence — Phase 2

> Everyone told me to learn SQL. Nobody told me companies stopped posting jobs called "Data Analyst."

---

## What this is

Think about how Shazam works. You don't search for a song by its title because you don't know it yet. You hum the melody and let the app find what matches.

That's exactly what this project does for job searching.

Instead of searching "data analyst" and hoping for the best, this pulls postings by the skills inside them. SQL. Business intelligence. Data insights. Then it looks at what titles actually came back. The data tells you what companies are calling the role. You stop guessing.

Same skills. Twelve different titles. Most of the market invisible to anyone searching just one term.

And then there is the AI side of this. Tools are multiplying faster than any one person can learn them. The answer is not to learn everything. It is to know your domain well enough to pick the right tool and use it without wasting time or money on things you do not need. Every tool in this project showed up in real job postings first. The stack was chosen from the data. That part is intentional.

---

## Live app

**[View on Streamlit](YOUR_STREAMLIT_URL_HERE)**

Filter by city. Compare salaries. See which titles show the most volume. Built from real postings pulled this week.

---

## The findings

- Titles like "Revenue Analyst," "Decision Support Analyst," and "People Analytics Specialist" require the same skills as "Data Analyst" but never show up when you search that term
- AI keywords like LLM, generative AI, and ChatGPT appear in the first 500 characters of job descriptions. Companies are not burying AI at the bottom of requirements. They are leading with it.
- Salary data was present in the majority of postings. Median mid-point is visible by city in the app.
- Data pulled across SF, NYC, Austin, Chicago, and Remote in a single session

---

## On AI tools

AI is growing faster than anyone can keep up with. That is not a reason to panic. It is a reason to be strategic.

The analysts who will do well are not the ones who learned the most tools. They are the ones who understood their domain well enough to know which tools were worth learning and why. SQL does not get replaced because ChatGPT exists. It gets more valuable because now you can move faster with it.

Knowing your domain is what lets you evaluate a tool instead of just following what someone posted on LinkedIn.

---

## How the search works

Most job searches start with a title. This one starts with a skill.

Adzuna's API searches both job title and description at the same time. So searching "sql analytics" or "business intelligence" returns any posting where those skills appear anywhere in the listing. Not just roles called "data analyst."

After pulling the results, the actual job titles that came back were extracted and normalized. Seniority labels stripped out. Variants grouped. What you see in the app is what companies are actually posting, not what a keyword list assumed they would post.

This is reverse search. Start from the skill, find the title. Not the other way around.

---

## Limitations flagged before presenting findings

1. Free tier caps descriptions at 500 characters. Skill match percentages are understated because most requirements appear later in the description and get cut off.
2. Deduplication is by job ID only. The same role posted across multiple boards could appear more than once.
3. "Remote" as a location returns national results. Salary comparisons between Remote and specific cities are directional only, not apples to apples.
4. Sample size per city and keyword combination is small. City-level findings show trends, not statistically significant conclusions.

Flagging this before someone else has to is the whole point.

---

## Stack

| Tool | Why it is here |
|------|----------------|
| Python + Pandas | Data pull, cleaning, title normalization |
| DuckDB | SQL queries directly on the dataframe, no database server needed |
| Plotly | Interactive charts |
| Streamlit | Live app with city filter, shareable in one URL |
| Adzuna API | Real job postings, free tier |
| Google Colab | Development environment |
| GitHub | Version control and Streamlit deployment source |

---

## Files

| File | What it is |
|------|------------|
| `app.py` | Streamlit app, the public-facing interactive layer |
| `phase2_job_intelligence.ipynb` | Full analysis notebook with methodology notes and limitations |
| `phase2_jobs_raw.csv` | Raw deduplicated data pulled from the API |
| `requirements.txt` | Libraries for Streamlit deployment |

---

## How to run it locally

```bash
git clone https://github.com/poweredbynoki/job-market-intelligence-p2
cd job-market-intelligence-p2
pip install -r requirements.txt
streamlit run app.py
```

For the data pull: open the notebook in Google Colab, add `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` to Colab Secrets via the key icon in the sidebar, toggle Notebook Access ON for both, then run all cells top to bottom.

Before uploading the notebook to GitHub: open the `.ipynb` in a text editor, Ctrl+F your actual key values, confirm they are not anywhere in the file. Bots scan new public repos for exposed keys within minutes of upload.

---

## About the builder

Non-traditional path. Combat Medic (68W), Lobby Operations Coordinator at Crisis24 supporting DoorDash HQ, BBA Information Systems magna cum laude.

Domain expertise in healthcare and operations, two of the fastest-growing sectors for data roles in 2026. Built this because I was job searching and did not want to guess which skills to prioritize. Treated it as a research question. Used the findings to decide what to learn next.

Limitations are documented. Findings are real. Stack was chosen from the data.

---

*Phase 1 -> [Job Market Intelligence Phase 1](https://github.com/poweredbynoki/-job-market-intelligence)*
