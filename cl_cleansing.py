import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import re


#pd.set_option('display.float_format', lambda x: '%.4f' % x)

order_old = ['Year','Make','Model','Price','Condition','Odometer','Paint Color','Extra_Info','Vehicle info','Vehicle info 2','Cylinders','City','Time',\
          'Title Status','Drive','Fuel','Transmission','Lat','Long','Date','pID']
order = ['Year','Make','Model','Condition','Color','Odometer','Fuel','Cylinders','Title Status','Drive','Transmission','Description',"Price"]

df = pd.read_csv('car_data-LasVegas_.csv')


nnl1 = []
nnl2 = []
makes = {'Chevy': 'Chevrolet', 'Vw' : 'Volkswagen'}

df['Cylinders'] = df['Cylinders'].str.extract(pat='(\d+)', expand=False)
df['Time'] = df['Time'].str.replace(';',':')

# Drop all rows where "Condition" is NaN.
df.to_csv('car_data_sorted-LasVegas2_.csv',index = False)
print('Original length of table: ', len(df))
len_df_old = len(df)
dropped = df.dropna(subset = ['Condition']).shape[0]/len_df_old
df = df.dropna(subset = ['Condition']).reset_index(drop = True)
print('Percentage of rows with nan Condition dropped: ' + str(round(100*(1  - (dropped)),2)) + '%')
len_df = len(df)

df['Year'] = np.zeros(len_df, dtype = np.int8)
df['Make'] = np.zeros(len_df, dtype = np.int8)
df['Model'] = np.zeros(len_df, dtype = np.int8)
df['Extra_Info'] = np.zeros(len_df)

