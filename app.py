import glob
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Employee Data')
st.header('Employee Data 2023')
st.subheader('Company Wide Roster')

### --- Load dataframe

excel_file = 'Employee Sample Data.xlsx'
sheet_name = 'Data'

df = pd.read_excel(excel_file,
                 sheet_name= sheet_name,
                 usecols='A:N',
                 header=0)

st.dataframe(df)

st.sidebar.header("Filter:")

department = st.sidebar.multiselect(
    "Select department:",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

businessUnit= st.sidebar.multiselect(
    "Business Unit:",
    options=df["Business_Unit"].unique(),
    default=df["Business_Unit"].unique()
)

country = st.sidebar.multiselect(
    "Country:",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

city = st.sidebar.multiselect(
    "City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

df_selection = df.query(
    "Department == @department & Business_Unit == @businessUnit & Country == @country & City == @city"
)

average_age = int(df_selection["Age"].mean(),)
average_salary = round(df_selection["Annual_Salary"].mean(),2)
total_annual_salary = round(df_selection["Annual_Salary"].sum(),2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Annual Salary:")
    st.subheader(f"US $ {total_annual_salary:,}")
with right_column:
    st.subheader("Average Salary")
    st.subheader(f"US $ {average_salary:,}")

st.markdown("---")

# Salary by department

salary_by_department = (
    df_selection.groupby(by=["Department"]).sum()[["Annual_Salary"]].sort_values(by="Annual_Salary")
)
fig_salary_by_department = px.bar(
    salary_by_department,
    x="Annual_Salary",
    y=salary_by_department.index,
    orientation="h",
    title="<b>Salary by department</b>",
    color_discrete_sequence=["#008388"] * len(salary_by_department),
    template="plotly_white",
)
fig_salary_by_department.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#Salary by country

salary_by_country = df_selection.groupby(by=["Country"]).sum()[["Annual_Salary"]]
fig_salary_by_country = px.bar(
    salary_by_country,
    y="Annual_Salary",
    title="<b>Salary by country</b>",
    color_discrete_sequence=["#008388"] * len(salary_by_country),
    template="plotly_white",
)
fig_salary_by_country.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_salary_by_department, use_container_width=True)
right_column.plotly_chart(fig_salary_by_country, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)