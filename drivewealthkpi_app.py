from xml.sax.xmlreader import IncrementalParser
import pandas as pd
import plotly.express as px
from dash import dcc, html, Output, Input, Dash

# LOAD DATA
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

##create new id combining parent and parent id
df['id'] = df.parent + df.parentibid

ids = list(df.id.unique())
parentibids = list(df.parentibid.unique())

# Dash app =====================================================
app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id = "parent-dropdown",
        options = parentibids,
        placeholder = 'Select Parent IB ID',
        # multi=True,
        # value = '637266bb-dc09-472f-8751-4b06e09ebece'
    ),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=list(df.kpi.unique()),
        value=["AUM"],
        inline=True
    ),
])

@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"),
    Input('parent-dropdown','value'))
def update_line_chart(metrics, parents):
    parents = [parents] if type(parents) == str else parents
    print(parents, metrics)
    sub_df = df[(df.parentibid.isin(parents)) & (df.kpi.isin(metrics))]
    print(sub_df.shape)
    parent_name = str(sub_df.parent.unique())
    fig = px.line(sub_df, 
        x="curMonth", y="amount", color='kpi', title = parent_name)
    return fig

app.run_server(debug=True)