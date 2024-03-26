import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor, RandomForestRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


def regression_model_selector(X_train, y_train, X_test, y_test, ss=False, quick=False):
    results = []
    if quick == True:
        models = [
            ('lr', LinearRegression()),
            ('ridge', Ridge()),
            ('knn', KNeighborsRegressor()),
            ('dt', DecisionTreeRegressor())
        ]
    
    else: 
        models =[
            ('lr', LinearRegression()),
            ('ridge', Ridge()),
            ('knn', KNeighborsRegressor()),
            ('dt', DecisionTreeRegressor()),
            ('rf', RandomForestRegressor()),
            ('adab', AdaBoostRegressor()),
            ('svr', SVR()),
        ]

    if ss == True:
        print('Using StandardScaler')
        for name, model in models:
            pipeline = Pipeline([
                ('scaler', StandardScaler()), 
                ('regressor', model) 
            ])
            
            pipeline.fit(X_train, y_train)
            
            predictions = pipeline.predict(X_test)
            
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            cv = cross_val_score(pipeline, X_train, y_train, cv=5).mean()
            train_score = pipeline.score(X_train, y_train)
            test_score = (pipeline.score(X_test, y_test))
            
            # store the results in results list
            results.append((name, rmse,cv, train_score, test_score))
        results = pd.DataFrame(results, columns = ['model', 'rmse', 'cv', 'train_score', 'test_score'])
        results['varience'] = results['train_score'] - results['test_score']
        return results

    elif ss == False: 
        print('Not using StandardScaler')
        for name, model in models:
            pipeline = Pipeline([
                ('regressor', model) 
            ])
            
            pipeline.fit(X_train, y_train)
            
            predictions = pipeline.predict(X_test)
            
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            cv = cross_val_score(pipeline, X_train, y_train, cv=5).mean()
            train_score = pipeline.score(X_train, y_train)
            test_score = (pipeline.score(X_test, y_test))
            
            # store the results in results list
            results.append((name, rmse,cv, train_score, test_score))
        results = pd.DataFrame(results, columns = ['model', 'rmse', 'cv', 'train_score', 'test_score'])
        results['varience'] = results['train_score'] - results['test_score']
        return results
    

def model_summary(model, X_train, X_test, y_train, y_test, log_target=False, cv=5, decplaces=3, coef =False):
    
    model = model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_pred = model.predict(X_test)
    if log_target == True:
        print(f"Exponent Root Mean Squared Error (RMSE): {round(np.exp(np.sqrt(mean_squared_error(y_test, y_pred))),decplaces)}")

    print(f"Root Mean Squared Error (RMSE): {round(np.sqrt(mean_squared_error(y_test, y_pred)),decplaces)}")
    print(f"Train R-squared (R2): {round(r2_score(y_train, y_train_pred),3)}")
    print(f"Test R-squared (R2): {round(r2_score(y_test, y_pred),3)}")
    crossval = cross_val_score(model, X_train, y_train, cv = cv, scoring='r2')
    if crossval.mean() < 0:
        print(f"High varience noted in cross validation: {crossval}")
        print(f"Cross validated r2: {round(crossval.mean(),decplaces)}")
    else:
        print(f"Cross validated r2: {round(crossval.mean(),decplaces)}")

    return model, y_pred

def plot_residuals(y, predicitons, figsize=(7, 5), colour = 'mediumpurple', line_colour='lightpink'): 
    residuals = y - predicitons
    plt.figure(figsize=figsize)
    plt.scatter(y, residuals, color=colour)
    plt.axhline(y=0, color=line_colour, linestyle='--', edgecolor='k')
    plt.xlabel('Actual Values')
    plt.ylabel('Residuals')
    plt.title('Residuals and Actual Values');
    return residuals