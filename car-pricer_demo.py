import pandas as pd
import dash
from dash import html
#import dash_html_components as html
from dash import dcc
from dash import dash_table
#import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import re
import string
import numpy as np
import requests
import pymssql
#
hostname = '*******' #server
port = '*******'
database = '*******'
username = '*******'
password = '*******'

listing_columns = ['Year','Make','Model','Odometer','Condition','Color','Cylinders','Transmission','Fuel','Drive'\
       ,'Title','Price']
dict_result = []

df = pd.read_csv('df.csv')
df_info = pd.read_csv('df_info.csv')
clicks = 0
price_old = 0

transmission_vals = {'Automatic': 1, 'Manual': 0}

year_vals = sorted(df.Year.value_counts().index, reverse = True)
dropdown_year = []
for year in year_vals:
    dropdown_year.append({'label': year, 'value': int(year)})
make_vals = df.Make.value_counts().index
dropdown_make = []
for make in make_vals:
    dropdown_make.append({'label': make, 'value': make})
model_vals = df.Model.value_counts().index
dropdown_model = []
for model in model_vals:
    dropdown_model.append({'label': model, 'value': model})
condition_vals = ['New','Like New','Excellent', 'Good', 'Fair', 'Salvage']
dropdown_condition = []
for condition in condition_vals:
    dropdown_condition.append({'label': condition, 'value': condition})
color_vals = df.Color.value_counts().index
dropdown_color = []
for color in color_vals:
    dropdown_color.append({'label': color, 'value': color})
title_vals = df.Title.value_counts().index
dropdown_title = []
for title in title_vals:
    dropdown_title.append({'label': title, 'value': title})
fuel_vals = df.Fuel.unique()
#fuel_vals = df[df.Make == selected_make].Fuel.value_counts().index
dropdown_fuel = []
for fuel in fuel_vals:
    dropdown_fuel.append({'label': fuel, 'value': fuel})

cylinder_index = sorted(df.Cylinders.value_counts().index.tolist())
cylinders_vals = [str(i) for i in cylinder_index]
dropdown_cylinders = []
for cylinders in cylinders_vals:
    if cylinders == '0':
        dropdown_cylinders.append({'label': 'N/A', 'value': 'N/A'})
    else:
        dropdown_cylinders.append({'label': cylinders, 'value': cylinders})

drive_vals = df.Drive.value_counts().index
#drive_vals = df[df.Make == selected_make].Drive.value_counts().index
dropdown_drive = []
for drive in drive_vals:
    dropdown_drive.append({'label': drive, 'value': drive})
