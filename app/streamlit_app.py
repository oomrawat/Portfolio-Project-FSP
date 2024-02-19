import streamlit as st
from recommendations import get_recommendations
from datetime import date, timedelta

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

                with st.spinner('Calculating recommendations...'):
                    progress_bar = st.progress(0)
                    def progress_callback(current, total):
                        progress = int((current / total) * 100)
                        progress_bar.progress(progress)

                    portfolio, portfolio_weights, price_dict, sell_date, total_investment = get_recommendations(investment_value, strategy, buying_date, progress_callback=progress_callback)

                    pf = {}
                    for stock, shares in portfolio.items():
                        if shares > 0:
                            weight = round((shares*price_dict[stock])/total_investment,3)
                            pf[stock] = {'No. of Shares':shares, 'Buying Price': round(price_dict[stock],2), 'Recommended Weightage': round(portfolio_weights[stock],4), 'Actual Weightage': weight}

                    st.write('Recommended Portfolio:\n', pf)
                    st.write('Rebalancing Date:', sell_date)
                    st.write('Total Investment Value:', str(round(total_investment,2)))
                    st.write('NOTE: Higher the investment value, more accurate is the weight allocation. Recommended amount is INR 1,00,000.')

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