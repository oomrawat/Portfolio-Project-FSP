import streamlit as st
from recommendations import get_recommendations, get_pie_chart_data, get_selected_strategies_results, get_density_plot_data
from datetime import date, timedelta
import random
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))
import plotly.graph_objs as go
import numpy as np
import scipy.stats as stats
import pandas as pd
from plotly.subplots import make_subplots

def show_results_chart():
    data = get_selected_strategies_results()
    data = data.set_index('Dates')

    fig = make_subplots(rows=1, cols=1, specs=[[{'type':'xy'}]])
    for column in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data[column], name=column, mode='lines+markers',
                                hoverinfo='x+y', line=dict(width=2)))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        width = 650,
        height = 500,
        margin=dict(t=1, b=0, l=0, r=0),
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor='center', yanchor='bottom')
    )

    # Update y-axis to display values as is with two decimal places
    fig.update_yaxes(tickformat=".2f")

    st.plotly_chart(fig)

def show_density_plot():
    data = get_density_plot_data()
    data = data.set_index(keys='Date')

    # Create subplots
    fig = make_subplots(rows=1, cols=1)

    # Create a KDE plot for each strategy within a specified x range
    x_range = np.linspace(-0.10, 0.20, 500)
    for column in data.columns:
        kde = stats.gaussian_kde(data[column])
        kde_values = kde(x_range)
        fig.add_trace(go.Scatter(
            x=x_range, y=kde_values,
            mode='lines', name=column,
            fill=None  # Fill area under the KDE curve
        ))

    # Adding a vertical dotted line for the NIFTY 50 average return
    nifty_50_avg_return = 0.0343  # Placeholder value for NIFTY 50 average return
    fig.add_trace(go.Scatter(
        x=[nifty_50_avg_return, nifty_50_avg_return], 
        y=[0, 14], 
        mode='lines', name='NIFTY 50 Average',
        line=dict(dash='dot')
    ))

    # Update layout for the figure
    fig.update_layout(
        xaxis_title='Monthly Returns',
        yaxis_title='Density',
        xaxis_range=[-0.05, 0.18],  # Set x-axis range
        width = 650,
        height = 500,
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(y=1, x=0.8, xanchor='left', yanchor='top'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )

    # Update y-axis to display values as is with two decimal places
    fig.update_yaxes(tickformat=".2f")

    # Show the plot in the streamlit app
    st.plotly_chart(fig)

def show_pie_chart(pf, portfolio_weights_adjusted):
    pf_in = get_pie_chart_data(portfolio_weights_adjusted)

    pastel_colors = [
        '#c4291c',
        '#8b8888',
        '#7b86c6',
        '#5db47d',
        '#4499df',
        '#4599df',
        '#397e49',
        '#832da4',
        '#e25d33',
        '#d98077',
        '#edc04c'
    ]

    # Get the unique industries and randomly select colors for them
    unique_industries = list(set(pf_in.values()))
    random_colors = random.sample(pastel_colors, len(unique_industries))
    industry_to_color = dict(zip(unique_industries, random_colors))

    # Create colors for the pie chart using 'pf_in'
    pie_colors = [industry_to_color[pf_in[symbol]] for symbol in portfolio_weights_adjusted.keys()]

    # Create labels for the pie chart to display symbols on the chart
    labels = []

    label1 = [symbol for symbol in portfolio_weights_adjusted.keys()]
    label2 = [pf[symbol]['No. of Shares'] for symbol in pf.keys()]
    for i in range(len(label1)):
        label = f"{label1[i]} ({label2[i]})"
        labels.append(label)

    # Create the hover text for each segment
    hover_texts = [
        f"{symbol}<br>Shares: {pf[symbol]['No. of Shares']}<br>Industry: {pf_in[symbol]}<br>Weightage: {portfolio_weights_adjusted[symbol]*100:.2f}%"
        for symbol in portfolio_weights_adjusted.keys()
    ]

    # Create the pie chart with custom hover text
    fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=list(portfolio_weights_adjusted.values()),
                        hoverinfo='text', text=hover_texts, textinfo='label', 
                        marker=dict(colors=pie_colors, line=dict(color='black', width=2)),
                        outsidetextfont=dict(color='white', size=15),
                        insidetextfont=dict(color='white', size=12)))

    # Update the layout to center the legend and set the text color to white
    fig.update_layout(
        legend_font_color='white',
        legend_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor='center', yanchor='bottom'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=10),
        margin=dict(t=1, b=0, l=0, r=0)  # Adjust margins as needed
    )

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)