for i in range(len_df-1):
    #clean duplicate year in 'year make model'
    df.loc[i,'Vehicle info 2'] = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', str(df['Vehicle info 2'][i]))
    df.loc[i,'Vehicle info'] = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', str(df['Vehicle info'][i]))
    
    if df.loc[i,'Vehicle info'] == '~' or len(df.loc[i,'Vehicle info'].split()) < 3:
        if len(df.loc[i,'Vehicle info 2'].split(' ')[0]) == 4 and df.loc[i,'Vehicle info 2'].split(' ')[0].isdigit():
            if len(df.loc[i,'Vehicle info 2'].split()) > 0:
                df.loc[i,'Year'] = df['Vehicle info 2'][i].split(' ')[0]
            if len(df.loc[i,'Vehicle info 2'].split()) > 1:
                df.loc[i,'Make'] = df['Vehicle info 2'][i].split(' ')[1]
            if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                if df['Vehicle info 2'][i].split(' ')[1] == 'Ford' and (df['Vehicle info 2'][i].split(' ')[2] == 'F' or df['Vehicle info 2'][i].split(' ')[2] == 'E'):
                    df.loc[i,'Model'] = ''.join(df['Vehicle info 2'][i].split(' ')[2:4])   
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Mercedes' and df['Vehicle info 2'][i].split(' ')[2] == 'Benz':
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[3]   
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Land' and df['Vehicle info 2'][i].split(' ')[2] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[3]  
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Range' and df['Vehicle info 2'][i].split(' ')[2] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = "Range Rover" 
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Mini' and df['Vehicle info 2'][i].split(' ')[2] == 'Cooper':
                    df.loc[i,'Make'] = "Mini Cooper"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[3]  
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Tesla' and df['Vehicle info 2'][i].split(' ')[2] == 'Model':
                    df.loc[i,'Make'] = "Tesla"
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = "Model " + df['Vehicle info 2'][i].split(' ')[3] 
                elif df['Vehicle info 2'][i].split(' ')[1] == 'F' and df['Vehicle info 2'][i].split(' ')[2] == '150':
                    df.loc[i,'Make'] = "Ford"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = "F150" 
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Saab' and df['Vehicle info 2'][i].split(' ')[2] == '9':
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = "9 " + df['Vehicle info 2'][i].split(' ')[3]              
                elif df['Vehicle info 2'][i].split(' ')[1] == 'Honda' and df['Vehicle info 2'][i].split(' ')[2] == 'Cr':
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = "Crv"       
                else:
                    df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[2].replace('-','')
            extra_info = []
            for k in df.loc[i,'Vehicle info 2'].split(' ')[3:]:
                extra_info.append(k)
            df.loc[i,'Extra_Info'] = ' '.join(extra_info)

        else: 
            for j in df.loc[i,'Vehicle info 2'].split(' '):
                if len(j) == 4 and j.isdigit():
                    df.loc[i,'Year'] = j  
            if len(df.loc[i,'Vehicle info 2'].split()) > 0:
                df.loc[i,'Make'] = df['Vehicle info 2'][i].split(' ')[0]
            if len(df.loc[i,'Vehicle info 2'].split()) > 1:
                if df['Vehicle info 2'][i].split(' ')[0] == 'Ford' and (df['Vehicle info 2'][i].split(' ')[1] == 'F' or df['Vehicle info 2'][i].split(' ')[1] == 'E'):
                    df.loc[i,'Model'] = ''.join(df['Vehicle info 2'][i].split(' ')[1:3]) 
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Mercedes' and df['Vehicle info 2'][i].split(' ')[1] == 'Benz':  
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[2]       
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Land' and df['Vehicle info 2'][i].split(' ')[1] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[2]  
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Range' and df['Vehicle info 2'][i].split(' ')[1] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = "Range Rover" 
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Mini' and df['Vehicle info 2'][i].split(' ')[1] == 'Cooper':
                    df.loc[i,'Make'] = "Mini Cooper"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[2] 
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Tesla' and df['Vehicle info 2'][i].split(' ')[1] == 'Model':
                    df.loc[i,'Make'] = "Tesla"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = "Model " + df['Vehicle info 2'][i].split(' ')[2] 
                elif df['Vehicle info 2'][i].split(' ')[0] == 'F' and df['Vehicle info 2'][i].split(' ')[1] == '150':
                    df.loc[i,'Make'] = "Ford"
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = "F150"
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Saab' and df['Vehicle info 2'][i].split(' ')[1] == '9':
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = "9 " + df['Vehicle info 2'][i].split(' ')[2] 
                elif df['Vehicle info 2'][i].split(' ')[0] == 'Honda' and df['Vehicle info 2'][i].split(' ')[1] == 'Cr':
                    if len(df.loc[i,'Vehicle info 2'].split()) > 2:
                        df.loc[i,'Model'] = "Crv"   
                else:
                    df.loc[i,'Model'] = df['Vehicle info 2'][i].split(' ')[1].replace('-','')
            extra_info = []
            for k in df.loc[i,'Vehicle info 2'].split(' ')[2:]:
                extra_info.append(k)
            df.loc[i,'Extra_Info'] = ' '.join(extra_info)
    else:
        if len(df.loc[i,'Vehicle info'].split(' ')[0]) == 4 and df.loc[i,'Vehicle info'].split(' ')[0].isdigit():
            if len(df.loc[i,'Vehicle info'].split()) > 0:
                df.loc[i,'Year'] = df['Vehicle info'][i].split(' ')[0]
            if len(df.loc[i,'Vehicle info'].split()) > 1:
                df.loc[i,'Make'] = df['Vehicle info'][i].split(' ')[1]
            if len(df.loc[i,'Vehicle info'].split()) > 2:
                if df['Vehicle info'][i].split(' ')[1] == 'Ford' and (df['Vehicle info'][i].split(' ')[2] == 'F' or df['Vehicle info'][i].split(' ')[2] == 'E'):
                    df.loc[i,'Model'] = ''.join(df['Vehicle info'][i].split(' ')[2:4])    
                elif df['Vehicle info'][i].split(' ')[1] == 'Mercedes' and df['Vehicle info'][i].split(' ')[2] == 'Benz':  
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[3]
                elif df['Vehicle info'][i].split(' ')[1] == 'Land' and df['Vehicle info'][i].split(' ')[2] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[3]  
                elif df['Vehicle info'][i].split(' ')[1] == 'Range' and df['Vehicle info'][i].split(' ')[2] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = "Range Rover" 
                elif df['Vehicle info'][i].split(' ')[1] == 'Mini' and df['Vehicle info'][i].split(' ')[2] == 'Cooper':
                    df.loc[i,'Make'] = "Mini Cooper"
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[3]
                elif df['Vehicle info'][i].split(' ')[1] == 'Tesla' and df['Vehicle info'][i].split(' ')[2] == 'Model':
                    df.loc[i,'Make'] = "Tesla"
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = "Model " + df['Vehicle info'][i].split(' ')[3]
                elif df['Vehicle info'][i].split(' ')[1] == 'F' and df['Vehicle info'][i].split(' ')[2] == '150':
                    df.loc[i,'Make'] = "Ford"
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = "F150"
                elif df['Vehicle info'][i].split(' ')[1] == 'Saab' and df['Vehicle info'][i].split(' ')[2] == '9':
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = "9 "+ df['Vehicle info'][i].split(' ')[3]
                elif df['Vehicle info'][i].split(' ')[1] == 'Honda' and df['Vehicle info'][i].split(' ')[2] == 'Cr':
                    if len(df.loc[i,'Vehicle info'].split()) > 3:
                        df.loc[i,'Model'] = "Crv"    
                else:
                    df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[2].replace('-','')
            extra_info = []
            for k in df.loc[i,'Vehicle info'].split(' ')[3:]:
                extra_info.append(k)
            df.loc[i,'Extra_Info'] = ' '.join(extra_info)

        else: 
            for j in df.loc[i,'Vehicle info'].split(' '):
                if len(j) == 4 and j.isdigit():
                    df.loc[i,'Year'] = j  
            if len(df.loc[i,'Vehicle info'].split()) > 0:
                df.loc[i,'Make'] = df['Vehicle info'][i].split(' ')[0]
            if len(df.loc[i,'Vehicle info'].split()) > 1:
                if df['Vehicle info'][i].split(' ')[0] == 'Ford' and (df['Vehicle info'][i].split(' ')[1] == 'F' or df['Vehicle info'][i].split(' ')[1] == 'E'):
                    df.loc[i,'Model'] = ''.join(df['Vehicle info'][i].split(' ')[1:3])        
                elif df['Vehicle info'][i].split(' ')[0] == 'Mercedes' and df['Vehicle info'][i].split(' ')[1] == 'Benz': 
                    if len(df.loc[i,'Vehicle info'].split()) > 2: 
                        df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[2]      
                elif df['Vehicle info'][i].split(' ')[0] == 'Land' and df['Vehicle info'][i].split(' ')[1] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[2]  
                elif df['Vehicle info'][i].split(' ')[0] == 'Range' and df['Vehicle info'][i].split(' ')[1] == 'Rover':
                    df.loc[i,'Make'] = "Land Rover"
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = "Range Rover" 
                elif df['Vehicle info'][i].split(' ')[0] == 'Mini' and df['Vehicle info'][i].split(' ')[1] == 'Cooper':
                    df.loc[i,'Make'] = "Mini Cooper"
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[2]
                elif df['Vehicle info'][i].split(' ')[0] == 'Tesla' and df['Vehicle info'][i].split(' ')[1] == 'Model':
                    df.loc[i,'Make'] = "Tesla"
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = "Model " + df['Vehicle info'][i].split(' ')[2]
                elif df['Vehicle info'][i].split(' ')[0] == 'F' and df['Vehicle info'][i].split(' ')[1] == '150':
                    df.loc[i,'Make'] = "Ford"
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = "F150"
                elif df['Vehicle info'][i].split(' ')[0] == 'Saab' and df['Vehicle info'][i].split(' ')[1] == '9':
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = "9 "+ df['Vehicle info'][i].split(' ')[2]
                elif df['Vehicle info'][i].split(' ')[0] == 'Honda' and df['Vehicle info'][i].split(' ')[1] == 'Cr':
                    if len(df.loc[i,'Vehicle info'].split()) > 2:
                        df.loc[i,'Model'] = "Crv"    
                else:
                    df.loc[i,'Model'] = df['Vehicle info'][i].split(' ')[1].replace('-','')
            extra_info = []
            for k in df.loc[i,'Vehicle info'].split(' ')[2:]:
                extra_info.append(k)
            df.loc[i,'Extra_Info'] = ' '.join(extra_info)

    for make in makes:
        if df.loc[i, 'Make'] == make:
            df.loc[i, 'Make'] = makes.get(make)

