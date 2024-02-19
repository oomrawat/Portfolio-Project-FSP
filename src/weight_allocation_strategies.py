##########################################################################
##########################################################################

# Importing required libraries, modules, etc.

from optimization_functions import maximize_returns, maximize_sharpe_ratio, minimize_variance

##########################################################################
##########################################################################

# Weight Allocation Strategy 1

def weight_allocation_1(selected_stocks):

    num_stocks = len(selected_stocks)

    weightage = round(1/num_stocks,4)

    portfolio = {}

    for stock in selected_stocks:
        portfolio[stock] = weightage

    return portfolio, None

##########################################################################
##########################################################################

# Weight Allocation Strategy 2

def weight_allocation_2(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date):

    num_stocks = len(selected_stocks)

    if num_stocks > 8:
        best_weights, best_method = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, 0.25)

        stock_weights = list(zip(selected_stocks, best_weights))

        # Sort the pairs based on weights, in descending order
        sorted_stock_weights = sorted(stock_weights, key=lambda x: x[1], reverse=True)

        # Select the top 8 stocks
        selected_stocks = [stock for stock, weight in sorted_stock_weights[:8]]

        best_weights, best_method = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, 0.25)

    else:
        best_weights, best_method = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, 0.25)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, best_method


##########################################################################
##########################################################################

# Weight Allocation Strategy 3

def weight_allocation_3(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date):

    num_stocks = len(selected_stocks)

    if num_stocks > 8:
        best_weights, best_method = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, 0.4)

        stock_weights = list(zip(selected_stocks, best_weights))

        # Sort the pairs based on weights, in descending order
        sorted_stock_weights = sorted(stock_weights, key=lambda x: x[1], reverse=True)

        # Select the top 8 stocks
        selected_stocks = [stock for stock, weight in sorted_stock_weights[:8]]

        best_weights, best_method = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, 0.4)

    else:
        best_weights, best_method = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, 0.4)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, best_method

##########################################################################
##########################################################################

# Weight Allocation Strategy 4

def weight_allocation_4(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, govt_bond_df):
    
    num_stocks = len(selected_stocks)

    if num_stocks > 8:
        best_weights, best_method = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.25, govt_bond_df)

        stock_weights = list(zip(selected_stocks, best_weights))

        # Sort the pairs based on weights, in descending order
        sorted_stock_weights = sorted(stock_weights, key=lambda x: x[1], reverse=True)

        # Select the top 8 stocks
        selected_stocks = [stock for stock, weight in sorted_stock_weights[:8]]

        best_weights, best_method = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.25, govt_bond_df)

    else:
        best_weights, best_method = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.25, govt_bond_df)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, best_method

##########################################################################
##########################################################################

# Weight Allocation Strategy 5

def weight_allocation_5(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, govt_bond_df):
    
    num_stocks = len(selected_stocks)

    if num_stocks > 8:
        best_weights, best_method = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, govt_bond_df)

        stock_weights = list(zip(selected_stocks, best_weights))

        # Sort the pairs based on weights, in descending order
        sorted_stock_weights = sorted(stock_weights, key=lambda x: x[1], reverse=True)

        # Select the top 8 stocks
        selected_stocks = [stock for stock, weight in sorted_stock_weights[:8]]

        best_weights, best_method = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, govt_bond_df)

    else:
        best_weights, best_method = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, govt_bond_df)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, best_method
    

##########################################################################
##########################################################################

# Weight Allocation Strategy 6

def weight_allocation_6(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date):
    
    num_stocks = len(selected_stocks)

    if num_stocks > 8:
        best_weights, best_method = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.25)

        stock_weights = list(zip(selected_stocks, best_weights))

        # Sort the pairs based on weights, in descending order
        sorted_stock_weights = sorted(stock_weights, key=lambda x: x[1], reverse=True)

        # Select the top 8 stocks
        selected_stocks = [stock for stock, weight in sorted_stock_weights[:8]]

        best_weights, best_method = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.25)

    else:
        best_weights, best_method = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.25)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, best_method

##########################################################################
##########################################################################

# Weight Allocation Strategy 7

def weight_allocation_7(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date):
    
    num_stocks = len(selected_stocks)

    if num_stocks > 8:
        best_weights, best_method = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.4)

        stock_weights = list(zip(selected_stocks, best_weights))

        # Sort the pairs based on weights, in descending order
        sorted_stock_weights = sorted(stock_weights, key=lambda x: x[1], reverse=True)

        # Select the top 8 stocks
        selected_stocks = [stock for stock, weight in sorted_stock_weights[:8]]

        best_weights, best_method = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.4)

    else:
        best_weights, best_method = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.4)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, best_method

##########################################################################
##########################################################################

# Weight Allocation Strategy 8

