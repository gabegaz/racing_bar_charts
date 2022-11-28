from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.express as px        
import pandas as pd
import numpy as np

app = Dash(__name__)

df = pd.read_csv('../data/bank_loan.csv')

df.head()
df.replace(0, np.nan, inplace=True)

app.layout = html.Div([
        html.H2("A racing bar chart: Ethiopian banks"),

        dcc.Dropdown(id= 'dropdown_var_input',
                options=[{'label': var, 
                                'value': var} for var in ['collection', 'disbursement', 'outstanding']]),
        html.Br(),

        html.Div(
            dcc.Graph(id='racing_bar_chart_output',
                ),
            ),
        html.Br()
    ])

@app.callback(
    Output('racing_bar_chart_output', 'figure'),
    Input('dropdown_var_input', 'value'))
def racing_bar_chart(selected_var):
    range_y=[]

    #determine the range of the y-axis for each of the variables
    if selected_var=='collection':
        range_y = [0, 54]
    if selected_var=='disbursement':
        range_y =  [0, 111]
    if selected_var=='outstanding':
        range_y = [0, 708]

    #construct the image        
    fig_bar = px.bar(df, x="bank", y=selected_var, color="bank",
                animation_frame="year", animation_group="bank",
                    range_y= range_y,
                    color_discrete_sequence=px.colors.qualitative.T10)    
    fig_bar.update_yaxes(showgrid=True),
    fig_bar.update_xaxes(categoryorder='total descending')
    fig_bar.update_traces(hovertemplate=None)
    fig_bar.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    fig_bar.update_layout(margin=dict(t=70, b=0, l=70, r=40),
                            hovermode="x unified",
                            xaxis_tickangle=360,
                            xaxis_title='Banks in Ethiopia', yaxis_title=selected_var,
                            title_font=dict(size=25, color='#a5a7ab', family="Lato, sans-serif"),
                            font=dict(color='#8a8d93'),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                            )
    #returns the constructed figure to the space with the id=racing_bar_chart_output
    return fig_bar

if __name__ == '__main__':
    app.run_server(debug=True)