dropdown_transmission = []
for transmission in transmission_vals:
    dropdown_transmission.append({'label': transmission, 'value': transmission_vals.get(transmission)})

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
                                html.Div([
                                html.H1('Used Car Price Prediction',
                                        style={'textAlign': 'center', 'color': '#503D36','font-size': 50}), 
                                    html.H1('Please fill all fields before calculating, starting with "Vehicle Type"',
                                        style={'textAlign': 'left','font-size': 23}), 
                                    html.H1('Note: the estimation works best if you enter reasonable values.',
                                        style={'textAlign': 'left','font-size': 20}),
                                html.Br(),
                                html.H1('Vehicle Type',
                                        style={'textAlign': 'left','font-size': 25}), 
                                html.Div([
                                    html.Div([
                                        html.P('Please Select Vehicle Year')
                                        ], style={'display':'inline-block', 'margin-right': '150px'}),  
                                    html.Div([
                                        html.P('Please Select Vehicle Make')
                                        ], style={'display':'inline-block', 'margin-right': '145px'}),
                                    html.Div([
                                        html.P('Please Select Vehicle Model')
                                        ], style={'display':'inline-block'})  
                                        ]),
                                html.Div([
                                    html.Div([
                                        dcc.Dropdown(
                                            id = 'dropdown_year',
                                            options=dropdown_year,
                                            value=2012,
                                            placeholder= 'Select Year')
                                        ], style={'width': '150px','display': 'inline-block', 'margin-right': '170px'}),
                                    html.Div([                             
                                        dcc.Dropdown(
                                            id = 'dropdown_make',
                                            options=dropdown_make,
                                            value='Volkswagen',
                                            placeholder='Select Make')
                                        ], style={'width': '150px','display': 'inline-block', 'margin-right': '170px'}),
                                    html.Div([       
                                            dcc.Dropdown(
                                            id = 'dropdown_model',
                                            options=dropdown_model,
                                            value = 'Passat',
                                            placeholder='Select Model')
                                        ], style={'width': '150px','display': 'inline-block',})
                                        ]),    
                                html.Br(), 
                                html.H1('Vehicle Condition',
                                        style={'textAlign': 'left','font-size': 25}), 
                                html.P('Please Input Vehicle Mileage'),
                                html.Br(), 
                                dcc.Input(
                                    id='input_odometer',
                                    type='number',
                                    placeholder = 'Enter Mileage',
                                    value= 160000,
                                    style={'width': 142, 'height': 32, 'font-size': '15px'}),     
                                html.Br(),     
                                html.Br(), 
                                html.P('Please Select Vehicle Condition'),
                                dcc.Dropdown(
                                    id = 'dropdown_condition',
                                    options=dropdown_condition,
                                    value= 'Good', 
                                    style={'width': '150px'}),                 
                                html.Br(),
                                html.H1('Vehicle Specs',
                                        style={'textAlign': 'left','font-size': 25}), 
                                html.Div([
                                    html.Div([
                                        html.P('Please Select Vehicle Color')
                                        ], style={'display':'inline-block', 'margin-right': '145px'}),  
                                    html.Div([
                                        html.P('Please Select Cylinder Count')
                                        ], style={'display':'inline-block', 'margin-right': '135px'}), 
                                    html.Div([
                                        html.P('Please Select Vehicle Drivetrain')
                                        ], style={'display':'inline-block'})
                                        ]),
                                html.Div([     
                                    html.Div([                          
                                        dcc.Dropdown(
                                            id = 'dropdown_color',
                                            options=dropdown_color,
                                            placeholder= 'Select Color',
                                            value = 'Grey')
                                        ], style={'width': '150px','display': 'inline-block', 'margin-right': '170px'}),
                                    html.Div([       
                                        dcc.Dropdown(
                                            id = 'dropdown_cylinders',
                                            options=dropdown_cylinders,
                                            placeholder= 'Select Cylinders',
                                            value = '4')
                                        ], style={'width': '150px','display': 'inline-block','margin-right': '170px'}), 
                                    html.Div([       
                                        dcc.Dropdown(
                                            id = 'dropdown_drive',
                                            options=dropdown_drive,
                                            placeholder= 'Select Drivetrain',
                                            value = 'Fwd')
                                        ], style={'width': '150px','display': 'inline-block'})
                                        ]),    
                                html.Br(),
                                html.Div([  
                                    html.Div([
                                        html.P('Please Select Vehicle Transmission')
                                        ], style={'display':'inline-block', 'margin-right': '95px'}),
                                    html.Div([
                                        html.P('Please Select Vehicle Fuel Type')
                                        ], style={'display':'inline-block'})  
                                        ]),              
                                html.Div([     
                                    html.Div([       
                                        dcc.Dropdown(
                                            id = 'dropdown_transmission',
                                            options=dropdown_transmission,
                                            placeholder= 'Select Transmission',
                                            value = dropdown_transmission[0]['value'])
                                        ], style={'width': '150px','display': 'inline-block','margin-right': '170px'}),     
                                    html.Div([       
                                        dcc.Dropdown(
                                            id = 'dropdown_fuel',
                                            options=dropdown_fuel,
                                            placeholder= 'Select Fuel Type',
                                            value = 'Gas')
                                        ], style={'width': '150px','display': 'inline-block'})
                                        ]),    
                                html.Br(),
                                html.H1('Title Status',
                                        style={'textAlign': 'left','font-size': 25}), 
                                html.P('Please Select Vehicle Title Status'),                               
                                dcc.Dropdown(
                                    id = 'dropdown_title',
                                    options=dropdown_title,
                                    value= 'Clean',
                                    style={'width': '150px'}),
                                html.Br(),
                                html.H1('Vehicle Description',
                                        style={'textAlign': 'left','font-size': 25}), 
                                html.P('Please add any additional details about the vehicle by typing below.'),
                                html.P('Here are some examples:'),
                                html.P('Very good condition.', style={'font-style': 'italic'}),
                                html.P('The wheels are missing.', style={'font-style': 'italic'}),
                                html.P('The windshield has some cracks in it.', style={'font-style': 'italic'}),
                                dcc.Textarea(
                                    id='my-input',
                                    placeholder='Enter Vehicle Description:',
                                    value='',
                                    style={'width': 700, 'height': 120, 'font-size': '15px'}),#style={'textAlign': 'center','width': '500px','height': '150px','font-size': '25px'}),
                                html.Br(),

                                html.Div(
                                    children=[
                                        html.H1(id='result', style={'color': '#18c429', 'font-size': 44}),
                                        html.Button('Calculate', id='button', n_clicks=0, 
                                            style={'width': '150px','height': '76px','font-size': '25px',\
                                                    'backgroundColor': '#40a9de',"color": "black"}),
                                        html.Br(),
                                        html.H1('Please wait for the result to load', style={'font-size': 20}),
                                    ],
                                    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
                                ),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H1('The algorithm used for making these price predictions include XGBoost for regression as well as BERT for NLP. \
                                        This application uses a machine learning algorithm trained on tens of thousands of used car listings that have been \
                                        obtained through web scraping of classifieds websites.',
                                        style={'font-family': 'Arial', 'margin-left': '0%','margin-right': '57%','font-size': 20, 'color': '#4d423d' }),
                                html.Br(),
                                html.H1('Give it a go and let me know what you think!',
                                        style={'font-family': 'Arial', 'margin-left': '0%','margin-right': '57%','font-size': 20, 'color': '#4d423d' }),
                                html.Br(),
                                html.H1('If you are interested in the code, take a look my GitHub page.',
                                        style={'font-family': 'Arial', 'margin-left': '0%','margin-right': '57%','font-size': 20, 'color': '#4d423d' }),
                                html.Br(),
                                html.Div(
                                    children=[
                                        html.Br(),
                                        html.H1('Vehicle listings with the same Make and Model and Year (± 2) as the one \
                                                you selected (retrieved from the database):',
                                                style={'textAlign': 'left','font-size': 32, 'color': '#4a4141'}),  
                                        dash_table.DataTable(
                                            id='listings',
                                            columns=[{"name": i, "id": i} for i in listing_columns],
                                            data=dict_result,
                                            sort_action='native', 
                                            style_cell={'textAlign': 'left', 'font_size': '23px'},
                                            style_header=dict(backgroundColor="paleturquoise"),
                                            style_data=dict(backgroundColor="lavender")
                                        ),
                                    ],
                                ),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.A(
                                    href="https://github.com/AlexBandurin", 
                                    children=[
                                        html.Img(
                                            src=app.get_asset_url('github_logo.png'),  # assumes the logo is in the 'assets' folder
                                            style={'height':'70px', 'width':'70px','margin-right':'10px'}
                                            )
                                        ],
                                        target="_blank"  # makes the link open in a new tab
                                    ),
                                    html.A(
                                        href="https://www.linkedin.com/in/alexbandurin/",
                                        children=[
                                            html.Img(
                                                src=app.get_asset_url('linkedin_logo.png'),  # assumes the logo is in the 'assets' folder
                                                style={'height':'70px', 'width':'70px','margin-left':'10px'}
                                            )
                                        ],
                                        target="_blank"  # makes the link open in a new tab
                                    )
                                        ],style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'transform': 'translateX(-25px)'}),
                                    ],    
                                    style= {'marginLeft' : '0.25%'})
                                    ])

