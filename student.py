import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Title of the app
st.title('Exploratory Data Analysis (EDA) of Student Exam Performance')
st.subheader('Paul Gary Oca'
)

#File upload thingy
uploaded_file = st.file_uploader("a. Upload CSV file here", type="csv")

if uploaded_file is not None:
     # 1. Load the data
    df = pd.read_csv(uploaded_file, delimiter=';')
    #Display the first few rows of the dataset.
    #st.subheader('b. Display the first few rows of the dataset.')
    #st.write(df.head())
    # 2. Show dataset information (e.g., data types, missing values).
    st.subheader('c. Missing Values')
    st.write(df.isnull().sum())
    #3. Generate summary statistics for the dataset.
    st.subheader('d. Summary Statistics')
    st.write(df.describe())
    num_cols = df.select_dtypes(include=['number']).columns  # Only numeric columns
    #4. Heat map
    
# Replace 'GP' or any other non-numeric values with NaN
    numeric_columns = df.select_dtypes(include=[float, int]).columns.tolist()

    if numeric_columns:
        # Add a multiselect widget in Streamlit to let the user choose columns
        selected_columns = st.multiselect('Select columns to include in the heatmap', numeric_columns, default=numeric_columns)

        # If the user has selected any columns, proceed with the correlation heatmap
        if selected_columns:
            # Filter the DataFrame to include only selected columns
            df_filtered = df[selected_columns]
            
            # Compute the correlation matrix
            corr = df_filtered.corr()
            
            # Plot the heatmap with a custom size
            fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size (width, height)
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            
            # Display the heatmap in Streamlit
            st.subheader('e. Correlation Heatmap')
            st.pyplot(fig)
        else:
            st.write("Please select at least one column to generate the heatmap.")

   
    st.subheader('f. Box and Whisker Plots')
    #for col in num_cols:
        #try:
            # Ensure that the column is numeric and doesn't contain lists/arrays
            #if pd.api.types.is_numeric_dtype(df[col]) and df[col].apply(lambda x: isinstance(x, (int, float))).all():
                #fig, ax = plt.subplots()
                #sns.boxplot(x=df[col], ax=ax)
                #ax.set_title(f'Box and Whisker Plot of {col}')
                #st.pyplot(fig)
            #else:
                #st.write(f"Skipping column {col} as it doesn't contain simple numeric data.")
        #except ValueError as e:
            #st.write(f"Error plotting column {col}: {e}")
    
    # 6. #Use Plotly to create an interactive scatter plot of student performance.
    st.subheader('g. Scatter Plots')
    num_cols = df.select_dtypes(include=[np.number]).columns

    # Create scatter plots for all pairs of numerical features
    for i, col1 in enumerate(num_cols):
        for col2 in num_cols[i+1:]:
            fig, ax = plt.subplots()
            ax.scatter(df[col1], df[col2])
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.set_title(f'Scatter Plot of {col1} vs {col2}')
            st.pyplot(fig)
    
    