def weight_allocation_8(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, govt_bond_df):

    min_var_weights, best_method_1 = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.2, 0.25)

    min_var_portfolio = dict(zip(selected_stocks, min_var_weights))

    max_ret_weights, best_method_2 = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.2, 0.25)

    max_ret_portfolio = dict(zip(selected_stocks, max_ret_weights))

    sorted_portfolio1 = sorted(min_var_portfolio.items(), key=lambda x: x[1], reverse=True)
    sorted_portfolio2 = sorted(max_ret_portfolio.items(), key=lambda x: x[1], reverse=True)

    # Initialize the number of stocks to pick
    num_to_pick = 4

    # Initialize sets to store selected stocks
    selected_stocks = set()

    while True:
        # Pick top stocks from each portfolio
        top_stocks_p1 = {stock for stock, _ in sorted_portfolio1[:num_to_pick]}
        top_stocks_p2 = {stock for stock, _ in sorted_portfolio2[:num_to_pick]}

        # Union the selected stocks
        selected_stocks = top_stocks_p1.union(top_stocks_p2)

        # Check if we have at least 8 stocks or reached the max possible
        if len(selected_stocks) >= 8 or (num_to_pick >= len(sorted_portfolio1) and num_to_pick >= len(sorted_portfolio2)):
            break

        # Increase the number of stocks to pick
        num_to_pick += 1
    
    best_weights, best_method_3 = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.25, govt_bond_df)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, (best_method_1, best_method_2, best_method_3)

##########################################################################
##########################################################################

# Weight Allocation Strategy 9

def weight_allocation_9(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, govt_bond_df):

    min_var_weights, best_method_1 = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.2, 0.4)

    min_var_portfolio = dict(zip(selected_stocks, min_var_weights))

    max_ret_weights, best_method_2 = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.2, 0.4)

    max_ret_portfolio = dict(zip(selected_stocks, max_ret_weights))

    sorted_portfolio1 = sorted(min_var_portfolio.items(), key=lambda x: x[1], reverse=True)
    sorted_portfolio2 = sorted(max_ret_portfolio.items(), key=lambda x: x[1], reverse=True)

    # Initialize the number of stocks to pick
    num_to_pick = 4

    # Initialize sets to store selected stocks
    selected_stocks = set()

    while True:
        # Pick top stocks from each portfolio
        top_stocks_p1 = {stock for stock, _ in sorted_portfolio1[:num_to_pick]}
        top_stocks_p2 = {stock for stock, _ in sorted_portfolio2[:num_to_pick]}

        # Union the selected stocks
        selected_stocks = top_stocks_p1.union(top_stocks_p2)

        # Check if we have at least 8 stocks or reached the max possible
        if len(selected_stocks) >= 8 or (num_to_pick >= len(sorted_portfolio1) and num_to_pick >= len(sorted_portfolio2)):
            break

        # Increase the number of stocks to pick
        num_to_pick += 1
    
    best_weights, best_method_3 = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, govt_bond_df)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, (best_method_1, best_method_2, best_method_3)

##########################################################################
##########################################################################

# Weight Allocation Strategy 10

def weight_allocation_10(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, govt_bond_df):

    max_shr_weights, best_method_1 = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.4, govt_bond_df)

    max_shr_portfolio = dict(zip(selected_stocks, max_shr_weights))

    min_var_weights, best_method_2 = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.4)

    min_var_portfolio = dict(zip(selected_stocks, min_var_weights))

    max_ret_weights, best_method_3 = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.4)

    max_ret_portfolio = dict(zip(selected_stocks, max_ret_weights))

    # Set to store stocks with at least 10% weight
    high_weight_stocks = set()

    # Function to add stocks with at least 10% weight from a given portfolio
    def add_high_weight_stocks(portfolio):
        for stock, weight in portfolio.items():
            if weight >= 0.1:
                high_weight_stocks.add(stock)

    # Check each portfolio
    add_high_weight_stocks(max_shr_portfolio)
    add_high_weight_stocks(min_var_portfolio)
    add_high_weight_stocks(max_ret_portfolio)

    selected_stocks = list(high_weight_stocks)

    best_weights, best_method_4 = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.2)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, (best_method_1, best_method_2, best_method_3, best_method_4)

##########################################################################
##########################################################################

# Weight Allocation Strategy 11

def weight_allocation_11(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, govt_bond_df):

    max_shr_weights, best_method_1 = maximize_sharpe_ratio(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.25, govt_bond_df)

    max_shr_portfolio = dict(zip(selected_stocks, max_shr_weights))

    min_var_weights, best_method_2 = minimize_variance(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.25)

    min_var_portfolio = dict(zip(selected_stocks, min_var_weights))

    max_ret_weights, best_method_3 = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.25)

    max_ret_portfolio = dict(zip(selected_stocks, max_ret_weights))

    # Set to store stocks with at least 10% weight
    high_weight_stocks = set()

    # Function to add stocks with at least 10% weight from a given portfolio
    def add_high_weight_stocks(portfolio):
        for stock, weight in portfolio.items():
            if weight >= 0.1:
                high_weight_stocks.add(stock)

    # Check each portfolio
    add_high_weight_stocks(max_shr_portfolio)
    add_high_weight_stocks(min_var_portfolio)
    add_high_weight_stocks(max_ret_portfolio)

    selected_stocks = list(high_weight_stocks)

    best_weights, best_method_4 = maximize_returns(selected_stocks, all_stocks_df, returns_type, buying_date_minus_1_year, buying_date, 0.3, 0.2)

    portfolio = dict(zip(selected_stocks, best_weights))

    return portfolio, (best_method_1, best_method_2, best_method_3, best_method_4)