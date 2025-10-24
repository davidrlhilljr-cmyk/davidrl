# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

# Load CSV
csv_data = pd.DataFrame()
if os.path.exists("data.csv"):
    try:
        csv_data = pd.read_csv("data.csv")
        st.success("CSV data loaded successfully.")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
else:
    st.warning("CSV file not found.")

# Load JSON
json_data = {}
if os.path.exists("data.json"):
    try:
        with open("data.json") as f:
            json_data = json.load(f)
        st.success("JSON data loaded successfully.")
    except Exception as e:
        st.error(f"Error loading JSON: {e}")
else:
    st.warning("JSON file not found.")



st.success("All data sources are ready for visualization!")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Frequency of Reported Topics") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.

if not csv_data.empty:
    activity_counts = csv_data["category"].value_counts()
    st.bar_chart(activity_counts)
    st.caption("This bar chart shows how often each topic or category was reported in the survey.")
else:
    st.warning("CSV data is empty or missing.")



# GRAPH 2: DYNAMIC GRAPH
if "filter_keyword" not in st.session_state:
    st.session_state.filter_keyword = ""
    
st.subheader(f"Graph 2: Total Values for Entries Matching '{st.session_state.filter_keyword}'") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.



#NEW: Text input for filtering

st.text_input("Enter a keyword to filter entries (e.g., 'Sleep', 'Study', 'Food'):", key="filter_keyword")  #NEW

filtered_csv = csv_data[
    csv_data["category"].astype(str).str.contains(st.session_state.filter_keyword, case=False, na=False)
]

if not filtered_csv.empty:
    filtered_csv["value"] = pd.to_numeric(filtered_csv["value"], errors="coerce")  # Convert safely
    filtered_values = filtered_csv.groupby("category")["value"].sum()
    st.line_chart(filtered_values)  #NEW
    st.caption(f"This line chart shows the total values for categories that include the keyword '{st.session_state.filter_keyword}'.")
else:
    st.warning("No matching categories found.")




# GRAPH 3: DYNAMIC GRAPH
if "usage_threshold" not in st.session_state:
        st.session_state.usage_threshold = 2.0
st.subheader(f"Graph 3: Data Points Above Threshold of {st.session_state.usage_threshold}") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

if json_data:
    json_df = pd.DataFrame(json_data["data_points"])

    #NEW: Slider for threshold

    st.slider("Highlight entries with values above:", 0.0, 5.0, 2.0, key="usage_threshold")  #NEW  #NEW
    highlight_df = json_df[json_df["value"] > st.session_state.usage_threshold]

    fig, ax = plt.subplots()
    ax.scatter(highlight_df["label"], highlight_df["value"], color="orange")
    ax.set_xlabel("Category or Day")
    ax.set_ylabel("Reported Value")
    ax.set_title("Reported Values Above Threshold")
    st.pyplot(fig)
    st.caption(f"This scatter plot shows data points where the value exceeds {st.session_state.usage_threshold}.")
else:
    st.warning("JSON data is missing or invalid.")



