##########################################################################
##########################################################################

# Importing required libraries, modules, etc.

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
import math
from calendar import monthrange
import numpy as np
import yfinance as yf
import weight_allocation_strategies as w_a_s

##########################################################################
##########################################################################

# Function 1: Extract and save stock data

def generate_and_save_data(start_date, end_date):
    """
    The function uses yahoo finance do download the stock data for all the stock symbols given in the file that's being pointed at using the file_path.
    It saves all the data as a csv file.

    Args:

        start_date (datetime.datetime): it is the start date from where the historical stock prices have to be saved

        end_date (datetime.datetime): it is the end date after which the historical stock prices need not be saved

    Returns:

        The function has no return values
    """
    try:
        # Load the CSV file to get the list of symbols
        file_path = '/Users/oomrawat/Desktop/04_FSP/FINC308 - Investment Analysis/Group Project/ind_niftytotalmarket_list.csv'  # Replace with your CSV file path
        df = pd.read_csv(file_path)

        # The symbols are in the third column
        symbols = list(df.iloc[:, 2].dropna().unique())  # Remove any NaN values and duplicates

        symbols_temp = []

        for symbol in symbols:
            symbols_temp.append(symbol + '.NS')

        print(symbols_temp, len(symbols_temp))

        symbols = symbols_temp
        symbols.remove('GATI.NS')
        symbols.append('ACLGATI.NS')
        symbols.remove('WELSPUNIND.NS')
        symbols.append('WELSPUNLIV.NS')

        # Function to fetch and return daily data for a given symbol
        def get_daily_data(symbol):

            data = yf.download(symbol, start_date, end_date, interval="1d")
            return data

        # Dictionary to hold data for all symbols
        all_data = {}

        # Loop through each symbol and fetch its weekly data
        for symbol in symbols:
            df = get_daily_data(symbol)
            all_data[symbol] = df

        close_columns = [df['Adj Close'] for df in all_data.values()]

        all_stocks_df = pd.DataFrame()
        all_stocks_df = pd.concat(close_columns, axis=1)
        column_names = []
        column_names += list(all_data.keys())
        all_stocks_df.columns = column_names

        all_stocks_df.index = pd.to_datetime(all_stocks_df.index)
        all_stocks_df = all_stocks_df.sort_index()

        all_stocks_df = all_stocks_df.backfill()
        all_stocks_df = all_stocks_df.drop_duplicates()
        all_stocks_df.dropna(axis=1)

        all_stocks_df.to_csv('../data/all_stock_data.csv')

        print(f"Stock data from the date {start_date} to the date {end_date} is succesfully downloaded and saved as 'all_stock_data.csv'.")

    except Exception as e:
        print(f"An error occurred: {e}")

##########################################################################
##########################################################################

# Function 2: To generate 3 month periods