@app.callback(
            [Output(component_id='dropdown_model', component_property='options'),
            Output(component_id='dropdown_condition', component_property='options'),
            #Output(component_id='dropdown_condition', component_property='value'),
            Output(component_id='dropdown_color', component_property='options'),
            #Output(component_id='dropdown_color', component_property='value'),
            Output(component_id='dropdown_drive', component_property='options'),
            #Output(component_id='dropdown_drive', component_property='value'),
            Output(component_id='dropdown_fuel', component_property='options'),
            #Output(component_id='dropdown_fuel', component_property='value'),
            Output(component_id='dropdown_title', component_property='options'),
            #Output(component_id='dropdown_title', component_property='value'),           
            Output(component_id='dropdown_cylinders', component_property='options'),
            #Output(component_id='dropdown_cylinders', component_property='value'),
            Output(component_id='dropdown_transmission', component_property='options')],
            #Output(component_id='dropdown_transmission', component_property='value')],
            [Input(component_id='dropdown_make', component_property='value'),
            Input(component_id='dropdown_model', component_property='value')])

def get_dropdown(make, model):
        filtered_df = df[(df.Make == make)&(df.Model == model)] 
        model_vals = df[df.Make == make].Model.value_counts().index
        dropdown_model = []
        for model_ in model_vals:
            dropdown_model.append({'label': model_, 'value': model_})
        condition_vals = filtered_df.Condition.value_counts().index
        dropdown_condition = []
        for condition_ in condition_vals:
            dropdown_condition.append({'label': condition_, 'value': condition_})

        color_vals = filtered_df.Color.value_counts().index
        dropdown_color = []
        for color_ in color_vals:
            dropdown_color.append({'label': color_, 'value': color_})

        drive_vals = filtered_df.Drive.value_counts().index
        dropdown_drive = []
        for drive_ in drive_vals:
            dropdown_drive.append({'label': drive_, 'value': drive_})

        fuel_vals = filtered_df.Fuel.value_counts().index
        dropdown_fuel = []
        for fuel_ in fuel_vals:
            dropdown_fuel.append({'label': fuel_, 'value': fuel_})
        
        title_vals = filtered_df.Title.value_counts().index
        dropdown_title = []
        for title_ in title_vals:
            dropdown_title.append({'label': title_, 'value': title_})
        
        cylinder_vals = sorted(filtered_df.Cylinders.unique().tolist())
        cylinder_vals = [str(i) for i in cylinder_vals]
        dropdown_cylinders = []
        for cylinders in cylinder_vals:
            dropdown_cylinders.append({'label': cylinders, 'value': cylinders})

        transmission_vals = sorted(filtered_df.Transmission_Automatic.unique().tolist())
        transmission_decode = {1:'Automatic', 0: 'Manual'}
        dropdown_transmission = []
        for transmission_ in transmission_vals:
            dropdown_transmission.append({'label': transmission_decode.get(transmission_), 'value': transmission_})

        return dropdown_model, dropdown_condition,  dropdown_color, dropdown_drive, dropdown_fuel,dropdown_title, dropdown_cylinders, dropdown_transmission

