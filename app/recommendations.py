import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))
from functions import stock_selection_weight_allocation_appversion, adjust_portfolio, generate_and_save_data, calculate_shares_to_buy_with_prices
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import math

def get_pie_chart_data(pf):
    current_dir = Path(__file__).resolve().parent
    csv_file = current_dir.parent / 'data' / 'ind_niftytotalmarket_list.csv'
    df = pd.read_csv(csv_file)
    pf_industry = {}
    for stock, weight in pf.items():
        symbol = stock[:-3]
        industry = df[df['Symbol']==symbol]['Industry'].iloc[0]
        pf_industry[stock] = industry
    
    total_weight = sum(pf.values())
    
    return pf_industry

def get_govt_bond_data():

    current_dir = Path(__file__).resolve().parent
    csv_file = current_dir.parent / 'data' / 'India 10-Year Bond Yield Historical Data.csv'
    govt_bond_df = pd.read_csv(csv_file)

    govt_bond_df = govt_bond_df[['Date','Price']]
    govt_bond_df.index = govt_bond_df['Date']
    govt_bond_df = govt_bond_df.drop('Date', axis=1)
    govt_bond_df.index = pd.to_datetime(govt_bond_df.index)

    return govt_bond_df

def get_all_stock_data(buying_date):

    current_dir = Path(__file__).resolve().parent
    csv_file = current_dir.parent / 'data' / 'all_stock_data.csv'

    all_stocks_df = pd.read_csv(csv_file, index_col=0)
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
        all_stocks_df_2 = pd.read_csv(csv_file, index_col=0)
        all_stocks_df_2.index = pd.to_datetime(all_stocks_df_2.index)
        all_stocks_df_2 = all_stocks_df_2.sort_index()
        all_stocks_df_2 = all_stocks_df_2.iloc[1:]
        all_stocks_df_final = pd.concat([all_stocks_df, all_stocks_df_2])
        all_stocks_df_final = all_stocks_df_final.drop_duplicates()
        all_stocks_df_final.to_csv(csv_file)

    return all_stocks_df

def get_recommendations(investment_value, strategy, buying_date, spinner_status, progress_callback=None):
    
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

    spinner_status.write('Fetching Data...')

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

    spinner_status.write('This will take a while please be patient...')

    progress_callback(2, progress)

    govt_bond_df = get_govt_bond_data()

    progress_callback(3, progress)

    all_stocks_df = get_all_stock_data(buying_date)
    all_stocks_df = all_stocks_df[~all_stocks_df.index.duplicated(keep='first')]

    progress_callback(4, progress)

    portfolio_weights, sell_date, best_method = stock_selection_weight_allocation_appversion(buying_date, holding_period, returns_type, max_non_positive_returns_count, weight_allocation_strategy, all_stocks_df, govt_bond_df, filters, last_x_years, last_x_years_opt, spinner_status, progress_callback=progress_callback)

    progress_callback(9, progress)
    
    portfolio_weights = adjust_portfolio(portfolio_weights)

    progress_callback(10, progress)

    adjusted_buy_date = all_stocks_df[all_stocks_df.index <= buying_date].index[-1]

    portfolio, price_dict, total_investment = calculate_shares_to_buy_with_prices(portfolio_weights, all_stocks_df, adjusted_buy_date, investment_value, strictly_lower=False)

    return portfolio, portfolio_weights, price_dict, sell_date, total_investment