# df['City'] = df['City'].astype('category')
# df['Condition'] = df['Condition'].astype('category')
# df['Cylinders'] = df['Cylinders'].astype('category')
# df['Drive'] = df['Drive'].astype('category')
# df['Fuel'] = df['Fuel'].astype('category')
# df['Paint Color'] = df['Paint Color'].astype('category')
# df['Title Status'] = df['Title Status'].astype('category')
# df['Transmission'] = df['Transmission'].astype('category')
# df['Make'] = df['Make'].astype('category') 

#df.to_csv('car_data_sorted_Miami2.csv', index = False)

#df_models2 = pd.read_csv('/Users/alex/Data_Science/Used_Cars/Used_Cars_Project/vehicle_models_updated.csv')
# df_models2.rename(columns={"make": "Make", "model": "Model",'drive':"Drive",'cylinders':"Cylinders",\
#                           'VClass':"Class"},inplace = True)
# for i in range(len(df_models2)):
#     if df_models2.loc[i,'Make'] == 'Mercedes-benz':
#                df_models2.loc[i,'Make'] = 'Mercedes'

# df1 = df.loc[:,['Make','Model','Cylinders','Drive']]
# df_models21 = df_models2.loc[:,['Make','Model','Cylinders','Drive']]
# df1 = df1.combine_first(df_models21).loc[df1.index.tolist()].loc[:,['Make','Model','Cylinders','Drive']]

