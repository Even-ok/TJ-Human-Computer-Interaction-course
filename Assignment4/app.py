from distutils.log import debug
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from getData import *

app=dash.Dash()

colors = {
    'text': '#7FDBFF'
}

mean_salary_type = ['10th Percentile ',
          '25th Percentile', '75th Percentile',
          '90th Percentile']

############################################################# Graph 1 #########################################################

def major_related_mid_career_salary():
    return html.Div([
        html.Div([
            html.Label('Choose one major',style={"font-weight": "bold","color":"#FFFFFF"}),
            dcc.Dropdown(
                id='major',
                options=[{'label': i, 'value': i} for i in get_undergraduate_major()],
                value='Accounting'
            )
        ],
        style={'width': '100%', 'display': 'inline-block'}),
        html.P([]),
    dcc.Graph(
    id='major_compare_salary',
    )
],className='tiaoxing')

@app.callback(
    dash.dependencies.Output('major_compare_salary', 'figure'),
    [dash.dependencies.Input('major', 'value')])
def update_major_related_mid_career_salary(major):
    major_salary_value = get_media_salary_by_certain_major(major)

    # go.Scatter can create a scatter chart or a line chart object, we will name it trace1
    trace1 = go.Scatter(
        x = mean_salary_type,  
        y = major_salary_value,    
        mode = "lines",     
        name = "citations",  
        marker=dict(size=8,
            color='darkblue',   
            line=dict(
            width=2,
            color="rgb(152,152,152)",)
        ))

    data = [trace1]

    # 添加图层layout
    layout = dict(title = 'Relation between major and mid-career salary',
                # title
                xaxis= dict(title= 'Percentage',ticklen= 5,zeroline= False)
                # Set the x-axis name, the length of the x-axis tick marks, and do not display the zero line
                ) 
    return {
        'data': data,
        'layout': layout
    }

############################################################# Graph 2 #########################################################
def school_type_and_region():
    return html.Div([
        html.Label('Choose distribution type',style={"font-weight": "bold","color":"#FFFFFF"}),
        dcc.RadioItems(id="choose_type_or_region",options = ['Type', 'Region'], value='Type',style={"color":"#FFFFFF","margin":"5px"}),

        html.P([]),
        dcc.Graph(
            id='school_type_or_region',
        )
    ], className='bintuk')

@app.callback(
    dash.dependencies.Output('school_type_or_region', 'figure'),
    [dash.dependencies.Input('choose_type_or_region', 'value')])
def get_type_or_region_number_pie(value):
    counting = get_type_or_region_number(value)
    trace1 = go.Pie(labels=counting.index, values=counting.values)
    
    data = [trace1]

    layout = dict(title = 'School distribution',
                xaxis= dict(title= 'Percentage',ticklen= 5,zeroline= False)
                ) 
    return {
        'data': data,
        'layout': layout
    }

############################################################# Graph 3 #########################################################

def from_starting_to_mid_Career_salary():
    return html.Div([
        html.Label('Choose mid-Career salary type',style={"font-weight": "bold","color":"#FFFFFF"}),
        dcc.RadioItems(id="choose_starting_or_mid",options=['Starting Median Salary', "Mid-Career Median Salary"], value='Starting Median Salary',style={"color":"#FFFFFF","margin":"5px"}),

        html.P([]),
        dcc.Graph(
            id='starting_mid',
        )
    ],className='sandiantu')

@app.callback(
    dash.dependencies.Output('starting_mid', 'figure'),
    [dash.dependencies.Input('choose_starting_or_mid', 'value')])
def starting_mid_scatter(value):
    if value == "Starting Median Salary":
        y_line = df_degree_payback["Starting Median Salary"]
    else:
        y_line = df_degree_payback["Mid-Career Median Salary"]

    trace1 =go.Scatter(
    x = df_degree_payback["Percent change from Starting to Mid-Career Salary"],
    y = y_line,
    mode = 'markers',# scatter
    name ='markers',
    marker = dict(
        size =7,
        color = 'orange'
        ),
    opacity=0.5,
    text=df_degree_payback["Undergraduate Major"]
    )
    
    data = [trace1]

    layout = dict(title = 'Relation between changing percent and Median Salary',
                xaxis= dict(title= 'Percentage',ticklen= 5,zeroline= False)
                ) 
    return {
        'data': data,
        'layout': layout
    }


