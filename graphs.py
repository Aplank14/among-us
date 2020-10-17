import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import pandas as pd

from frequency import ProcessText
from collections import Counter

class GraphDisplay():

    def __init__(self):
        self.speakers = {}
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.callback(
            dash.dependencies.Output('dd-output-container', 'figure'),
            [dash.dependencies.Input('demo-dropdown', 'value')])(self.update_output)

    def update_output(self, value):
        if(value==''):
            value = list(self.speakers.keys())[0] 
        fig = px.bar(self.speakers[value], x="Word", y="Count")
        return fig

    def graphs(self, main_df, table_df):

        dropdownOpts = []
        for speaker, frame in self.speakers.items():
            dropdownOpts.append({'label': speaker, 'value':speaker})

        fig = px.bar(main_df, x="Word", y="Count",color="Name")
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        
        fig.update_xaxes(
                tickangle = 90,
                title_text = "Words",
                title_font = {"size": 20},
                title_standoff = 25,
                constrain = "domain",
                )

        fig.update_yaxes(
                title_text = "Count",
                title_font = {"size": 20},
                title_standoff = 25)

        table = ff.create_table(table_df)

        self.app.layout = html.Div(children=[
            html.H1(children='Andy is dumb'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='example-graph',
                figure=fig
            ),

            dcc.Graph(id="table", figure=table),

            dcc.Dropdown(
                id='demo-dropdown',
                options=dropdownOpts,
                value=''
            ),
            dcc.Graph(id='dd-output-container')


        ])

        self.app.run_server(debug=True)

    def create_graphs(self, p1):
        main_df = pd.DataFrame(columns=['Word', 'Count', 'Name'])
        for speaker, data in p1.speakers.items():
            df = pd.DataFrame(data.most_common(10), columns =['Word', 'Count'])
            df['Name'] = speaker
            self.speakers[speaker] = df
            main_df = main_df.append(df)

        df = pd.DataFrame(list(p1.totalWords.items()), columns =['Speaker', 'Count'])
        print(df)

        self.graphs(main_df, df)

if __name__ == '__main__': 
    p1 = ProcessText()
    p1.analyze_text() 

    p2 = GraphDisplay()
    p2.create_graphs(p1)
