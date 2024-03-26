# Investment-Grade Wine - README 
Capstone Aaran Daniel
Predictive Modelling and Application Development for Investment-Grade (Fine) Wine

## Intro
You many not know that investment grade wine is traded - with daily price fluctuations - like many other asset classes. Yes, consumers do drink these wines on occasion but there is another market for them, investors. These investors buy fine wines by the crate to hold securely 'in bond' for later resale, hopefully at a profit. Investment grade wines are charactrised by: 1. Their ability to improve in taste over time and; 2. Brand or producer recognition within the wine trade. Only certain regions are generally considered to make investment-grade wine namely: Napa Valley (US), Piedmont and Tuscany (Italy), Bordeaux, Burgundy, Champagne, and Rhone (France).

## Problem Statement
I work for a wine investment advisory company. The company would like predict future prices of investment-grade wines to successfully advise customers on investments. This task involves identifying underprices wines and building a predictive time series model that predits the price appreciation over the coming X months (TBC). The company would also like back-of-house application for the sales team, allowing them to quickly search the portfolio for wines and provide historical returns to potential customers/investors.

## Primary Aim
Develop a predictive model using historical price data of investment-grade wines to forecast future price appreciation.

## Secondary Aims
- Identify key price predictive features of investment-grade wines.<br>
- Discover additional trends within the investment-grade wine portfolio for sales/marketing strategies when onboarding new customers.<br>
- Identify currently undervalued wines and those beneficial for the sales/marketing strategies, emphasizing:<br>
  1. Growth of back vintages to reassure investors.<br>
  2. Data-driven selection of great wines at great valuations to persuade customers to invest.<br>
- Build a back-of-house application for quick portfolio searches and providing investment returns to potential investors.<br>

## Metric for Success

Looking at historic price volatility to work out how we define a successful prediction. Define average volitility - for example if wine prices generally only move 5% max a year, target RSME less than 5% of price. If we find significant variation in volatility across categories (e.g. vintages or producers) we can set some more specific targets.<br>

## Process

### 1. Data Collection
- **Source**: Wine Compare API, access confirmed awaiting access key<br>
- **Key Features**: price history, current market price, vintage, region, producer, bottle size, weather data, critics ratings, grape variety, rarity, production quantities, brand power, regional vintage quality, optimum drinking age. Optional additions: Cru Classe status (or equivalent), Robert Parker score, Averaged Other Critics' score, Wine-Searcher rank / Google reach, Weighted production levels, Liquidity as evidenced by Liv-ex bid/offer spread, Supply to market over time.<br>
- **Core Wine Regions to focus on**: Napa Valley (US), Piedmont and Tuscany (Italy), Bordeaux, Burgundy, Champagne, and Rhone (France). (Secondary importance: Spain and Australia)<br>

### 2. Data Preparation
- Combine data sources, handle missing values/outliers.<br>
- Feature Engineering: <br>
        - Climate effects (with a combination of year and region info)<br>
        - price-to-rating ratio<br>
        - historical price volatility: via standard deviation or beta. <br>
                - Standard deviation: calculate the standard deviation of each wine and split wines into binary volitile or not, or use standard deviation as a feature?<br>
                - Beta: Use the liv ex 100 to set a benchmark, calculate covariance between the wines and the bench mark. beta = covariance / market_variance. (A beta greater than 1 indicates that the stock is more volatile than the market, while a beta less than 1 suggests it is less volatile.)<br>
        - Critic Name and Critic score interaciton variable. e.g. <br>
- Scale features for unbiased model training.<br>
- Are critics ratings more/less predictive of prices within certain regions that are more under the spotlight?<br>

### 3. EDA - Aggregate Level
- Calculate summary statistics like mean, median, and standard deviation of price changes.<br>
- Explore correlations between price changes and potential features like vintage, region, grape variety, critic ratings, and auction history.<br>
- Identify trends in the data particularly those which can be of use to sales and marketing teams. <br>
- Find initial coefficients with LR.<br>
- Investigate is "Burgundy is overpriced at the moment vs. Bordeaux which is underpriced".<br>
- Start at market level then analyse: region, year, producer.<br>
- Research suggests removing bottles prices above $50,000 USD <br>
- Critic's scores distributions will be a key thing to analyse at this stage. <br>

### 4. EDA - Individual Wine Level
- Investigate price trends for individual wines over time.<br>
- Analyse the distribution of price changes for different wine characteristics.<br>
- Visualise relationships between features and price changes for individual wines.<br>
- Find initial coefficients with LR.<br>
- Investigate current market wisdom 'younger vintages perform better and that brand equity / critic scores / vintage quality vs. price is the deciding factor.'<br>
- Look at daily volitility and consider smoothing out the volitility with rolling mean.<br>
- It has been suggested in research that past significant increases in wine prices suggest a slowing in appreciation in future - ie the opposite of momentum. <br>
-  SHAP analysis (not sure exaclty how this fits in, need to do more research) https://shap.readthedocs.io/en/latest/ <br>
- Identify wines producers which have averaged high critic scores over 3-4 vintages in a row? <br>
- Isolate limited production wines and analyse them seperately are there any in renowned regions that are below average prices for the region?<br> 
- Look for wines with a differential between vintage/region average and wine price.

