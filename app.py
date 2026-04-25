import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
from collections import Counter

st.set_page_config(page_title="Job Market Intelligence", layout="wide")

st.title("Job Market Intelligence — Phase 2")
st.caption("2,619 real postings. 4 cities. Skill-based search. Built by Nuha G.")

@st.cache_data
def load_data():
    df = pd.read_csv("phase2_jobs_raw.csv")
    noise_keywords = [
        'teacher','nurse','doctor','physician','urologist','therapist',
        'engineer','software','developer','product manager','account executive',
        'project manager','architect','attorney','lawyer','pharmacist'
    ]
    mask = ~df['title'].str.lower().str.contains('|'.join(noise_keywords), na=False)
    df = df[mask].copy()
    df['title_clean'] = df['title'].str.lower()
    for word in ['senior','sr.','sr ','junior','jr.','jr ','lead ','staff ',
                 'principal ','associate ','i ','ii ','iii ','iv ']:
        df['title_clean'] = df['title_clean'].str.replace(word, '', regex=False)
    df['title_clean'] = df['title_clean'].str.strip()
    df['mid_salary'] = (df['salary_min'] + df['salary_max']) / 2
    return df

df = load_data()

city = st.selectbox("Filter by city", ["All cities"] + sorted(df["city"].dropna().unique().tolist()))
if city != "All cities":
    filtered = df[df["city"] == city]
else:
    filtered = df

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total postings", f"{len(filtered):,}")
col2.metric("Cities covered", filtered['city'].nunique())
col3.metric("Unique titles found", filtered['title_clean'].nunique())
sal = filtered[(filtered['salary_min'] > 20000) & (filtered['salary_max'] > 20000)]
col4.metric("Median salary", f"${sal['mid_salary'].median():,.0f}" if len(sal) > 0 else "N/A")

st.markdown("---")

st.subheader("What companies actually call the role")
st.caption("Searched by skill keywords, not assumed titles. These are the titles that came back.")
title_counts = filtered['title_clean'].value_counts().head(20).reset_index()
title_counts.columns = ['title', 'postings']
title_counts = title_counts.sort_values('postings')
fig1 = px.bar(
    title_counts, x='postings', y='title', orientation='h',
    labels={'postings': '% of postings', 'title': ''},
    color='postings',
    color_continuous_scale='Blues'
)
fig1.update_layout(coloraxis_showscale=False, height=500)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Median salary by city")
st.caption("Same skills, different paychecks depending on where the job is.")
sal_city = (
    filtered[(filtered['salary_min'] > 20000) & (filtered['salary_max'] > 20000)]
    .groupby('city')['mid_salary']
    .median()
    .reset_index()
    .sort_values('mid_salary', ascending=False)
)
sal_city.columns = ['city', 'median_salary']
fig2 = px.bar(
    sal_city, x='city', y='median_salary',
    labels={'median_salary': 'median mid salary ($)', 'city': ''},
    color='median_salary',
    color_continuous_scale='Blues'
)
fig2.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Which skill keyword found the most postings")
st.caption("This is the reverse search in action. Each bar is a skill, not a title.")
kw_counts = filtered['keyword'].value_counts().reset_index()
kw_counts.columns = ['keyword', 'postings']
fig3 = px.bar(
    kw_counts, x='postings', y='keyword', orientation='h',
    labels={'postings': 'postings found', 'keyword': ''},
    color='postings',
    color_continuous_scale='Blues'
)
fig3.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Postings by city")
city_counts = filtered['city'].value_counts().reset_index()
city_counts.columns = ['city', 'postings']
fig4 = px.bar(
    city_counts, x='city', y='postings',
    labels={'postings': 'postings', 'city': ''},
    color='postings',
    color_continuous_scale='Blues'
)
fig4.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("About this project")
st.markdown("""
Most job searches start with a title. This one starts with a skill.

Instead of searching "data analyst" and hoping for the best, this project pulled postings
by the skills inside them. SQL, business intelligence, data insights. Then it looked at
what titles actually came back. Same skills showing up under a dozen different names.
If you are only searching one title, you are missing most of the market.

**Non-traditional background:** Combat Medic (68W), Ops Coordinator at Crisis24 supporting
DoorDash HQ, BBA Information Systems magna cum laude. Domain expertise in healthcare and
operations, two of the fastest-growing sectors for data roles right now.

**Limitations documented in the notebook:**
- Free tier caps descriptions at 500 characters
- Deduplication by job ID only
- City-level salary findings are directional, not statistically robust
""")
