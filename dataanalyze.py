import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Data Analyzer",page_icon="💻",layout="wide")

st.title("🧑‍💻 Analyze Your Data 👩‍💻")
st.write("📂 Upload A **CSV** or an **Excel** File To Explore Your Data Interactively!")

 
 #  for uploading file 
upload_file = st.file_uploader("Upload a CSV or An Excel File", type=["csv",'xlsx'])

if upload_file is not None: 
    try:
        file_extension = upload_file.name.split('.')[-1].lower()

        if file_extension == 'csv':
            data = pd.read_csv(upload_file)
        elif file_extension == 'xlsx':
            data = pd.read_excel(upload_file)
        else:
            st.error("Unsupported file format")
            st.stop()

        # convert bool column as str
        bool_cols = data.select_dtypes(include=['bool']).columns
        data[bool_cols] = data[bool_cols].astype('str')

    except Exception as e:
        st.error('I could not read excel/csv file format')
        st.exception(e)
        st.stop()

    st.success('✅ File Uploaded Successfully!')
    st.write('### Preview of Data')
    st.dataframe(data.head())
 
    st.write("### 📋 Data Overview")
    st.write("Number Of Rows : ",data.shape[0])
    st.write("Number Of Column :",data.shape[1])
    st.write("Number Of Missing Values : ",data.isnull().sum().sum())
    st.write("Number Of Duplicate Records : ",data.duplicated().sum())

    st.write('### 📌 Complete Summary Of Dataset')
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    # describe()
    st.write('### 📊 Statistical Summary Of Dataset')
    st.dataframe(data.describe())

    st.write('### 📈 Statistical Summary For Non-Numerical Features Of Dataset')
    st.dataframe(data.describe(include=['bool','object']))

    st.write('### 🗳 Select The Desired Column For Analysis')
    selected_columns = st.multiselect("Choose Columns",data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info("No Column Selected. Showing Full Dataset")
        st.dataframe(data.head())
    
    st.write('### 🖥 Data Visualization')
    st.write("Select ***Columns*** For Data Visualization")
    columns = data.columns.tolist()
    x_axis = st.selectbox("Select Column For X-Axis",options=columns)
    y_axis = st.selectbox("Select Column For Y-Axis",options=columns)

    # Create Buttons For Diff Diff Charts
    col1, col2, col3 = st.columns(3)
 
    with col1:
        line_btn = st.button(' 📍 Line Graph')
    with col2:
        scatter_btn = st.button(' 📍 Scatter Graph')
    with col3:
        bar_btn = st.button(" 📍 Bar Chart")
 
    # 📈 Line Chart
    if line_btn:
        st.write('### Showing A Line Graph')
        fig,ax = plt.subplots()
        ax.plot(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Line Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)
 
    # 🔵 Scatter Chart
    if scatter_btn:
        st.write('### Showing A Scatter Graph')
        fig,ax = plt.subplots()
        ax.scatter(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Scatter Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)

    # 📊 Bar Chart
    if bar_btn:
        st.write('### Showing A Bar Chart ')
        fig, ax = plt.subplots()
        ax.bar(data[x_axis], data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Line Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)

else:

    st.info('Please Upload A CSV Or An Excel File To Get Started')