**Preliminary research suggests the following to verify:**
- "Lower price ranges have better returns." Perhaps this is explained by the lower priced wines still having appeal to drinking purchasers as opposed to just investors. <br>
- Salient brands names actually have worse returns - the big names perform worse over time. They are already expensive to their brand recogintion is alread 'priced in'. Where as un up and comer is yet to have their boom.<br>
- 'Collectors items' have worse returns.<br>

### 5. Modelling

#### Initial Modelling Process Idea: 
**STEP ONE - REGRESSION**
Aim: Discover more predictive features which should be used as exogenous variables in time series modelling (step 3)<br>
Method: White box regression modelling. Linear regression to analyse the linear relationship between features and price appreciation. Decision Trees to identify important features and potential non-linear relationships.<br>
Granularity: At the wine level, where each observation is a different wine, with price over time aggregated (see target below).<br>
Potential Targets: 1. Average price over timeframe or;2. Current market price?; <br>

**STEP TWO - CLUSTERING:**
Aim: Create a short list of wines to focus on for time series modeling (step 3).<br>
Method: Unsupervised learning, hide price from the model then cluster the wines. Plot the individual clusters with price added back in, identify clusters where ceratin wines are underpriced (or overpriced) compared to the rest of the cluster.<br>
Granularity: Same as step 1, at the wine level with prices aggregated over time in someway.<br>

**STEP THREE - TIME SERIES:**
Method: Having identified wines to focus on, time series model an ARIMA baseline, move on to SARIMAX, VAR, perhaps facebook Prophet and RNNs depending on the amount of data. Use those predictive features identified in step 1 as exogenous variables.<br>
Granularity: observations of daily prices, each model is for an individual wine - (is it possible to model multiple wines at once?).<br>
Target: future price but the model will be train/test split on past prices of course.<br>
Goal: Build a model that accurately predicts future prices.<br>

#### Other Modelling Ideas 
    * Do a lagged regression model trained to predict prices at a set point in the future, either to verify time series findings or as a method to identify wines that will appreciate in the future. (Accurate but less interpreablt models Random forests and Gradient Boosting (XGB) might be best suited to this: improving prediction accuracy.)
    * Consider ensemble methods to combine predictions from multiple models for improved accuracy? (e.g., aggregate and individual, I dont fully understand this yet but did come up in my research)
    * Long Short-Term Memory (LSTM) networks: Handle complex temporal dependencies in price data.
    * Considering clustering spark AWS?
    * XGBoost for time series  https://machinelearningmastery.com/xgboost-for-time-series-forecasting/ 

### 6. Evaluation and Iteration
- Use metrics like root mean squared error (RMSE) or R-squared to assess prediction accuracy.<br>
- Use cross-validation techniques specific to time series data, like Time Series Split or Walk Forward Validation.<br>
- Pros and cons of initial iteration of the model. <br>
- Implement monitoring to track model performance over time, and plan for periodic retraining as new data becomes available.<br>
- Wait for more data to come out and test predicitons it on real daily data!<br>

## Potential Challenges
- Insufficient data or attributes.<br>
- Lack of domain knowledge for market segmentation.<br>
- Time series modelling difficulties and unpredictability. <br>
- Possible need for bespoke models per wine category.<br>
- Computational and resource limitations for advanced models.<br>
- Risk of models predicting current trends without offering new insights.<br>

## The Application: 
Purpose: Allow sales are marketing team to quickly search wines and provide historical returns information to prospective customers (potential wine investors). 

Functionality: 
1. Type in the name of a wine and see how back vintages have performed over different time horizons (i.e. how they have appreciated). 

2. Recommend a portfolio based on a budget (e.g. these are the most undervalued wines on the market right now).


## Future Analysis Ideas: 
        * Consider NLP approach, incorporating sentiment analysis from wine reviews. Can we gain an edge on the market by scraping sentiment from vivino, twitter, reddit for sentiments on vintage wines. 
        * Setting some predictions on wines / categories or interest and waiting. In 3 or 4 months down the line seeing how the model performs. The more we do this the better.
        * Influencer analysis or scraping En Primeur releases, Decanter World Wine Awards or International Wine Challenge, to get an edge on the market. 
        * Explore adittional regions: Priorat in Spain, Willamette Valley in Oregon, or Stellenbosch in South Africa.
        * Look for consistent winners in prestigious awards like 


## Expected Imports (TBC)
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller



import warnings # necessary b/c pandas & statsmodels datetime issue
warnings.simplefilter(action="ignore")

Other: 
import VARIMA from DARTS
Prophet 
