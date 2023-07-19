# Car_Price_Prediction: Project Overview

I create a web application that takes information about a vehicle such as year, make, model, mileage, condition, color, etc. as well as a description (NLP is used to process text input) and outputs an estimated price. Additionally, it will retrieve similar vehicle listings from an Azure database  .

It uses a machine learning algorithm trained on tens of thousands of used car listings that have been obtained through web scraping of Cragslist websites.

## EDA

Used bar plots to visualize vehicle frequency by Make as well as by Year: <br /><br /> 
<p align="center">
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/make_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_frequency.png"  width="80%" height="70%">

<br />
Here is a scatter plot of vehicle Price vs Year, with marker colors indicating the vehicle condition: <br /> <br /> 

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/condition_freq.png"  width="80%" height="70%">
<br>Bar plots visualizing the frequency of colors, fuel types, cylinders, drivetrain, and title status:<br>
<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/color_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/fuel_frequency.png"  width="80%" height="70%">  

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/cylinders_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/drive_frequency.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/title_frequency.png"  width="80%" height="70%">

<br /> <br /> Boxplots showing the distribution of data by price, odometer (mileage), and  year. Note: This technique was used for 
filtering out outliers in the raw dataset. The below boxplot shows the distribution of the cleaned dataset. For more details,
take a look at my EDA [notebook](https://github.com/AlexBandurin/car_price_prediction/blob/master/Used_Cars_Project_EDA.ipynb) <br /><br /> 

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/price_outliers.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/odometer_outliers.png" width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_outliers.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/price_dist.png"  width="80%" height="70%">

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/odometer_dist.png"  width="80%" height="70%">  

<img src="https://github.com/AlexBandurin/car_price_prediction/blob/master/year_dist.png"  width="80%" height="70%">
</p> 
