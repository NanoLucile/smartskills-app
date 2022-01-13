import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State


############  DATAS ################

learn = pd.read_csv('learn.csv')
code = pd.read_csv('code.csv')
salary = pd.read_csv('salary.csv')
age = pd.read_csv('age.csv')


###########  APP ###############

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG],
                    meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                  ],suppress_callback_exceptions=True)



app.layout = html.Div(
     [
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


############" HOME PAGE LAYOUT################

index_page = html.Div(
    
    dbc.Row([
        
        dbc.Col([
            
            html.Div([   
                html.Img(src="https://static.wixstatic.com/media/c36c76_4d26ae83942b46c79e0e3919b818760e~mv2.png/v1/fill/w_1000,h_685,al_c,usm_0.66_1.00_0.01/c36c76_4d26ae83942b46c79e0e3919b818760e~mv2.png", className="logo"),
            ])
                           
        ], lg=3, md=12, sm=12 ),      
                
               
        dbc.Col([
            html.Div([
                    html.Br(),
                    html.H1("Projet SMART SKILLS", className="main-title"),
                    ], className="title-div"),

            dbc.Row([
                        html.Div([  html.Br(),
                                    html.P(),
                                    dcc.Link(
                                        dbc.Button('General Overview',
                                        id='general', 
                                        color = 'Blue',
                                        style = {'margin':"5px",'border':'2px solid #C8D4E3', 'border-radius': '12px',
                                        'background' : '#f2f5fa', 'color' : 'black', 'font-size': '24px',
                                        'width': '250px'}
                                                            ),
                                                            href='/page-1'),

                                    dcc.Link(
                                        dbc.Button('Employee training',
                                        id='insight', 
                                        color = 'Blue',
                                        style = {'margin':"5px",'border':'2px solid #C8D4E3', 'border-radius': '12px',
                                        'background' : '#f2f5fa', 'color' : 'black', 'font-size': '24px',
                                        'width': '250px'}
                                                            ),
                                                            href='/page-2')
                                    
                                ], className='d-grid gap-2 d-flex justify-content-center'),
                        ]),

            ], lg=8, md=12, sm=12)    
            
        ])
      
)


##############" PAGE OVERVIEW LAYOUT ##################

page_1_layout = html.Div([
                            html.Div(
                                    
                                dbc.Col([
                                    html.H1('General Overview'),
                                    html.Br(),

                                    dbc.Row([

                                        dcc.Dropdown(
                                                                options=[{'label': c, 'value': c}
                                                                for c in list(salary.DevType.unique())],
                                                                value= 'Data Analyst',
                                                                id='dropdown-component',
                                                                style = {'width' : '350px'}

                                                                ),
                                    ], className='d-grid gap-2 d-flex justify-content-center'),                   

                                    html.Br(),
                                    dbc.Row([
                                        
                                        dbc.Container(
                                                        [
                                                        dcc.RadioItems(
                                                        options=[
                                                            {'label': 'Databases', 'value': 'data_df'},
                                                            {'label': 'Languages', 'value' : 'lang_df'},
                                                            {'label': 'Platforms', 'value' : 'plat_df'},
                                                            {'label': 'Webframes', 'value' : 'web_df'},
                                                            {'label': 'Tools', 'value' : 'tool_df'},
                                                            {'label': 'Others', 'value' : 'other_df'}],

                                                        id="radio-component",
                                                        className="date-group-items",
                                                        labelStyle={'display': 'inline-block'},
                                                        value = 'lang_df'
                                                            ),
                                                        
                                                        html.P(id="output"),
                                                        ],
                                                        className='d-grid gap-2 d-flex justify-content-center',
                                                    ),
                                                                                      

                                        dcc.Graph(id='barplot', className='graph bottom', config={'displayModeBar': False}) ,
                                                    
                                            ], className='d-grid gap-2 d-flex justify-content-center'),

                                    dbc.Row([    
                                        
                                        dbc.Col([
                                            
                                            # emplacement du graph sur ma page
                                            dcc.Graph(id='pieplot',className='top graph', config={'displayModeBar': False}),
                                            dcc.Graph(id='boxplot', config={'displayModeBar': False}, className='middle')
                                            
                                        ], lg=6, md=12, sm=12),

                                        dbc.Col([

                                            dcc.Graph(id='histplot', className='top graph', config={'displayModeBar': False}),
                                            dcc.Graph(id='ageplot', className='middle', config={'displayModeBar': False})
                                        ], lg=6, md=12, sm=12)
                                        
                                        ])


                               ], lg=12, md=12, sm=12)         

                                ),

                        html.Div(id='page-1-content'),
                        html.Br(),
                        dcc.Link('Go to Page 2', href='/page-2'),
                        html.Br(),
                        dcc.Link('Go back to home', href='/'),
])


#################### CALLBACKS #############################################""


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


## pour le pie plot LEARN

@app.callback(
    Output(component_id='pieplot', component_property='figure'),
    Input(component_id='dropdown-component', component_property='value'),
)
# Fonction callback
def update_pieplot(devtype): # -> autant de paramètre(s) que d'input(s)
    
    
    # Création et alimentation du en données du graph
    fig = go.Figure()
    
    colors = px.colors.qualitative.Prism
    learn2 = learn[learn['DevType'] == devtype]
    data = pd.DataFrame(learn2['LearnCode'].value_counts())
    labels = data.index
    values = data['LearnCode']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    fig.update_layout(title_text="How did you learn code ?",title_x=0.5, paper_bgcolor= '#7f8081' ,font_color='white' ,
                    legend=dict(
                    yanchor="bottom",
                    y=-0.4,
                    xanchor="center",
                    x = 0.5)
                    )
            
    fig.update_yaxes(visible=False, fixedrange=False)

    fig.update_traces(hoverinfo='label+percent', textfont_size=12,
                  marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    
    # Renvoi du graph mis à jour dans le layout
    return fig

 ### pour le histplot YEARS   
@app.callback(
    Output(component_id='histplot',component_property='figure'),
    Input(component_id='dropdown-component', component_property='value')
)
def update_histplot(devtype):

    fig = go.Figure()

    data = code[code['DevType'] == devtype]

    fig = px.histogram(data, x="YearsCode",
                   title='Years Code',
                   labels={'YearsCode':'Years since first code'},
                   nbins = 12, 
                   color_discrete_sequence=['rgb(29, 105, 150)'],
                   opacity = 0.9
                   )
   
    fig.update_layout(title_x=0.5,
                    yaxis_title= None,
                    paper_bgcolor='#7f8081',font_color='white',
                    showlegend=False,
                    plot_bgcolor='#7f8081' )

 
    return fig


### pour le box plot salary
@app.callback(
    Output(component_id='boxplot', component_property = 'figure'),
    Input(component_id = 'dropdown-component', component_property='value')
)

def update_boxplot(devtype) :

    df = salary[salary['DevType'] == devtype]

    fig = go.Figure(data=[go.Box(y=df[(df['ConvertedCompYearly']<=100000) & (df['ConvertedCompYearly']>=10000)]['ConvertedCompYearly'], marker_color = 'rgb(95, 70, 144)')])

    #fig = px.box(data[(data['ConvertedCompYearly']<=100000) & (data['ConvertedCompYearly']>=10000)], y='ConvertedCompYearly')

    fig.update_layout(title_text="Salary overview",
                    title_x=0.5,
                    yaxis_title= None,
                    paper_bgcolor='#7f8081',font_color='white',
                    showlegend=False,
                    plot_bgcolor='#7f8081' )
    
    return fig

### pour le ageplot
@app.callback(
    Output(component_id='ageplot', component_property = 'figure'),
    Input(component_id = 'dropdown-component', component_property='value')
)

def update_ageplot(devtype) :

    data = age[age['DevType'] == devtype]

    fig = px.histogram(data, x="Age",
                   color = 'Gender',
                   title='Age and gender',
                   category_orders={"Age": ["Under 18 years old",
                                            "18-24 years old",
                                            "25-34 years old",
                                            "35-44 years old",
                                            "45-54 years old",
                                            "55-64 years old",
                                            "65 years or older"],
                                   "Gender" : ["Man","Woman","Non binary","Prefer not to say"]},
                   color_discrete_sequence=px.colors.qualitative.Prism
                   
                   )
    fig.update_layout(title_x=0.5,
                    yaxis_title= None,
                    xaxis_title = None,
                    paper_bgcolor='#7f8081',font_color='white',
                    plot_bgcolor='#7f8081',
                    legend=dict(
                                yanchor="top",
                                xanchor="right"
                                
                            ))
    
    return fig

### pour le barplot techno
@app.callback(
    Output(component_id='barplot', component_property = 'figure'),
    [ Input(component_id = 'dropdown-component', component_property='value'),
      Input(component_id = 'radio-component', component_property='value')]
)

def update_barplot(devtype, techno) :

    data= pd.read_csv(techno+'.csv')
 
    fig = px.bar(data, y="WorkedWith", x= devtype ,color = "WorkedWith", color_discrete_sequence=px.colors.qualitative.Prism)
    
    fig.update_yaxes(categoryorder='total descending',range=[-0.5,4.5])

    fig.update_layout(title_text="Technologies most used",
                    title_x=0.5,
                    yaxis_title= None,
                    paper_bgcolor= '#7f8081',font_color='white',
                    showlegend=False,
                    plot_bgcolor='#7f8081' )
    
    return fig

app.run_server(debug=True)