import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the page configuration (must be first)
st.set_page_config(page_title="Dashboard", layout="wide")

# Load data from Excel
@st.cache
def load_data(file_path):
    excel_data = pd.ExcelFile(file_path)
    data = {sheet_name: excel_data.parse(sheet_name) for sheet_name in excel_data.sheet_names}
    return data

# Define the main app function
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    pages = {
        "Home": home_page,
        "Metric 1": lambda: detail_page("Metric 1"),
        "Metric 2": lambda: detail_page("Metric 2"),
        # Add more metrics as needed
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    pages[selection]()

# Home page
def home_page():
    st.title("Welcome to the Dashboard")
    st.subheader("Explore Metrics")
    
    # Display scorecards with clickable links
    cols = st.columns(2)  # Adjust column layout as needed
    with cols[0]:
        if st.button("Metric 1 Score"):
            detail_page("Metric 1")
    with cols[1]:
        if st.button("Metric 2 Score"):
            detail_page("Metric 2")
    # Add more scorecards as needed

# Detail page for a specific metric
def detail_page(metric_name):
    st.title(f"Details for {metric_name}")
    
    if metric_name in data:
        metric_data = data[metric_name]
        
        # Add filters
        st.sidebar.header("Filters")
        # Date range filter
        start_date = st.sidebar.date_input("Start Date", metric_data['Date'].min())
        end_date = st.sidebar.date_input("End Date", metric_data['Date'].max())
        
        # Filter data based on the date range
        filtered_data = metric_data[(metric_data['Date'] >= pd.Timestamp(start_date)) & 
                                    (metric_data['Date'] <= pd.Timestamp(end_date))]

        # Display filtered data
        st.write(filtered_data)

        # Add a line chart
        st.line_chart(filtered_data.set_index('Date')['Value'])

        # Add a bar chart
        st.bar_chart(filtered_data.set_index('Date')['Value'])

        # Add a custom Matplotlib plot
        plt.figure(figsize=(10, 5))
        plt.plot(filtered_data['Date'], filtered_data['Value'], marker='o', label='Value')
        plt.title(f"{metric_name} Over Time")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

    else:
        st.warning(f"No data available for {metric_name}")

# Entry point
if __name__ == "__main__":
    # Load Excel data
    data = load_data("dummy_metrics.xlsx")  # Replace with your file path
    main()
