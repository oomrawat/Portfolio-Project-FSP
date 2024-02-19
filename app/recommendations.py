import pandas as pd
import sys
sys.path.append('../src')
from functions import stock_selection_weight_allocation, adjust_portfolio, generate_and_save_data
from datetime import datetime

def custom_round(number):
    # Separate the number into the integer and decimal parts
    integer_part = int(number)
    decimal_part = number - integer_part
    
    # Check if the decimal part is above .75; if so, round up
    if decimal_part > 0.8:
        return integer_part + 1
    else:
        return integer_part
    
def calculate_shares_to_buy_with_prices(portfolio_weights, prices_df, buying_date, total_investment):

    buying_date = prices_df[prices_df.index <= buying_date].index[-1]

    # Step 1: Calculate initial amount to be invested in each stock
    initial_investment = {stock: weight * total_investment for stock, weight in portfolio_weights.items()}
    
    # Step 2: Determine share price for each stock on the day before buying
    day_before_buying_date = prices_df.index[prices_df.index.get_loc(buying_date) - 1]
    share_prices = prices_df.loc[day_before_buying_date]
    
    # Step 3: Calculate initial number of shares to buy for each stock
    initial_shares = {stock: custom_round(initial_investment[stock]/share_prices[stock]) for stock in portfolio_weights.keys()}
    
    # Step 4: Adjust for stocks that are too expensive
    affordable_stocks = {stock: shares for stock, shares in initial_shares.items() if shares >= 1}
    total_weight_of_affordable_stocks = sum([portfolio_weights[stock] for stock in affordable_stocks.keys()])
    adjusted_weights = {stock: portfolio_weights[stock] / total_weight_of_affordable_stocks for stock in affordable_stocks.keys()}
    adjusted_investment = {stock: adjusted_weights[stock] * total_investment for stock in affordable_stocks.keys()}
    
    # Step 5: Recalculate the number of shares to buy for each of the remaining stocks
    final_shares = {stock: custom_round(adjusted_investment[stock]/share_prices[stock]) for stock in affordable_stocks.keys()}
    
    # Collect the buying prices for the affordable stocks
    price_dict = {stock: share_prices[stock] for stock in affordable_stocks.keys()}
    
    # Calculate actual investment based on final shares and their buying prices
    actual_investment = sum([final_shares[stock] * price_dict[stock] for stock in final_shares.keys()])
    
    return final_shares, price_dict, actual_investment

def calculate_investment(portfolio_weights, stock_prices, buying_date, amount_available):

    buying_date = stock_prices[stock_prices.index <= buying_date].index[-1]

    buying_prices = stock_prices.loc[pd.to_datetime(buying_date) - pd.Timedelta(days=1)]

    portfolio = {}
    price_dict = {}
    actual_investment = 0

    # Initial Allocation
    for stock, weight in portfolio_weights.items():
        allocated_amount = amount_available * weight
        buying_price = buying_prices[stock]
        price_dict[stock] = buying_price
        num_shares = allocated_amount // buying_price
        portfolio[stock] = num_shares
        actual_investment += num_shares * buying_price

    # Adjustment logic for underinvestment
    if actual_investment < amount_available * 0.95:
        sorted_weights = sorted(portfolio_weights.items(), key=lambda x: x[1], reverse=True)
        for stock, weight in sorted_weights:
            while actual_investment < amount_available * 1.05:
                additional_share_cost = price_dict[stock]
                if actual_investment + additional_share_cost > amount_available * 1.05:
                    break
                portfolio[stock] += 1 
                actual_investment += additional_share_cost
    
    # Adjustment logic for overinvestment
    if actual_investment > amount_available * 1.05:
        sorted_weights = sorted(portfolio_weights.items(), key=lambda x: x[1], reverse=False)
        for stock, weight in sorted_weights:
                while actual_investment > amount_available * 0.95:
                        additional_share_cost = price_dict[stock]
                        if actual_investment - additional_share_cost < amount_available * 0.95:
                                break
                        portfolio[stock] -= 1
                        actual_investment -= additional_share_cost
    
    return portfolio, price_dict, actual_investment

def get_govt_bond_data():

    govt_bond_df = pd.read_csv('../data/India 10-Year Bond Yield Historical Data.csv')
    govt_bond_df = govt_bond_df[['Date','Price']]
    govt_bond_df.index = govt_bond_df['Date']
    govt_bond_df = govt_bond_df.drop('Date', axis=1)
    govt_bond_df.index = pd.to_datetime(govt_bond_df.index)

    return govt_bond_df

