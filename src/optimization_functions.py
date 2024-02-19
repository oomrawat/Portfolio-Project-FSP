##########################################################################
##########################################################################

# Importing required libraries, modules, etc.

from scipy.optimize import minimize
import numpy as np
import math

##########################################################################
##########################################################################

# Function 1: Maximize Returns

def maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, maximum_ann_stdev, weightage_no_more_than):

    num_symbs = len(selected_stocks)

    selected_stocks_df = all_stocks_df[selected_stocks]

    if returns_type == 'LR':
        selected_stocks_returns_df = np.log(selected_stocks_df / selected_stocks_df.shift(1))
        selected_stocks_returns_df = selected_stocks_returns_df.dropna()
    elif returns_type == 'SR':
        selected_stocks_returns_df = selected_stocks_df.pct_change().dropna()

    returns_df_date_filter = selected_stocks_returns_df[(selected_stocks_returns_df.index >= buying_date_minus_1_year) & (selected_stocks_returns_df.index < buying_date)]

    covariance_matrix = returns_df_date_filter.cov()

    average_returns = returns_df_date_filter.mean()

    def daily_return(weights, average_returns):
        return np.dot(weights, average_returns)
    
    def annual_return(weights, average_returns):
        return ((daily_return(weights, average_returns)+1)**365)-1

    def daily_variance(weights, covariance_matrix):
        return np.dot(np.dot(weights, covariance_matrix), weights)
    
    def daily_standard_deviation(weights, covariance_matrix):
        return math.sqrt(daily_variance(weights, covariance_matrix))
    
    def annual_standard_deviation(weights, covariance_matrix):
        return daily_standard_deviation(weights, covariance_matrix) * math.sqrt(252)

    def objective_function(weights):
        return -annual_return(weights, average_returns)

    # Initial Guess
    initial_weights = [1/num_symbs]*num_symbs

    # Constraints and bounds remain the same as before
    constraints = (
        {'type': 'ineq', 'fun': lambda x: np.sum(x) - 1 + 0.01},  # Sum of weights >= 1 - tolerance
        {'type': 'ineq', 'fun': lambda x: 1 - np.sum(x) + 0.01},  # Sum of weights <= 1 + tolerance
        {'type': 'ineq', 'fun': lambda x: maximum_ann_stdev - annual_standard_deviation(x, covariance_matrix)},
        *({'type': 'ineq', 'fun': lambda x, i=i: weightage_no_more_than - x[i]} for i in range(num_symbs))
    )

    bounds = [(0, 1)] * len(initial_weights)

    # List of optimization methods to try
    # methods = ['cobyla', 'slsqp', 'trust-constr']
    methods = ['slsqp']

    # Dictionary to store the results
    results = {}

    # Run optimization using each method
    for method in methods:
        try:
            result = minimize(
                objective_function,
                initial_weights,
                method=method,
                bounds=bounds,
                constraints=constraints
            )
            results[method] = result

        except:
            pass

    # Select the result with the best objective function value
    best_method = max(results, key=lambda x: -objective_function(results[x].x))

    # Rounding the optimized weights of the best result
    best_weights = [round(weight, 4) for weight in results[best_method].x]

    return best_weights, best_method

##########################################################################
##########################################################################

# Function 2: Maximize Sharpe Ratio

def maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, weightage_no_more_than, govt_bond_df):

    num_symbs = len(selected_stocks)

    selected_stocks_df = all_stocks_df[selected_stocks]

    if returns_type == 'LR':
        selected_stocks_returns_df = np.log(selected_stocks_df / selected_stocks_df.shift(1))
        selected_stocks_returns_df = selected_stocks_returns_df.dropna()
    elif returns_type == 'SR':
        selected_stocks_returns_df = selected_stocks_df.pct_change().dropna()

    returns_df_date_filter = selected_stocks_returns_df[(selected_stocks_returns_df.index >= buying_date_minus_1_year) & (selected_stocks_returns_df.index < buying_date)]

    covariance_matrix = returns_df_date_filter.cov()

    average_returns = returns_df_date_filter.mean()

    adjusted_buy_date = govt_bond_df[govt_bond_df.index < buying_date].index[-1]
    risk_free_rate = govt_bond_df[govt_bond_df.index == adjusted_buy_date].values[0][0]/100

    def daily_return(weights, average_returns):
        return np.dot(weights, average_returns)
    
    def annual_return(weights, average_returns):
        return ((daily_return(weights, average_returns)+1)**365)-1

    def daily_variance(weights, covariance_matrix):
        return np.dot(np.dot(weights, covariance_matrix), weights)
    
    def daily_standard_deviation(weights, covariance_matrix):
        return math.sqrt(daily_variance(weights, covariance_matrix))
    
    def annual_standard_deviation(weights, covariance_matrix):
        return daily_standard_deviation(weights, covariance_matrix) * math.sqrt(252)

    def objective_function(weights):
        return -(annual_return(weights, average_returns)-risk_free_rate)/annual_standard_deviation(weights, covariance_matrix)

    # Initial Guess
    initial_weights = [1/num_symbs]*num_symbs

    # Constraints and bounds remain the same as before
    constraints = (
        {'type': 'ineq', 'fun': lambda x: np.sum(x) - 1 + 0.0001},  # Sum of weights >= 1 - tolerance
        {'type': 'ineq', 'fun': lambda x: 1 - np.sum(x) + 0.0001},  # Sum of weights <= 1 + tolerance
        *({'type': 'ineq', 'fun': lambda x, i=i: weightage_no_more_than - x[i]} for i in range(num_symbs))
    )

    bounds = [(0, 1)] * len(initial_weights)

    # List of optimization methods to try
    # methods = ['cobyla', 'slsqp', 'trust-constr']
    methods = ['slsqp']

    # Dictionary to store the results
    results = {}

    # Run optimization using each method
    for method in methods:
        try:
            result = minimize(
                objective_function,
                initial_weights,
                method=method,
                bounds=bounds,
                constraints=constraints
            )
            results[method] = result

        except:
            pass

    # Select the result with the best objective function value
    best_method = max(results, key=lambda x: -objective_function(results[x].x))

    # Rounding the optimized weights of the best result
    best_weights = [round(weight, 4) for weight in results[best_method].x]

    return best_weights, best_method

##########################################################################
##########################################################################

# Function 3: Minimize Variance

def minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, minimum_ann_ret, weightage_no_more_than):

    num_symbs = len(selected_stocks)

    selected_stocks_df = all_stocks_df[selected_stocks]

    if returns_type == 'LR':
        selected_stocks_returns_df = np.log(selected_stocks_df / selected_stocks_df.shift(1))
        selected_stocks_returns_df = selected_stocks_returns_df.dropna()
    elif returns_type == 'SR':
        selected_stocks_returns_df = selected_stocks_df.pct_change().dropna()

    returns_df_date_filter = selected_stocks_returns_df[(selected_stocks_returns_df.index >= buying_date_minus_1_year) & (selected_stocks_returns_df.index < buying_date)]

    covariance_matrix = returns_df_date_filter.cov()

    average_returns = returns_df_date_filter.mean()

    def daily_return(weights, average_returns):
        return np.dot(weights, average_returns)
    
    def annual_return(weights, average_returns):
        return ((daily_return(weights, average_returns)+1)**365)-1

    def daily_variance(weights, covariance_matrix):
        return np.dot(np.dot(weights, covariance_matrix), weights)
    
    def daily_standard_deviation(weights, covariance_matrix):
        return math.sqrt(daily_variance(weights, covariance_matrix))
    
    def annual_standard_deviation(weights, covariance_matrix):
        return daily_standard_deviation(weights, covariance_matrix) * math.sqrt(252)

    def objective_function(weights):
        return daily_variance(weights, covariance_matrix)

    # Initial Guess
    initial_weights = [1/num_symbs]*num_symbs

    # Constraints and bounds remain the same as before
    constraints = (
        {'type': 'ineq', 'fun': lambda x: np.sum(x) - 1 + 0.0001},  # Sum of weights >= 1 - tolerance
        {'type': 'ineq', 'fun': lambda x: 1 - np.sum(x) + 0.0001},  # Sum of weights <= 1 + tolerance
        {'type': 'ineq', 'fun': lambda x: annual_return(x, average_returns) - minimum_ann_ret},
        *({'type': 'ineq', 'fun': lambda x, i=i: weightage_no_more_than - x[i]} for i in range(num_symbs))
    )

    bounds = [(0, 1)] * len(initial_weights)

    # List of optimization methods to try
    # methods = ['cobyla', 'slsqp', 'trust-constr']
    methods = ['slsqp']

    # Dictionary to store the results
    results = {}

    # Run optimization using each method
    for method in methods:
        try:
            result = minimize(
                objective_function,
                initial_weights,
                method=method,
                bounds=bounds,
                constraints=constraints
            )
            results[method] = result

        except:
            pass

    # Select the result with the best objective function value
    best_method = min(results, key=lambda x: objective_function(results[x].x))

    # Rounding the optimized weights of the best result
    best_weights = [round(weight, 4) for weight in results[best_method].x]

    return best_weights, best_method