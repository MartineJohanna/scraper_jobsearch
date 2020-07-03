import dash
import dash_core_components as dcc 
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go



app = dash.Dash()



np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

app.layout = html.Div([
    dcc.Graph(
        id='barplot1',
        figure={
            'data': [
                go.Scatter(
                    x = random_x,
                    y = random_y,
                    mode = 'markers',
                    marker = {
                        'size': 12,
                        'color': 'rgb(51,204,153)',
                        'symbol': 'pentagon',
                        'line': {'width': 2}
                        }
                )
            ],
            'layout': go.Layout(
                title = 'Random Data Scatterplot',
                xaxis = {'title': 'Some random x-values'},
                yaxis = {'title': 'Some random y-values'},
                hovermode='closest')}
    ),
    dcc.Graph(id='scatterplot',
                            figure={'data':[
                                go.Scatter(
                                    x=random_x,
                                    y=random_y,
                                    mode='markers',
                                    marker={
                                        'size':12,
                                        'color':'rgb(51,204,153)',
                                        'symbol': 'pentagon',
                                        'line':{'width':2}
                                    }
                                )],
                                'layout':go.Layout(title='my scatterplot',
                                                    xaxis={'title': 'some x title'})}
                                 )])

if __name__ == '__main__':
    app.run_server()




# app = dash.Dash()

# colors = {'background': '#111111', 'text': '#7FDBFF'}


# app.layout = html.Div(children=[
#             html.H1('hello dash', style={'TextAlign': 'center',
#                                          'color':colors['text']}),

#             dcc.Graph(id='example',
#                     figure={'data':[
#                         {'x':[1,2,3], 'y':[4,1,2], 'type':'bar', 'name':'SF'},
#                         {'x':[1,2,3], 'y':[2,4,5], 'type':'bar', 'name':'NYC'}
#                     ],
#                             'layout':{
#                             'plot_bgcolor': colors['background'],
#                             'paper_bgcolor': colors['background'],
#                             'font': {'colors': colors['text']},
#                             'title':'barplots'}})
# ], style={'backgroundcolor': colors['background']}
# )



# if __name__ == '__main__':
#     app.run_server()