@app.callback(
            [Output(component_id='result', component_property='children'),
             Output(component_id='listings', component_property='data')],
            [Input(component_id = 'button',component_property = 'n_clicks')],
            [State(component_id='dropdown_year', component_property='value'),
            State(component_id='dropdown_make', component_property='value'),
            State(component_id='dropdown_model', component_property='value'),
            State(component_id='input_odometer', component_property='value'),
            State(component_id='dropdown_cylinders', component_property='value'),
            State(component_id='dropdown_condition', component_property='value'),
            State(component_id='dropdown_color', component_property='value'),
            State(component_id='dropdown_title', component_property='value'),
            State(component_id='dropdown_fuel', component_property='value'),
            State(component_id='dropdown_transmission', component_property='value'),
            State(component_id='dropdown_drive', component_property='value'),
            State(component_id='my-input', component_property='value')]
            )  


def get_price(clicks, year, make, model, odometer, cylinders, condition, color, title, fuel, transmission, drive, description):
        
        def fix_text(text): 
            if text == ' ':
                text = ''   
            elif text != '':
                text = text.lower()   
                pattern = r"\(([^()]*)\)"  # Define the pattern to match parentheses and their contents
                text = re.sub(pattern, r'\1', text)  # Use the sub() function from the re module to replace the pattern with its content without parentheses
                text = text.replace('!', '.').replace('?', '.') # Replace exclamation marks and question marks with periods
                punctuation = string.punctuation.replace(',', '').replace('.', '')  # Remove all punctuation except for commas and periods
                text = text.translate(str.maketrans('', '', punctuation)) # Remove leading/trailing whitespace
                text = text.strip() 
                text = re.sub(r'\s+([.])', r'\1', text)  # Replace any whitespace before a period with nothing
                if text.endswith(','): # If the text ends with a comma, replace the last character (comma) with a period
                    text = text[:-1] + '.'    
                if not text.endswith('.'): # If the text doesn't end with a period, add one
                    text += '.'    
                # Ensure that multiple periods at the end of the text are replaced with a single period
                text = re.sub(r'[.]+$', '.', text)
            else:
                pass
            return text

        description = description.strip()
        description = fix_text(description)

        if clicks == 0:
            return ' ',[]
        elif all([isinstance(var, str) and var for var in [make, model, cylinders, condition, color, title, fuel, drive]]) \
        and all([isinstance(var, int) and var for var in [year, odometer]]):
                Transmission = {'Automatic': 1, 'Manual': 0, 'Other':0}
                frame = pd.DataFrame(np.zeros([1,df_info.shape[1]]), columns = df_info.columns).drop(columns = ['Description'])
                frame['Make_'+ make] = 1 
                frame['Model_'+ model] = 1 
                frame['Drive_'+ drive] = 1 
                frame['Fuel_'+ fuel] = 1 
                frame['Title_'+ title] = 1
                frame['Color_'+ color] = 1 
                frame['Cylinders_'+ cylinders] = 1 
                frame['Condition_' + condition] = 1
                frame['Year'] = year 
                frame['Odometer'] = odometer 
                frame['Transmission_Automatic'] = Transmission.get(transmission)

                conn = pymssql.connect(server=hostname, port=port, user=username, password=password, database=database)
                cursor = conn.cursor()

                query = f"SELECT * FROM car_data WHERE Make = '{make}' and Model = '{model}' and Year BETWEEN {year - 2} AND {year + 2} ORDER BY Year, Odometer"

                cursor.execute(query)
                rows = cursor.fetchall()
                rows_new = []
                # Get column names from cursor.description
                columns = [column[0] for column in cursor.description]
                columns[7] = 'Transmission'
                for row in rows:
                    row_new = list(row)
                    row_new[-1] = "${:,}".format(row[-1])
                    row_new[7] = 'Automatic' if row_new[7] == 1 else 'Manual'
                    rows_new.append(tuple(row_new))
                rows = rows_new
                # Convert query result to list of dictionaries
                dict_result = [dict(zip(columns, row)) for row in rows]

                data = {
                    "description": description,
                    "frame": frame.to_dict(orient="list")                               
                }

                response = requests.post("https://price-predictor2.azurewebsites.net/api/MyFunction?code=QolQ40Wi7RtUD3fx77-KbCvhLfLN_Cw8WMr9-08B0LBOAzFu8QvLtg==", json=data)


                if response.status_code == 200:
                    price = response.text

                    return ("Your Vehicle Price is:    $" + str('{:,}'.format(int(price)))), dict_result
                else:
                    return "Technical difficutlties.... (Error: Could not get price from Azure Function)", []
                
        else: 
            return 'Please Fill All Fields',[]

if __name__ == '__main__':
    app.run_server(debug=True)