def main():
    st.set_page_config(page_title="Strategic Wealth Management", layout="wide")

    st.title("Strategic Wealth Management: \n  ## A Quantitative Approach to Portfolio Selection and Time-Based Rebalancing")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""   
    **Disclaimer**: This application is part of a graduation project, and not meant to give investment ideas. For actual investment decisions, please consult a financial advisor.
    
    Please scroll down and share your feedback, comments, or any thoughts you have about the project or the app. Your input is highly valued. Thank you for visiting!
    """)

    tab1, tab2, tab3 = st.tabs(["Project Description", "Analysis and Results", "Get Recommendations"])
    
    with tab1:
        st.header("Project Description")
        st.markdown("""
        <br>

        #### **Motivation**:
        
        Modern investors want more than simply financial rewards; they also want empowerment, ownership, and the capacity to make data-driven decisions. In the exponentially growing Indian financial market, there are many investment options, which can be overwhelming for individual investors.
                    
        This project intends to help simplify investing for them with a structured approach. I am also motivated by the idea that historical data can greatly assist investment decisions. This project will use strategies that consider various statistical factors to make investment choices more organized. The goal is to provide individuals with the tools they need to make informed decisions in the dynamic Indian financial markets.  

        <br>            
        
        #### **Problem Statement**:
                    
        To create a novel approach to portfolio selection and time-based rebalancing to outperform market benchmark indices.  

        <br>        

        #### **Objectives**:
            
        -   Develop a historical data-driven investment strategy that focuses on analysing market indices and identifying a good combination of assets within those indices.
            
        -   Create a user-friendly app/interface that allows individual investors to choose their portfolios based on the strategy’s recommendations.
                    
        -   Evaluate the performance of the strategy through backtesting and historical data analysis, providing investors with insights into potential portfolio performance.  

        <br>       
                    
        #### **Understanding Our Investment Strategies**:
        
        Our web application employs a cutting-edge, data-driven approach for portfolio management in the dynamic Indian financial market, summarized as follows:
        
        -   Historical Data Analysis: We analyze past market data to identify patterns and assets that have historically outperformed, using this insight to inform future investment decisions.

        -   Stock Selection: Through statistical filters, we select stocks that demonstrate potential for growth and stability, tailoring selections to match individual risk appetites and investment goals.

        -   Weight Allocation: Utilizing both traditional and advanced methods, we optimize how your investment is spread across selected assets to balance risk and potential returns, based on Markowitz Portfolio Theory and beyond.

        -   Time-Based Rebalancing: Our strategies include regular portfolio adjustments to align with market changes and personal investment objectives, ensuring your investments stay on target.  

        <br>     
                    
        #### **User Journey**:
                    
        -   Read about the project.
            
        -   Go through the results and analysis of the strategies.
                    
        -   Read the [project report](https://drive.google.com/drive/u/0/folders/1tYmcImmnLgvzahalI1mrp0nQ98nEewQ-) if you want to delve deeper into the methodolody and analysis of the project.
            
        -   Choose one of the top strategies according to your risk-appetite.

        -   Choose a date, set an amount, and check the app's recommendations for you.  
                    
        <br>
                    
        #### **Risk Disclosure**:
        
        Investments involve risks including the possible loss of principal. Historical performance is not indicative of future results. Users should consider their financial situation, objectives, and risk tolerance before investing. The content provided here is for informational purposes only and should not be construed as financial advice.  

        """, unsafe_allow_html=True)        

    with tab2:
        st.header("Analysis and Results")
        st.markdown("""
        <br>
        
        This section of the application delivers a detailed examination of our investment strategy development process, which is underpinned by an extremely rigorous methodology. From an initial set of 880 unique strategies, we meticulously filtered down to the five most promising strategies through multiple stages of selection. These strategies were judged across a variety of parameters to ensure robustness and potential for success.
        
        <br>
                    
        #### **Testing and Evaluation Details**:
                    
        All the strategies were first backtested for a period of 4 years from 1st January 2020 to 1st January 2024. Although, this evaluation is slightly skewed due to presence of survivorship bias (more details in the [project report](https://drive.google.com/drive/u/0/folders/1tYmcImmnLgvzahalI1mrp0nQ98nEewQ-)).
        
        Regardless of a bias present in that evaluation, it is extremely useful for strategy selection and comparative analysis that lead us to these 5 selected strategies through various stages of selection.

        Post this, these 5 strategies were put to test during a live-testing phase from October 2023 to December 2023 wherein all possible portfolios that these strategies suggest on 59 market days were considered, and this was without a survivorship bias.
        
        Statistics and graphs showing the results of both of these testing processes can be found below.
        
        <br>            
        
        #### **Strategy 1 - Resilient Growth Strategist (S7-A7-T5)**:
                    
        With a formidable Compound Annual Growth Rate (CAGR) across several years and a high success rate in recent live testing, this strategy has emerged as a steadfast option for investors who seek growth coupled with resilience to market changes.

        <br>        

        #### **Strategy 2 - Steadfast Conservative (S5-A6-T5)**:
            
        Renowned for its unmatched success rate and minimal variance, the Steadfast Conservative strategy is crafted for investors who are risk-averse and desire stability and consistent performance.
                    
        <br>       
                    
        #### **Strategy 3 - Consistent Balanced (S5-A6-T7)**:
        
        With a solid track record of success and moderate returns, this strategy offers a balanced portfolio for investors seeking a dependable and measured approach to investing.
                    
        <br>     
                    
        #### **Strategy 4 - Emergent Opportunist (S3-A11-T3)**:
                    
        Targeting investors with a more aggressive risk appetite, this strategy stands out for its significant average monthly returns in recent testing, aligning with a philosophy of capitalizing on short-term market opportunities. 
                    
        <br>
                    
        #### **Strategy 5 - Dynamic Achiever (S3-A10-T3)**:
        
        The strategy's superior average monthly returns in the live test phase make it suitable for the assertive investor aiming for substantial growth through active market engagement.

        """, unsafe_allow_html=True)

        col1, spacer, col2 = st.columns([1, 0.1, 1])

        with col1:
            st.markdown("""
            <br>
                                    
            #### **Backtesting Results (January 2020 - January 2024)**:
                        
            """, unsafe_allow_html=True)

            show_results_chart()

        with spacer:
            st.write("")

        with col2:
            st.markdown("""
            <br>    
                                
            #### **Live-Testing Results Density Plot (Oct 2023 - Dec 2023)**:
                        
            """, unsafe_allow_html=True)

            show_density_plot()

        st.markdown("""     
        <br>
                    
        #### **Backtesting Statistics (January 2020 - January 2024)**:
                    
        """, unsafe_allow_html=True)
        
        current_dir = Path(__file__).resolve().parent
        csv_file = current_dir.parent / 'data' / 'backtesting_stats.csv'
        table_data = pd.read_csv(csv_file)

        html = table_data.to_html(index=False)
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("""
        <br>
                    
        #### **Live-Testing Statistics (October 2023 - December 2023)**:
                    
        """, unsafe_allow_html=True)

        current_dir = Path(__file__).resolve().parent
        csv_file = current_dir.parent / 'data' / 'livetesting_stats.csv'
        table_data = pd.read_csv(csv_file)

        html = table_data.to_html(index=False)
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("""
        <br>

        #### **NOTE**: More details about the strategy combination codes mentioned above and methodology behind the strategy formation can be found in the [project report](https://drive.google.com/drive/u/0/folders/1tYmcImmnLgvzahalI1mrp0nQ98nEewQ-).
        """, unsafe_allow_html=True)

    with tab3:
        st.header("Get Recommendations")

        # Row 1
        col1, col2 = st.columns([1, 1])

        with col1:
            strategy = st.selectbox(
                "Select Strategy",
                ['Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 4', 'Strategy 5'],
                key='strategy_selectbox',
                help='Learn about strategies in the "Analysis and Results" section before selecting.')
        
        with col2:
            st.markdown("\n")
            st.markdown("""
                            <style>
                            .custom-warning-1 {
                                background-color: #3e3c22;
                                color: #ffffc8;
                                padding: 7.5px;
                                border-radius: 8px;
                                text-align: center;
                                margin-top: 12px;
                            }
                            </style>
                            <div class="custom-warning-1">
                                Learn about strategies in the "Analysis and Results" section before selecting.
                            </div>
                            """, unsafe_allow_html=True)
                    
        # Row 2
        col1, col2 = st.columns([1, 1])

        with col1:
            investment_value = st.number_input(
                "Enter Investment Value (INR)",
                value=10000,
                step=1000,
                format="%d",
                key='investment_value_input',
                help="Enter a value greater than or equal to 10000."
            )

        with col2:
            investment_value_warning_placeholder = st.empty()

        # Row 3
        col1, col2 = st.columns([1, 1])

        with col1:
            buying_date = st.date_input("Select Buying Date", value=date.today(), min_value=date.today(), key='buying_date_input')

        with col2:
            if buying_date > date.today() + timedelta(days=1):
                st.markdown("""
                            <style>
                            .custom-warning-2 {
                                background-color: #5e0805;
                                color: #ffc8c8;
                                padding: 7.5px;
                                border-radius: 8px;
                                text-align: center;
                                margin-top: 28px;
                            }
                            </style>
                            <div class="custom-warning-2">
                                Warning: Choosing a future date may affect the accuracy of recommendations.
                            </div>
                            """, unsafe_allow_html=True)

        # Row 4 and beyond
        st.write("\n")

        button_clicked = st.button("Get Recommendations")
        
        if button_clicked:
            if investment_value >= 10000:
                try:
                    investment_value_warning_placeholder.clear()
                except:
                    pass
                
                with st.spinner(''):
                    spinner_status = st.empty()

                    spinner_status.write('Calculations started...')
                    
                    progress_bar = st.progress(0)

                    def progress_callback(current, total):
                        progress = int((current / total) * 100)
                        progress_bar.progress(progress)

                    portfolio, portfolio_weights, price_dict, sell_date, total_investment = get_recommendations(investment_value, strategy, buying_date, spinner_status, progress_callback=progress_callback)

                    pf = {}
                    portfolio_weights_adjusted = {}
                    for stock, shares in portfolio.items():
                        if shares > 0:
                            weight = round((shares*price_dict[stock])/total_investment,3)
                            pf[stock] = {'No. of Shares':shares, 'Buying Price': round(price_dict[stock],2), 'Weightage': weight}
                            portfolio_weights_adjusted[stock] = weight

                    spinner_status.write('Calculations Completed.')

                    st.markdown('<h1 style="font-size: 2em;">Recommended Portfolio:\n</h1>', unsafe_allow_html=True)
            
                    col1, col2 = st.columns([5, 7])

                    with col2:
                        st.write('')
                        show_pie_chart(pf, portfolio_weights_adjusted)

                    with col1:
                        for stock, stock_dict in pf.items():
                            st.write('')
                            no_of_shares = stock_dict['No. of Shares']
                            cmp = stock_dict['Buying Price']
                            st.markdown(f'<h1 style="font-size: 1.2em; font-weight: normal;">{stock}: Shares: {no_of_shares}, Current Market Price: ₹{cmp}</h1>', unsafe_allow_html=True)

                        st.markdown(f'<h1 style="font-size: 1.2em; font-weight: normal;">Rebalancing Date: {sell_date}</h1>', unsafe_allow_html=True)
                        st.markdown(f'<h1 style="font-size: 1.2em; font-weight: normal;">Total Investment Value: ₹{str(round(total_investment,2))}</h1>', unsafe_allow_html=True)
                        st.markdown('<h1 style="font-size: 1.2em; font-weight: normal;">NOTE: Higher the investment value, more accurate is the weight allocation. Recommended amount is INR 1,00,000.</h1>', unsafe_allow_html=True)

            else:
                investment_value_warning_placeholder.markdown("""
                            <style>
                            .custom-warning-3 {
                                background-color: #5e0805;
                                color: #ffc8c8;
                                padding: 7.5px;
                                border-radius: 8px;
                                text-align: center;
                                margin-top: 28px;
                            }
                            </style>
                            <div class="custom-warning-3">
                                Investment Value should be at least 10000 INR.
                            </div>
                            """, unsafe_allow_html=True)
        
    st.markdown("""
    <br>
                
    #### **Comments/Feedbacks/Thoughts**:
                
    Please drop your name and contact/email address with the message if you wish to be contacted back!
    """, unsafe_allow_html=True)

    feedback = st.text_area("", height=100, key='5')
    send_feedback = st.button("Send Message", key='6')

    if send_feedback:
        import smtplib
        import ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "oom.rawat@flame.edu.in"
        receiver_email = "oomrawat@gmail.com"

        abcd = 'vshq gwzh leti jbyj'

        message = MIMEMultipart("alternative")
        message["Subject"] = "New Feedback Received"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"Feedback received from the app:\n\n{feedback}"

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, abcd)
            server.sendmail(sender_email, receiver_email, message.as_string())
        
        st.success("Feedback sent successfully!")

    st.markdown("""
    <br>
                
    #### **Contact Information**:
                
    Oom Rawat  
    E-mail: oom.rawat@flame.edu.in or oomrawat@gmail.com  
    Mobile: +91 96388 82712
    
    """, unsafe_allow_html=True)
                
    st.markdown("""
    <footer style="width: 100%; text-align: center; font-size: large; padding: 10px 0;">
        Created by Oom Rawat
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()