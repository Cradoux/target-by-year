import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


df = pd.read_csv(
    'data_out.csv')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [html.Div([
        dcc.Graph(id='graph-with-slider',animate=True, style={'height':'75vh'}),
    ],className='row'),
    html.Div([
        dcc.RadioItems(
        id = 'radio',
        options=[
            {'label': 'Max pChEMBL value', 'value': 'best_pchembl'},
            {'label': 'Max LLE', 'value': 'best_lle'}
        ],
        value='best_lle'
    )
    ], className='row eleven columns'),
    html.Div([
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            step=1,
            vertical=False,
            updatemode='drag',
            marks={str(year): str(year) for year in df['year'].unique() if year % 5 == 0}
        ),

        ],className='eleven columns',  style={'padding-bottom':'20px'}),
        # html.Div([
        #     html.Iframe(
        #         # enable all sandbox features
        #         # see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe
        #         # this prevents javascript from running inside the iframe
        #         # and other things security reasons
        #         id='chembl_widget',
        #         src="http://chembl-glados.herokuapp.com/target_report_card/CHEMBL204/embed/approved_drugs_clinical_candidates/",
        #         style={'width': '800px', 'height': '300px'}
        #     )
        # ]),
    ])

@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('radio', 'value')])
def update_figure(selected_year,x_axis_type):
    '''
    Updates plot
    :param selected_year:
    :param x_axis_type:
    :return:
    '''

    traces = []
    for c in df['class'].unique():
        dataset_by_year = df[df['year'] == selected_year]
        dataset_by_year_and_class = dataset_by_year[dataset_by_year['class'] == c]

        traces.append(go.Scatter(
            x=dataset_by_year_and_class[x_axis_type],
            y=dataset_by_year_and_class['cumsum'],
            text=dataset_by_year_and_class['target'],
            #text=[(int(x)+1)*5 for x in dataset_by_year_and_class['drug']],
            mode='markers',
            opacity=0.7,
            marker={
                'size': [(x+1)*5 for x in dataset_by_year_and_class['best_phase_for_ind']]
            },
            name=c
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Maximum achieved to date', 'range':[0,17]},
            yaxis={'title': 'Cumulative Sum of Compounds','type':'log','range':[-1,6]},
            margin={'l': 50, 'b': 0, 't': 10, 'r':0},
            legend={'orientation':"h",'y':-0.17 },
            hovermode='closest',
            showlegend=True,
        )
    }


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://codepen.io/mikesmith1611/pen/QOKgpG.css"]#,
                #"https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(port=1111)
