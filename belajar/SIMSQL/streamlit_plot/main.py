import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

def generate_sample_data():
    """Generates sample time series data."""
    data = {
        'time': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07']),
        'value': [10, 12, 9, 15, 13, 18, 16]
    }
    return pd.DataFrame(data)

def create_seaborn_line_plot(df):
    """Creates a line plot of the time series data using seaborn."""
    fig, ax = plt.subplots()
    sns.lineplot(x='time', y='value', data=df, ax=ax)
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Time Series Line Plot (Seaborn)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def main():
    st.title('Time Series Line Plot (Seaborn)')

    data_source = st.radio("Select data source:", ("Sample Data", "Upload CSV"))

    if data_source == "Sample Data":
        df = generate_sample_data()
        st.write("Using sample data:")
        st.dataframe(df)
    else:
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, parse_dates=['time'])
                st.write("Uploaded data:")
                st.dataframe(df)

            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                return
        else:
            st.info("Please upload a CSV file.")
            return

    if 'time' in df.columns:
         try:
             df['time'] = pd.to_datetime(df['time'])
         except:
             st.error("Error: 'time' column must be convertible to datetime.")
             return
    else:
        st.error("Error: CSV must contain a 'time' column.")
        return

    if 'value' in df.columns:
        try:
            df['value'] = pd.to_numeric(df['value'])
        except:
            st.error("Error: 'value' column must be numeric.")
            return
    else:
        st.error("Error: CSV must contain a 'value' column.")
        return

    fig = create_seaborn_line_plot(df)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
