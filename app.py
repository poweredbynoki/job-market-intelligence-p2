
import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

st.set_page_config(page_title="Job Market Intelligence", layout="wide")
st.title("Job Market Intelligence — Phase 2")
st.caption("246+ real postings. 5 cities. 8 job title variants. Built by Nuha G.")

df = pd.read_csv("phase2_jobs_raw.csv")
con = duckdb.connect()
con.register("jobs", df)

city = st.selectbox("Filter by city", ["All"] + sorted(df["city"].unique().tolist()))
if city != "All":
    df = df[df["city"] == city]
    con.register("jobs", df)

st.subheader("Postings by job title")
fig1 = px.bar(
    df["search_title"].value_counts().reset_index(),
    x="count", y="search_title", orientation="h",
    labels={"count":"postings","search_title":""}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Salary by city")
sal = con.execute(
    "SELECT city, ROUND(AVG((salary_min+salary_max)/2),0) as avg_salary "
    "FROM jobs WHERE salary_min>20000 AND salary_max>20000 GROUP BY city ORDER BY avg_salary DESC"
).df()
fig2 = px.bar(sal, x="city", y="avg_salary", labels={"avg_salary":"avg mid salary"})
st.plotly_chart(fig2, use_container_width=True)

st.subheader("About this project")
st.markdown(
    "Built to answer: what do companies actually require, and is AI showing up yet? "
    "Non-traditional background: Combat Medic, Ops Coordinator, BBA Information Systems. "
    "Domain expertise in healthcare and operations — two of the fastest-growing data sectors. "
    "Limitations are documented in the notebook."
)
