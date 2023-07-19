# Car_Price_Prediction: Project Overview

I create a web application that takes information about a vehicle such as year, make, model, mileage, condition, color, etc. as well as a description (NLP is used to process text input) and outputs an estimated price. Additionally, it will retrieve similar vehicle listings from an Azure database  .

It uses a machine learning algorithm trained on tens of thousands of used car listings that have been obtained through web scraping of Cragslist websites.
## Web scraping
Using Selenium and BeautifulSoup Python packages, I was able to collect vehicle descriptions from over 50,000 Craigslist listsings. 
These variables included: **Vehicle info, Price, Cylinders, City (city the listing was posted in), Condition, Odometer (mileage), Paint Color, Time (time the listing was posted), Title Status, Drive (drivetrain), Fuel, Transmission, Description (vehicle description), Type (vehicle type), Size, Lat (latitude of seller location), Long (longtitude of seller location), Date(date the listing was posted), pID (unique id of the listing)** 

[Web scraping notebook](https://github.com/AlexBandurin/car_price_prediction/blob/master/clbot3.py)
## Data Cleansing
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
- Price
NOTE: The variables **Year**, **Make**, and **Model** have been extracted from the "Vehicle info" attribute attained in the web scraping stage

[Data Cleansing](https://github.com/AlexBandurin/car_price_prediction/blob/master/cl_cleansing.py)
## EDA

Used bar plots to visualize vehicle frequency by Make as well as by Year: <br /><br /> 
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/make_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_frequency.png"  width="80%" height="70%">
</p> 
<br /><br /> Here is a scatter plot of vehicle Price vs Year, with marker colors indicating the vehicle condition: <br /> <br /> 

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/condition_freq.png"  width="80%" height="70%">
Bar plots visualizing the frequency of colors, fuel types, cylinders, drivetrain, and title status:<br /><br /> 
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
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/price_outliers.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/odometer_outliers.png" width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_outliers.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/price_dist.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/odometer_dist.png"  width="80%" height="70%">  

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_dist.png"  width="80%" height="70%">
</p> 

[EDA notebook](https://github.com/AlexBandurin/car_price_prediction/blob/master/Used_Cars_Project_EDA.ipynb)

## Model Building
I tried several models, including Linear Regression, Decision Tree regressor, XGBoost regressor, and Random Forest Regressor.
To gauge performance, I used the R squared, where the independent variable is the actual value of the target variable,or price, and the dependent
variable is the "y hat" or the price predicted by the model. Additionally, I considered the Means Squared Error (MSE) and Mean Absolute Error (MAE).


R squared: 0.711, MAE: 3821.986, MSE: 30190283.525

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/LinReg_Plot.png"  width="60%" height="60%">
</p> 
<br>R squared: 0.639, MAE: 3789.584, MSE: 37757232.95 <br />

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/regression_tree_Plot.png"  width="60%" height="60%">
</p> 
R squared: 0.648, MAE: 3758.232, MSE: 36762406.605 <br />

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/random_forest_plot.png"  width="60%" height="60%">
</p> 
R squared: 0.825, MAE: 2757.316, MSE: 18291157.564 <br />

<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/xgboost_plot.png"  width="60%" height="60%">
</p> 

[Model Building notebook](https://github.com/AlexBandurin/car_price_prediction/blob/master/Prediction_Modeling.ipynb)