#df1 = pd.concat([df1,df.loc[:,['Paint Color']]], axis=1,ignore_index=True, sort=True)
#df1.rename(columns = {0:'Make',1:'Model',2:'Cylinders',3:'Drive',4:'Color'}, inplace = True)

# unfilled_cars = []
# cnt = 0
# len_df = len(df1)
# for j,k in zip(['Color'],[5]):
#     for i in range(1,len_df):
#         if not isinstance(df1.loc[i,j], str):
#             df_t = df1[(df1['Make'] == df1.loc[i,['Make']][0]) & (df1['Model'] == df1.loc[i,['Model']][0])][j]
#             df_t = df_t[~df_t.isna()]
#             try:
#                 if len(df_t) > k:
#                     df1.loc[i,j] = df_t.mode()[:1][0]
#                 else:
#                     raise Exception('Too short')
#             except Exception as e: 
#                     cnt +=1
#                     unfilled_cars.append(str(df1.loc[i,['Make']][0])+' '+str(df1.loc[i,['Model']][0]))
#                     pass
            
# for j,k in zip(['Drive','Cylinders','Color'],[2,2,6]):
#     for i in range(1,len_df):
#         if not isinstance(df1.loc[i,j], str):
#             df_t = df1[(df1['Make'] == df1.loc[i,['Make']][0]) & (df1['Model'] == df1.loc[i,['Model']][0])][j]
#             df_t = df_t[~df_t.isna()]
#             try:
#                 if len(df_t) > k:
#                     df1.loc[i,j] = df_t.mode()[0]
#                 else:
#                     raise Exception('Too short')
#             except Exception as e: 
#                     cnt +=1
#                     # print('exception', e)
#                     # print(j)
#                     # print('len of df_t:', len(df_t))
#                     # print(cnt)
#                     unfilled_cars.append(str(df1.loc[i,['Make']][0])+' '+str(df1.loc[i,['Model']][0]))
#                     # print(str(df1.loc[i,['Make']][0])+' '+str(df1.loc[i,['Model']][0]))
#                     pass

# df = pd.concat([df1,df.loc[:,['Year',"Condition", "Title Status","Transmission",'Odometer','Fuel',"Price"]]], axis=1)
# df.reset_index(drop = True)
# df.rename(columns = {0:'Make',1:'Model',2:'Cylinders',3:'Drive',4:'Color',5:'Year',6:"Condition",\
#                      7:"Title Status", 8:"Transmission", 9:'Odometer',10:'Fuel', 11: "Price"}, inplace = True)

# Order df columns
df.rename(columns = {"Paint Color":"Color"}, inplace = True)
df = df.loc[:,order]
# Delete all "Makes with less than one frequency"


# df.drop('Color',axis = 1, inplace = True)
# df = df.replace(None, '', regex=True)
# print(df[order[:6]][:35])
# print(df[order[6:]][:35])
# # print(df.shape)
# print(df.info())
    
# Delete values with null "year", "make", and "model" 
#df = df.loc[(df['Year'] != 0) & (df['Year'] != '0') & (df['Make'] != 0) & (df['Model'] != 0) & (df['Model'] != '0')]

# create a filter for "Price" and "Odometer" features
# q_low1 = df["Price"].quantile(0.01)
# q_hi1  = df["Price"].quantile(0.95)
# q_hi2  = df["Odometer"].quantile(0.95)
#q_hi3  = df["Year"].quantile(0.99)

# df = df[(df["Price"] < q_hi1) & (df["Price"] > q_low1) & (df["Odometer"] < q_hi2)]
        # & (df["Year"] < q_hi3)]
#df.fillna('',inplace = True)
df.to_csv('car_data_sorted-LasVegas_.csv', index = False)

#df_models2.to_csv('/Users/alex/Data_Science/Used_Cars/Used_Cars_Project/vehicle_models_updated.csv')
