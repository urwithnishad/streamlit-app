import streamlit as st
import pandas as pd
import plotly.express as px

# LOAD DATA =============================================================================
df = pd.read_csv('data/HistoricalKPIs.csv', parse_dates=['curMonth'])

# PREP DATA
## correct years with only two digits -> 4 digits
df.loc[df.curMonth.str.len()<8, 'curMonth'] = df.loc[df.curMonth.str.len()<8, 'curMonth'].str.replace('-','-20')
## convert months to datetime
df.curMonth = pd.to_datetime(df.curMonth, format="%b-%Y")
## sort by date to make line charts connect properly
df.sort_values(['curMonth'], inplace=True)
## fill null ibids
df.parentibid.fillna('', inplace = True)

parentibids = list(df.parentibid.unique())
kpis = list(df.kpi.unique())

#Dashboard App ==========================================================================
id_select = [st.selectbox("Select parentibid", parentibids)]
kpi_select = st.multiselect("Select KPIs to plot", kpis)

if not id_select:
    st.error("Please select at least one parentibid")
else:
    data = df[df.parentibid.isin(id_select)][['parent','parentibid','curMonth','kpi','amount']]
    parent_name = str(data.parent.unique())
    fig = px.line(data[data.kpi.isin(kpi_select)], 
        x="curMonth", y="amount", color='kpi', title=parent_name)
    st.plotly_chart(fig, use_container_width=True)
    
# table limited to selected month
month_select = st.selectbox("Select month to visualize", list(df.curMonth.unique()))
table_df = df[df.curMonth==month_select]
table_kpi_select = st.selectbox("Select KPI to visualize in table below", list(table_df.kpi.unique()))    
st.dataframe(table_df[table_df.kpi==table_kpi_select])