def get_all_stock_data(buying_date):

    all_stocks_df = pd.read_csv('../data/all_stock_data.csv', index_col=0)
    all_stocks_df.index = pd.to_datetime(all_stocks_df.index)
    all_stocks_df = all_stocks_df.sort_index()
    
    latest_date_available = str(all_stocks_df.index[-1])[:10]

    start_date = latest_date_available
    end_date = buying_date

    end_date_minus_one = end_date[:-2] + str(int(end_date[-2:])-1)
    end_date_minus_two = end_date[:-2] + str(int(end_date[-2:])-2)
    end_date_minus_three = end_date[:-2] + str(int(end_date[-2:])-3)

    # Convert string to datetime object
    date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    day = date_obj.weekday()
    print(start_date, end_date, day)

    if (day == 6) and (start_date == end_date_minus_two):
        all_stocks_df_final = all_stocks_df
    elif (day == 0) and (start_date == end_date_minus_three):
        all_stocks_df_final = all_stocks_df
    elif (start_date == end_date) or (start_date == end_date_minus_one):
        all_stocks_df_final = all_stocks_df
    else:
        generate_and_save_data(start_date, end_date)
        all_stocks_df_2 = pd.read_csv('../data/all_stock_data.csv', index_col=0)
        all_stocks_df_2.index = pd.to_datetime(all_stocks_df_2.index)
        all_stocks_df_2 = all_stocks_df_2.sort_index()
        all_stocks_df_2 = all_stocks_df_2.iloc[1:]
        all_stocks_df_final = pd.concat([all_stocks_df, all_stocks_df_2])
        all_stocks_df_final = all_stocks_df_final.drop_duplicates()
        all_stocks_df_final.to_csv('../data/all_stock_data.csv')

    return all_stocks_df

def get_recommendations(investment_value, strategy, buying_date, progress_callback=None):
    
    progress = 10

    buying_date = str(buying_date)[:10]

    if strategy == 'Strategy 1':
        stock_selection_strategy = 13
        weight_allocation_strategy = 7
        last_x_years = 0.5
        last_x_years_opt = 0.5
    
    elif strategy == 'Strategy 2':
        stock_selection_strategy = 10
        weight_allocation_strategy = 8
        last_x_years = 0.5
        last_x_years_opt = 1
    
    elif strategy == 'Strategy 3':
        stock_selection_strategy = 7
        weight_allocation_strategy = 3
        last_x_years = 0.25
        last_x_years_opt = 0.5
    
    elif strategy == 'Strategy 4':
        stock_selection_strategy = 13
        weight_allocation_strategy = 5
        last_x_years = 0.25
        last_x_years_opt = 0.5
    
    progress_callback(1, progress)

    filters = 4
    if stock_selection_strategy in [1,2,5,6,9,10,13,14]:
        holding_period = '1q'
    elif stock_selection_strategy in [3,4,7,8,11,12,15,16]:
        holding_period = '1m'

    if stock_selection_strategy in [1,3,5,7,9,11,13,15]:
        returns_type = 'SR'
    elif stock_selection_strategy in [2,4,6,8,10,12,14,16]:
        returns_type = 'LR'

    if stock_selection_strategy in [1,2,3,4]:
        max_non_positive_returns_count = 15
    elif stock_selection_strategy in [5,6,7,8]:
        max_non_positive_returns_count = 10
    elif stock_selection_strategy in [9,10,11,12]:
        max_non_positive_returns_count = None
        filters = 3
    elif stock_selection_strategy in [13,14,15,16]:
        max_non_positive_returns_count = None
        filters = 2

    progress_callback(2, progress)

    govt_bond_df = get_govt_bond_data()

    progress_callback(3, progress)

    all_stocks_df = get_all_stock_data(buying_date)
    all_stocks_df = all_stocks_df[~all_stocks_df.index.duplicated(keep='first')]

    progress_callback(4, progress)

    portfolio_weights, sell_date, best_method = stock_selection_weight_allocation(buying_date, holding_period, returns_type, max_non_positive_returns_count, weight_allocation_strategy, all_stocks_df, govt_bond_df, filters, last_x_years, last_x_years_opt)

    progress_callback(9, progress)
    
    portfolio_weights = adjust_portfolio(portfolio_weights)

    progress_callback(10, progress)

    # portfolio, price_dict, total_investment = calculate_investment(portfolio_weights, all_stocks_df, buying_date, investment_value)
    portfolio, price_dict, total_investment = calculate_shares_to_buy_with_prices(portfolio_weights, all_stocks_df, buying_date, investment_value)

    return portfolio, portfolio_weights, price_dict, sell_date, total_investment