def generate_three_month_periods(buying_date, holding_period):
    """
    The function takes buying_date and holding_period as arguments and returns three month periods and the selling date.
    It generates a list of all possible 3-month periods in the last 3 years before the buying date.
    Each period will be used for analysis. The function also calculates the selling date, which is 3 months from the buying date.
    
    Args:

        buying_date (string): it is a string in the format "yyyy-mm-dd"

        holding_period (string): it can be either '1q' or '1m'

    Returns:

        three_month_periods (list of tuples): it is a list of all 3 month periods in the last 3 years of the buying date that start from the 1st of a month

        selling_date (string): it is the selling date based on a calculation using the 'buying_date' and the 'holding_period'
    """
    if isinstance(buying_date, str):
        buying_date = datetime.strptime(buying_date, '%Y-%m-%d').date()

    if holding_period == '1m':
        selling_date = buying_date + relativedelta(months=1)
    elif holding_period == '1q':
        selling_date = buying_date + relativedelta(months=3)
    else:
        print("Incorrect Argument for 'holding_period'. Has to be either '1m' or '1q'")

    three_month_periods = []

    for month_back in range(34):
        start_date = buying_date - relativedelta(months=month_back+3)
        end_date = buying_date - relativedelta(months=month_back)
        three_month_periods.append((start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

    return three_month_periods, selling_date.strftime('%Y-%m-%d')

##########################################################################
##########################################################################

# Function 3: To generate 1 month periods

def generate_one_month_periods(buying_date, holding_period):
    """
    The function generates a list of custom period tuples and a selling date based on the buying date and holding period.
    Each period starts on the day of the buying date, and the same day +10, and +20 of each month in the last 3 years.
    The periods where either the start date or the end date is after the buying date are excluded.
    Non-existent dates like '2020-02-30' are included as per specification.

    Args:
        buying_date (string): Date of buying in the format "yyyy-mm-dd"
        holding_period (string): Holding period, either '1q' (3 months) or '1m' (1 month)

    Returns:
        one_month_periods (list of tuples): List of all custom periods within the last 3 years of the buying date
        selling_date (string): Calculated selling date based on the buying date and holding period
    """
    if isinstance(buying_date, str):
        buying_date = datetime.strptime(buying_date, '%Y-%m-%d').date()

    start_day = buying_date.day

    if holding_period == '1m':
        selling_date = buying_date + relativedelta(months=1)
    elif holding_period == '1q':
        selling_date = buying_date + relativedelta(months=3)
    else:
        print("Incorrect Argument for 'holding_period'. Has to be either '1m' or '1q'")
        return [], ''

    one_month_periods = []

    # Start from three years before the buying date
    start_period = buying_date - relativedelta(years=3)

    while start_period <= buying_date - relativedelta(months=1):
        for day_offset in [0, 10, 20]:
            day = start_day + day_offset
            potential_start_date = start_period.replace(day=1) + relativedelta(days=day - 1)
            end_date = potential_start_date + relativedelta(months=1)

            if potential_start_date >= buying_date or end_date > buying_date:
                # Skip periods starting or ending after the buying date
                continue

            one_month_periods.append((potential_start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        start_period = start_period + relativedelta(months=1)

    return one_month_periods, selling_date.strftime('%Y-%m-%d')

##########################################################################
##########################################################################

# Function 4: Get Closest Valid Date

def get_closest_valid_date(date_str):
    """
    The function takes a date in a string format and returns the same date if it's a valid calendar date or returns the closest date to that that is a valid calendar date.
    For example: 2024-02-30 will become 2024-02-29 or 2023-02-29 will become 2023-02-28

    Args:
        date_str (string): Date in the format "yyyy-mm-dd"
    
    Returns:
        closest_valid_date (string): Date in the format "yyyy-mm-dd" after conversion
    """
    # Split the date string into components
    year_str, month_str, day_str = date_str.split('-')
    year, month, day = int(year_str), int(month_str), int(day_str)
    
    # Find the last day of the given month and year
    last_day_of_month = monthrange(year, month)[1]
    
    # If the given day is out of range, adjust it to the last day of the month
    if day > last_day_of_month:
        day = last_day_of_month
    
    closest_valid_date = str(datetime(year, month, day))
    # Return the closest valid date
    return closest_valid_date

##########################################################################
##########################################################################

# Function 5: Stock selection for 3 month holding period strategies

def one_quarter_stock_selection(buying_date, holding_period, returns_type, max_non_positive_returns_count, all_stocks_df, filters, last_x_years):

    three_month_periods, selling_date = generate_three_month_periods(buying_date, holding_period)

    columns = ['Date Range'] + list(all_stocks_df.columns)
    returns_3_month_periods_df = pd.DataFrame(columns=columns)

    # Iterate over each date range
    for start_date, end_date in three_month_periods:
        # initialize a row with the date range
        row = {'Date Range': f'{start_date} to {end_date}'}

        # converting date to same type
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        nearest_start_date = all_stocks_df.index.asof(start_date)
        nearest_end_date = all_stocks_df.index.asof(end_date)
        
        # calculate return percentage for each stock symbol
        for stock in all_stocks_df.columns:

            initial_price = all_stocks_df.loc[nearest_start_date, stock]
            final_price = all_stocks_df.loc[nearest_end_date, stock]
            
            if returns_type == 'SR':
                return_percentage = ((final_price - initial_price) / initial_price) * 100
            elif returns_type == 'LR':
                return_percentage = np.log(final_price / initial_price) * 100
            else:
                print("Incorrect Argument for 'returns_type'. Has to be either 'SR' or 'LR'")
                break

            row[stock] = return_percentage
        
        # append the row to the new DataFrame
        returns_3_month_periods_df = returns_3_month_periods_df.append(row, ignore_index=True)
    
    if last_x_years == 1:
        buying_date_minus_1_year = str(int(buying_date[:4])-1)+buying_date[4:]

    elif last_x_years == 2:
        buying_date_minus_1_year = str(int(buying_date[:4])-2)+buying_date[4:]
    
    elif last_x_years == 0.5:
        year = buying_date[:4]
        month = buying_date[5:7]
        day = buying_date[8:10]
        if int(month) <= 6:
            year = str(int(year)-1)
            month = str(12+(int(month)-6))
        else:
            month = str(int(month)-6)
        if len(month) == 1:
                month = '0'+month
        buying_date_minus_1_year = year+'-'+month+'-'+day
    
    elif last_x_years == 0.25:
        year = buying_date[:4]
        month = buying_date[5:7]
        day = buying_date[8:10]
        if int(month) <= 3:
            year = str(int(year)-1)
            month = str(12+(int(month)-3))
        else:
            month = str(int(month)-3)
        if len(month) == 1:
                month = '0'+month
        buying_date_minus_1_year = year+'-'+month+'-'+day

    try:
        last_1_year_stock_df = all_stocks_df[(all_stocks_df.index >= buying_date_minus_1_year) & (all_stocks_df.index < buying_date)]
    except:
        buying_date_minus_1_year = get_closest_valid_date(buying_date_minus_1_year)[:10]
        last_1_year_stock_df = all_stocks_df[(all_stocks_df.index >= buying_date_minus_1_year) & (all_stocks_df.index < buying_date)]

    # Initialize a list to store the data for the new DataFrame
    data = []

    # Iterate through each stock symbol in new_df's columns (except the 'Date Range' column)
    for stock in returns_3_month_periods_df.columns[1:]:
        # Get the series of returns for this stock
        returns = returns_3_month_periods_df[stock]

        # Calculate the number of positive and non-positive returns
        positive_returns_count = (returns > 0).sum()
        non_positive_returns_count = (returns <= 0).sum()

        # Calculate the standard deviation and average of the returns
        std_dev_returns = returns.std()
        avg_returns = returns.mean()

        # Get the last x years rows for the stock
        if last_x_years == 2:
            last_13_returns = returns_3_month_periods_df[stock].head(22)
        
        elif last_x_years == 1:
            last_13_returns = returns_3_month_periods_df[stock].head(10)

        elif last_x_years == 0.5:
            last_13_returns = returns_3_month_periods_df[stock].head(4)

        elif last_x_years == 0.25:
            last_13_returns = returns_3_month_periods_df[stock].head(1)

        # Calculate the stats for the last 13 periods
        positive_last_13_count = (last_13_returns > 0).sum()
        non_positive_last_13_count = (last_13_returns <= 0).sum()
        std_dev_last_13 = last_13_returns.std()
        avg_last_13 = last_13_returns.mean()

        daily_avg_ret_all_time = all_stocks_df.pct_change().iloc[1:].mean()[stock]

        daily_avg_ret_last_1_year = last_1_year_stock_df.pct_change().iloc[1:].mean()[stock]

        # Append the calculated values to the data list
        data.append([stock, daily_avg_ret_all_time, positive_returns_count, non_positive_returns_count, std_dev_returns, avg_returns, 
                    daily_avg_ret_last_1_year, positive_last_13_count, non_positive_last_13_count, std_dev_last_13, avg_last_13])

    # Create a new DataFrame with the calculated data
    stock_analysis_df = pd.DataFrame(data, columns=['Stock Symbol', 'Daily Average Returns All Time', 'Positive Returns Count', 'Non-Positive Returns Count', 
                                            'Std Dev Returns', 'Average Returns All 3MP', 'Daily Average Returns Last X Year', 'Positive Last X Years Count', 
                                            'Non-Positive Last X Years Count', 'Std Dev Last X Years', 'Average Last X Years 3MP'])

    filter_1 = stock_analysis_df[stock_analysis_df['Daily Average Returns All Time'] > 0]

    filter_2 = filter_1[filter_1['Daily Average Returns Last X Year'] > 0]

    # for strategy 1,2,3,4,5,6,7,8

    if filters == 4:

        filter_3 = filter_2[(filter_2['Non-Positive Last X Years Count']==0)]

        filter_4 = filter_3[(filter_3['Non-Positive Returns Count'] <= max_non_positive_returns_count)]

        if len(filter_4) < 5 or len(filter_4) > 30:

            filter_4 = filter_3.sort_values(by='Non-Positive Returns Count').iloc[:30]

            if len(filter_4) < 5:

                filter_4 = filter_2.sort_values(by='Non-Positive Last X Years Count').iloc[:30]
        
        selected_stocks = list(filter_4['Stock Symbol'])

    # for strategy 9,10,11,12
    
    elif filters == 3:

        filter_3 = filter_2[(filter_2['Non-Positive Last X Years Count']==0)]

        if len(filter_3) < 5 or len(filter_3) > 30:

            filter_3 = filter_2.sort_values(by='Non-Positive Last X Years Count').iloc[:30]

        selected_stocks = list(filter_3['Stock Symbol'])

    # for strategy 13,14,15,16
        
    elif filters == 2:

        filtered_stocks = []
        i = 0
        while len(filtered_stocks) < 50:
            filter_1 = stock_analysis_df[stock_analysis_df['Non-Positive Last X Years Count']<=i]
            filtered_stocks = list(filter_1['Stock Symbol'])
            i += 1
        
        filter_2 = filter_1.sort_values(by='Daily Average Returns Last X Year', ascending=False).iloc[:30]

        selected_stocks = list(filter_2['Stock Symbol'])
    
    return selected_stocks, selling_date

##########################################################################
##########################################################################

# Function 6: Stock selection for 1 month holding period strategies

def one_month_stock_selection(buying_date, holding_period, returns_type, max_non_positive_returns_count, all_stocks_df, filters, last_x_years):

    one_month_periods, selling_date = generate_one_month_periods(buying_date, holding_period)

    if max_non_positive_returns_count != None:
        max_non_positive_returns_count = round((max_non_positive_returns_count/34)*106)

    columns = ['Date Range'] + list(all_stocks_df.columns)
    returns_3_month_periods_df = pd.DataFrame(columns=columns)

    # Iterate over each date range
    for start_date, end_date in one_month_periods:
        # initialize a row with the date range
        row = {'Date Range': f'{start_date} to {end_date}'}

        # converting date to same type
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        nearest_start_date = all_stocks_df.index.asof(start_date)
        nearest_end_date = all_stocks_df.index.asof(end_date)
        
        # calculate return percentage for each stock symbol
        for stock in all_stocks_df.columns:

            initial_price = all_stocks_df.loc[nearest_start_date, stock]
            final_price = all_stocks_df.loc[nearest_end_date, stock]
            
            if returns_type == 'SR':
                return_percentage = ((final_price - initial_price) / initial_price) * 100
            elif returns_type == 'LR':
                return_percentage = np.log(final_price / initial_price) * 100
            else:
                print("Incorrect Argument for 'returns_type'. Has to be either 'SR' or 'LR'")
                break

            row[stock] = return_percentage
        
        # append the row to the new DataFrame
        returns_3_month_periods_df = returns_3_month_periods_df.append(row, ignore_index=True)
    
    if last_x_years == 1:
        buying_date_minus_1_year = str(int(buying_date[:4])-1)+buying_date[4:]
       
    elif last_x_years == 2:
        buying_date_minus_1_year = str(int(buying_date[:4])-2)+buying_date[4:]
    
    elif last_x_years == 0.5:
        year = buying_date[:4]
        month = buying_date[5:7]
        day = buying_date[8:10]
        if int(month) <= 6:
            year = str(int(year)-1)
            month = str(12+(int(month)-6))
        else:
            month = str(int(month)-6)
        if len(month) == 1:
                month = '0'+month
        buying_date_minus_1_year = year+'-'+month+'-'+day
    
    elif last_x_years == 0.25:
        year = buying_date[:4]
        month = buying_date[5:7]
        day = buying_date[8:10]
        if int(month) <= 3:
            year = str(int(year)-1)
            month = str(12+(int(month)-3))
        else:
            month = str(int(month)-3)
        if len(month) == 1:
                month = '0'+month
        buying_date_minus_1_year = year+'-'+month+'-'+day

    last_1_year_stock_df = all_stocks_df[(all_stocks_df.index >= buying_date_minus_1_year) & (all_stocks_df.index < buying_date)]

    # Initialize a list to store the data for the new DataFrame
    data = []

    # Iterate through each stock symbol in new_df's columns (except the 'Date Range' column)
    for stock in returns_3_month_periods_df.columns[1:]:
        # Get the series of returns for this stock
        returns = returns_3_month_periods_df[stock]

        # Calculate the number of positive and non-positive returns
        positive_returns_count = (returns > 0).sum()
        non_positive_returns_count = (returns <= 0).sum()

        # Calculate the standard deviation and average of the returns
        std_dev_returns = returns.std()
        avg_returns = returns.mean()

        # Get the last x years rows for the stock
        if last_x_years == 2:
            last_13_returns = returns_3_month_periods_df[stock].tail(70)
        
        elif last_x_years == 1:
            last_13_returns = returns_3_month_periods_df[stock].tail(34)

        elif last_x_years == 0.5:
            last_13_returns = returns_3_month_periods_df[stock].tail(16)

        elif last_x_years == 0.25:
            last_13_returns = returns_3_month_periods_df[stock].tail(7)

        # Calculate the stats for the last 13 periods
        positive_last_13_count = (last_13_returns > 0).sum()
        non_positive_last_13_count = (last_13_returns <= 0).sum()
        std_dev_last_13 = last_13_returns.std()
        avg_last_13 = last_13_returns.mean()

        daily_avg_ret_all_time = all_stocks_df.pct_change().iloc[1:].mean()[stock]

        daily_avg_ret_last_1_year = last_1_year_stock_df.pct_change().iloc[1:].mean()[stock]

        # Append the calculated values to the data list
        data.append([stock, daily_avg_ret_all_time, positive_returns_count, non_positive_returns_count, std_dev_returns, avg_returns, 
                    daily_avg_ret_last_1_year, positive_last_13_count, non_positive_last_13_count, std_dev_last_13, avg_last_13])

    # Create a new DataFrame with the calculated data
    stock_analysis_df = pd.DataFrame(data, columns=['Stock Symbol', 'Daily Average Returns All Time', 'Positive Returns Count', 'Non-Positive Returns Count', 
                                            'Std Dev Returns', 'Average Returns All 3MP', 'Daily Average Returns Last X Year', 'Positive Last X Years Count', 
                                            'Non-Positive Last X Years Count', 'Std Dev Last X Years', 'Average Last X Years 3MP'])

    filter_1 = stock_analysis_df[stock_analysis_df['Daily Average Returns All Time'] > 0]
    
    filter_2 = filter_1[filter_1['Daily Average Returns Last X Year'] > 0]

    # for strategy 1,2,3,4,5,6,7,8

    if filters == 4:

        filter_3 = filter_2[(filter_2['Non-Positive Last X Years Count']==0)]

        filter_4 = filter_3[(filter_3['Non-Positive Returns Count'] <= max_non_positive_returns_count)]

        if len(filter_4) < 5 or len(filter_4) > 30:

            filter_4 = filter_3.sort_values(by='Non-Positive Returns Count').iloc[:30]

            if len(filter_4) < 5:

                filter_4 = filter_2.sort_values(by='Non-Positive Last X Years Count').iloc[:30]
        
        selected_stocks = list(filter_4['Stock Symbol'])

    # for strategy 9,10,11,12
    
    elif filters == 3:

        filter_3 = filter_2[(filter_2['Non-Positive Last X Years Count']==0)]

        if len(filter_3) < 5 or len(filter_3) > 30:

            filter_3 = filter_2.sort_values(by='Non-Positive Last X Years Count').iloc[:30]

        selected_stocks = list(filter_3['Stock Symbol'])

    # for strategy 13,14,15,16
        
    elif filters == 2:

        filtered_stocks = []
        i = 0
        while len(filtered_stocks) < 50:
            filter_1 = stock_analysis_df[stock_analysis_df['Non-Positive Last X Years Count']<=i]
            filtered_stocks = list(filter_1['Stock Symbol'])
            i += 1
        
        filter_2 = filter_1.sort_values(by='Daily Average Returns Last X Year', ascending=False).iloc[:30]

        selected_stocks = list(filter_2['Stock Symbol'])
    
    return selected_stocks, selling_date

##########################################################################
##########################################################################
    
# Function 7: Filtering the stocks according to the strategy and calling the appropriate weight allocation strategy

def stock_selection_weight_allocation(buying_date, holding_period, returns_type, max_non_positive_returns_count, weight_allocation_strategy, all_stocks_df, govt_bond_df, filters, last_x_years, last_x_years_opt):
    '''
    The function takes all the below given arguments to filter and select stocks based on the defined rules in strategies.txt and calls the appropriate weight allocation strtegy function and returns the final portfolio.

    Args:

        buying_date (string): it is a string of the buying date in the format 'yyyy-mm-dd'

        holding_period (string): it can be either '1q' (1 quarter) or '1m' (1 month)

        returns_type (string): it can be either 'LR' (log returns) or 'SR' (simple returns)

        max_non_positive_returns_count (integer): it can be any number between 0 and 34 but from the ideas thought of so far it can either be 15 or 10
    
        weight_allocation_strategy (integer): it can be anything from the 7 weight allocation strategies thought of so far (s1, s2, s3, s4, s5, s6, or s7)

        all_stocks_df (pandas dataframe): it is the pandas dataframe of all the historical stock prices for the dates used while generating the dataframe

        govt_bond_df (pandas dataframe): it is the pandas dataframe of government bond data that will be use further in some of the weight allocation strategies

        filters (integer): it is the number of filters to be applied and for now it can either be 3 or 4

    Returns:

        portfolio (dictionary of string:float type): a dictionary of symbols chosen as the keys and their weightages as the values

        selling_date (string): date on which the portfolio should be sold according to the strategy

        best_method (string): it is the best method out of the 3 different optimization algorthims that the weight allocation strategies are using just for analysis
    '''
    if holding_period == '1q':
        selected_stocks, selling_date = one_quarter_stock_selection(buying_date, holding_period, returns_type, max_non_positive_returns_count, all_stocks_df, filters, last_x_years)
    elif holding_period == '1m':
        selected_stocks, selling_date = one_month_stock_selection(buying_date, holding_period, returns_type, max_non_positive_returns_count, all_stocks_df, filters, last_x_years)

    if last_x_years_opt == 1:
        buying_date_minus_x_year = str(int(buying_date[:4])-1)+buying_date[4:]

    elif last_x_years_opt == 2:
        buying_date_minus_x_year = str(int(buying_date[:4])-2)+buying_date[4:]

    elif last_x_years_opt == 0.5:
        year = buying_date[:4]
        month = buying_date[5:7]
        day = buying_date[8:10]
        if int(month) <= 6:
            year = str(int(year)-1)
            month = str(12+(int(month)-6))
        else:
            month = str(int(month)-6)
        if len(month) == 1:
            month = '0'+month
        buying_date_minus_x_year = year+'-'+month+'-'+day
    
    elif last_x_years_opt == 0.25:
        year = buying_date[:4]
        month = buying_date[5:7]
        day = buying_date[8:10]
        if int(month) <= 3:
            year = str(int(year)-1)
            month = str(12+(int(month)-3))
        else:
            month = str(int(month)-3)
        if len(month) == 1:
            month = '0'+month
        buying_date_minus_x_year = year+'-'+month+'-'+day

    buying_date_minus_x_year = get_closest_valid_date(buying_date_minus_x_year)[:10]

    portfolio, best_method = prep_call_weight_allocation_strategy(returns_type, buying_date_minus_x_year, buying_date, selected_stocks, weight_allocation_strategy, all_stocks_df, govt_bond_df)

    return portfolio, selling_date, best_method

##########################################################################
##########################################################################
    
# Function 8: Preperation for Weight Allocation

def prep_call_weight_allocation_strategy(returns_type, buying_date_minus_x_year, buying_date, selected_stocks, strategy_number, all_stocks_df, govt_bond_df):
    '''
    The function takes all the below described arguments and calls the chosen weight allocation strategy function to return the final portfolio and the best algorithm for optimization

    Args:

        returns_type (string): it can be either 'LR' (log returns) or 'SR' (simple returns)

        buying_date (string): it is a string of the buying date in the format 'yyyy-mm-dd'
    
        buying_date_minus_1_year (string): it is a string of the one year before the buying date in the format 'yyyy-mm-dd'
    
        selected_stocks (list): list of stocks selected based on the stock selection strategy chosen
    
        strategy_number (integer): strategy number for the weight allocation strategy
    
        all_stocks_df (pandas dataframe): it is the pandas dataframe of all the historical stock prices for the dates used while generating the dataframe

        govt_bond_df (pandas dataframe): it is the pandas dataframe of government bond data that will be use further in some of the weight allocation strategies
    
    Returns:

        portfolio (dictionary of string:float type): a dictionary of symbols chosen as the keys and their weightages as the values

        best_method (string): it is the best method out of the 3 different optimization algorthims that the weight allocation strategies are using just for analysis
    '''
    if len(selected_stocks) > 0:

        if strategy_number == 1:
            portfolio, best_method = w_a_s.weight_allocation_1(selected_stocks)

        elif strategy_number == 2:
            portfolio, best_method = w_a_s.weight_allocation_2(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date)
        
        elif strategy_number == 3:
            portfolio, best_method = w_a_s.weight_allocation_3(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date)
        
        elif strategy_number == 4:
            portfolio, best_method = w_a_s.weight_allocation_4(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date, govt_bond_df)
        
        elif strategy_number == 5:
            portfolio, best_method = w_a_s.weight_allocation_5(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date, govt_bond_df)
        
        elif strategy_number == 6:
            portfolio, best_method = w_a_s.weight_allocation_6(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date)
        
        elif strategy_number == 7:
            portfolio, best_method = w_a_s.weight_allocation_7(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date)
        
        elif strategy_number == 8:
            portfolio, best_method = w_a_s.weight_allocation_8(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date, govt_bond_df)
        
        elif strategy_number == 9:
            portfolio, best_method = w_a_s.weight_allocation_9(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date, govt_bond_df)

        elif strategy_number == 10:
            portfolio, best_method = w_a_s.weight_allocation_10(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date, govt_bond_df)

        elif strategy_number == 11:
            portfolio, best_method = w_a_s.weight_allocation_11(selected_stocks, all_stocks_df, returns_type, buying_date_minus_x_year, buying_date, govt_bond_df)

        return portfolio, best_method
    
    else:

        return None, None

##########################################################################
##########################################################################
    
# Function 9: Function to adjust weights of a portfolio

def adjust_portfolio(portfolio):
    """
    Adjusts the weights of the stocks in the portfolio so that they sum up to 1, 
    while maintaining the same proportion. Stocks with a weight less than 0.01 are removed.

    Args:
        portfolio (dict): A dictionary with stock symbols as keys and weights as values.

    Returns:
        dict: Adjusted portfolio with weights summing up to 1.
    """
    # Remove stocks with weight less than 0.01
    filtered_portfolio = {stock: weight for stock, weight in portfolio.items() if weight >= 0.01}

    # Calculate the sum of the remaining weights
    total_weight = sum(filtered_portfolio.values())

    # Adjust the weights to sum up to 1
    adjusted_portfolio = {stock: weight / total_weight for stock, weight in filtered_portfolio.items()}

    return adjusted_portfolio