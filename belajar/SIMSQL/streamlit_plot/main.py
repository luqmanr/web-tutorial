import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('BORMA SALES DATA')

df = pd.read_csv('./data/dago.csv')
st.dataframe(df)

plt.figure(figsize=(10, 5))
sns.lineplot(x='tanggal', y='sales', data=df, marker='o', markersize=20)

# Set plot labels and title
plt.xlabel('Tanggal')
plt.ylabel('Sales')
plt.title('Sales for All Stores (Grouped by Date)')
plt.xticks(rotation=0, ha='right')  # Rotate x-axis labels
plt.legend(title='Store')  # Add a legend with a title
plt.tight_layout()
st.pyplot(plt)

# data_source = st.radio("Select data source:", ("Sample Data", "Upload CSV"))

# if data_source == "Sample Data":
#     df = generate_sample_data()
#     st.write("Using sample data:")
#     st.dataframe(df)
# else:
#     uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
#     if uploaded_file is not None:
#         try:
#             df = pd.read_csv(uploaded_file, parse_dates=['time'])
#             st.write("Uploaded data:")
#             st.dataframe(df)

#         except Exception as e:
#             st.error(f"Error reading CSV: {e}")
#             return
#     else:
#         st.info("Please upload a CSV file.")
#         return

# if 'time' in df.columns:
#         try:
#             df['time'] = pd.to_datetime(df['time'])
#         except:
#             st.error("Error: 'time' column must be convertible to datetime.")
#             return
# else:
#     st.error("Error: CSV must contain a 'time' column.")
#     return

# if 'value' in df.columns:
#     try:
#         df['value'] = pd.to_numeric(df['value'])
#     except:
#         st.error("Error: 'value' column must be numeric.")
#         return
# else:
#     st.error("Error: CSV must contain a 'value' column.")
#     return

# fig = create_seaborn_line_plot(df)
# st.pyplot(fig)
