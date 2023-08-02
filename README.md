# Car_Price_Prediction: Project Overview

I create a web application in **Plotly Dash** that takes information about a vehicle such as year, make, model, mileage, condition, color, etc. as well as a description (**NLP** is used to process text input) and outputs an estimated price. Additionally, it will retrieve similar vehicle listings from an **Azure database** that stores my data  .

It uses a **machine learning** algorithm trained on tens of thousands of used car listings that have been obtained through **web scraping** of Craigslist websites.

Here is the link to my web application: http://www.car-pricer.com/

I also recreated some visualizations exploring the trends in the used car market in Tableau. 
Here is my [Tableau Dashboard](https://public.tableau.com/app/profile/alexander.bandurin/viz/UsedCars_16899152133770/ColorFrequencies)

## Web scraping
[Web scraping file](https://github.com/AlexBandurin/car_price_prediction/blob/master/clbot3.py) <br /><br />
Using Selenium and BeautifulSoup Python packages, I was able to collect vehicle descriptions from over 50,000 Craigslist listsings. 
For higher efficiency, Object Oriented Programming (OOP) was used to implement web scraping. 

## Data Cleansing
[Data Cleansing File](https://github.com/AlexBandurin/car_price_prediction/blob/master/cl_cleansing.py) <br /><br />
The raw data was then cleaned and organized into a table with only the following variables:
- Year
- Make
- Model
- Condition
- Color
- Odometer
- Fuel
- Cylinders
- Title Status
- Drive
- Transmission
- Description
- Price <br />

NOTE: The variables **Year**, **Make**, and **Model** have been extracted from the "Vehicle info" attribute attained in the web scraping stage

## EDA
[EDA notebook](https://github.com/AlexBandurin/car_price_prediction/blob/master/Used_Cars_Project_EDA.ipynb) <br /><br />
Used bar plots to visualize vehicle frequency by Make as well as by Year: <br /><br /> 
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/make_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_frequency.png"  width="80%" height="70%">
</p> 
<br /><br /> Here is a scatter plot of vehicle Price vs Year, with marker colors indicating the vehicle condition: <br /> <br /> 
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/condition_freq.png"  width="80%" height="70%">
</p> 
Bar plots visualizing the frequency of colors, fuel types, cylinders, drivetrain, and title status: <br /><br /> 
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/color_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/fuel_frequency.png"  width="80%" height="70%">  

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/cylinders_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/drive_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/title_frequency.png"  width="80%" height="70%">
</p> 

I also considered heatmaps showing correlations between all the features:
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/corr_matrix.png"  width="60%" height="60%">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/corr_matrix_makes.png"  width="60%" height="60%">
</p> 
<br /> <br /> Boxplots and bar charts showing the distribution of data by price, odometer (mileage), and  year. Note: This technique was used for 
filtering out outliers in the raw dataset. The below boxplot shows the distribution of the cleaned dataset.
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/price_outliers.png"  width="70%" height="60%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/odometer_outliers.png" width="70%" height="60%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_outliers.png"  width="70%" height="60%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/price_dist.png"  width="70%" height="60%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/odometer_dist.png"  width="70%" height="60%">  

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_dist.png"  width="70%" height="60%">
</p> 

## Model Building
[Model Building notebook](https://github.com/AlexBandurin/car_price_prediction/blob/master/Used_Cars_Modeling.ipynb) <br /><br />
I tried several models, including Linear Regression, Decision Tree regressor, XGBoost regressor, and Random Forest Regressor.
To gauge performance, I used the R squared, where the independent variable is the actual value of the target variable,or price, and the dependent
variable is the "y hat" or the price predicted by the model. Additionally, I considered the Means Squared Error (MSE) and Mean Absolute Error (MAE).

The XGBoost algorithm has performed the best by far, so it is the one I decided to go with.

R squared: 0.711, MAE: 3821.986, MSE: 30190283.525

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/LinReg_Plot.png"  width="60%" height="60%">
</p> 
R squared: 0.639, MAE: 3789.584, MSE: 37757232.95 <br /><br />

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/regression_tree_Plot.png"  width="60%" height="60%">
</p> 
R squared: 0.8, MAE: 2883.438, MSE: 20877533.251 <br /><br />

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/random_forest_plot.png"  width="60%" height="60%">
</p> 
R squared: 0.825, MAE: 2757.316, MSE: 18291157.564 <br /><br />

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/xgboost_plot.png"  width="60%" height="60%">
</p> 

## Natural Language Processing (NLP)

[NLP Model Building](https://github.com/AlexBandurin/car_price_prediction/blob/master/Used_Cars_NLP_Models.ipynb)

I used BERT, a large language model (LLM) from Transformers for converting the text descriptions of each vehicle into vector form. 
I also tried the GloVe algorithm, but its performance has been noticeably worse. 

Methodology:
- The text contents of the vehicle description column are converted into 768 vectors using PyTorch and BERT
- Those vectors are appended to the original dataframe instead of the original textual description. 
- The resulting dataframe is run through XGBRegressor to create a price prediction model.

## Web application and Azure Functions

[Web Application]()
[Function App]()

I created a web application using Flask. Through a user-firendly interface, it takes vehicle information via drop-down menus and text input from the user and generates a price prediction. 
In order to optimize compute time and save space, the model has been uploaded to Azure Function App, a serverless compute platform that generates the price prediction every time a user clicks "Calculate". The information entered by a user is converted into JSON format, and is sent to the Function app via RESTful API interface. The price prediction is then returned to be displayed on the site. 

## SQL Database

Additionally, I added a real-time query feature, enabling dynamic data retrieval from Azure SQL database based on user input. Data from vehicle listings of the same make, model, and year as selected by the user are displayed on the webpage. It is also visualized on an interactive map (created with Folium), providing the user with geographical insight. 