############################################################# Graph 4 #########################################################

def major_related_starting_salary_bar():
    return html.Div([
        html.Label('Choose majors',style={"font-weight": "bold","color":"#FFFFFF"}),
        dcc.Dropdown(
                id='multi_major',
                options=[{'label': i, 'value': i} for i in get_undergraduate_major()],
                value=['Accounting', 'Education','Economics'],
                multi=True
            ),
        html.P([]),
        dcc.Graph(
            id='starting_salary_bar'
        )
    ],className='zhexiantu')
@app.callback(
    dash.dependencies.Output('starting_salary_bar', 'figure'),
    [dash.dependencies.Input('multi_major', 'value')])
def update_major_related_mid_career_salary(multi_major):
    print(multi_major)
    major_starting_salary_value = get_starting_salary_by_certain_major(multi_major)
    trace1 = go.Bar(
                x=major_starting_salary_value["Starting Median Salary"],
                y=multi_major,
                marker=dict(color='rgba(171, 50, 96, 0.6)',line=dict(color='rgba(171, 50, 96, 1.0)',width=1)),
                name='research',
                orientation='h',    # Bar direction（horizontal）
)
    data = [trace1]

    layout = dict(title = 'Comparison of starting median salary among majors',
                xaxis= dict(title= 'Salary',ticklen= 5,zeroline= False)
                ) 
    return {
        'data': data,
        'layout': layout
    }


############################################################# Graph 5 #########################################################

def salary_and_region_box():
    return html.Div([
        html.Label('Choose salary type',style={"font-weight": "bold","color":"#FFFFFF"}),
        dcc.Checklist(
            id="check_box",
            options=['Starting Median Salary', "Mid-Career Median Salary"],
            value=['Starting Median Salary', "Mid-Career Median Salary"],
            style={"font-weight": "bold","color":"#FFFFFF"}
        ),
        html.P([]),
        dcc.Graph(
            id='region_salary',
        )
    ],className='bintu')

@app.callback(
    dash.dependencies.Output('region_salary', 'figure'),
    [dash.dependencies.Input('check_box', 'value')])
def update_region_salary(multi_salary_type):
    region = ["Northeastern","Southern","Midwestern","Western","California"]
    data = []
    if "Starting Median Salary" in multi_salary_type:
        for reg in region:
            trace0 = go.Box(
                y=get_regions_salary(reg)["Starting Median Salary"],
                name = reg,
                marker = dict(
                    color = 'rgb(12, 12, 140)',
                )
            )
            data.append(trace0)

    if "Mid-Career Median Salary" in multi_salary_type:
        for reg in region:
            trace1 = go.Box(
                y=get_regions_salary(reg)["Mid-Career Median Salary"],
                name = reg,
                marker = dict(
                    color = 'orange',
                )
            )
            data.append(trace1)

    layout = dict(title = 'Relation between salary and region',
                xaxis= dict(title= 'Salary',ticklen= 5,zeroline= False)
                ) 
    return {
        'data': data,
        'layout': layout
    }

def row1():
    return html.Div([
        major_related_mid_career_salary(),
        school_type_and_region(),
        from_starting_to_mid_Career_salary()
    ], className='row')
def row2():
    return html.Div([
            major_related_starting_salary_bar(),
            salary_and_region_box()
    ],className='row')
def row3():
    return html.Div([
        row1(),
        row2()
    ],className='di')
app.layout=html.Div([
    html.H1(["Data Visualization"],style={'margin':'2% auto','color':'white'}),
    row3(),
],className='card')



if __name__ =='__main__':
    dataInit()
    app.run_server(port=4050,debug=True)