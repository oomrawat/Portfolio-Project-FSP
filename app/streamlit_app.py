import streamlit as st
from recommendations import get_recommendations, get_pie_chart_data
from datetime import date, timedelta
import random
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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
    st.set_page_config(page_title="Portfolio Selection and Rebalancing Project", layout="wide")

    st.title("Portfolio Selection and Rebalancing Project")
    st.markdown("""
    **Disclaimer**: This application is part of a student project. It uses simulated data for investment recommendations. For actual investment decisions, please consult a financial advisor.
    """)

    tab1, tab2, tab3 = st.tabs(["Project Description", "Analysis and Backtesting Results", "Get Recommendations"])
    
    with tab1:
        st.header("Project Description")
        st.markdown("""
        **Objective**: 
                    
        **Features**:

        **Implementation Steps**:

        **Outcome**:

        """)

    with tab2:
        st.header("Analysis and Backtesting Results")
        st.markdown("This section can be used to present the analysis...")
        # st.image('image2.jpg', caption="Sample Image for Analysis Results")

    with tab3:
        st.header("Get Recommendations")

        # Row 1
        col1, col2 = st.columns([1, 1])

        with col1:
            strategy = st.selectbox(
                "Select Strategy",
                ['Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 4'],
                key='strategy_selectbox',
                help='Learn about strategies in the "Analysis and Backtesting Results" section before selecting.')
        
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
                                Learn about strategies in the "Analysis and Backtesting Results" section before selecting.
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
    <footer style="position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: large;">
        Created by Oom Rawat
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()