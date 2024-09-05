import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Title of the app
st.title('Exploratory Data Analysis of Student Exam Performance')
st.subheader('by Paul Gary Oca')

# Initialize session state for navigation and plot type
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'
if 'plot_type' not in st.session_state:
    st.session_state['plot_type'] = 'All'

col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

with col1:
    if st.button('Home'):
        st.session_state['page'] = 'Home'
with col2:
    if st.button('Data Overview'):
        st.session_state['page'] = 'Data Overview'
with col3:
    if st.button('Data Analysis'):
        st.session_state['page'] = 'Data Analysis'

# Display content based on the selected navigation button
if st.session_state['page'] == 'Home':
    st.write("Welcome to the Student Exam Performance EDA app.")
    st.write("Use the navigation menu above to explore the data and perform analysis.")
    
    uploaded_file = st.file_uploader("Upload CSV file here", type="csv")   
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=';')

elif st.session_state['page'] == 'Data Overview':
    uploaded_file = st.file_uploader("Upload CSV file here", type="csv")   
    if uploaded_file is not None:
        # Load the data
        df = pd.read_csv(uploaded_file, delimiter=';')
        st.subheader('Display the first few rows of the dataset')
        st.write(df.head())
        
        # Show dataset information (e.g., data types, missing values)
        st.subheader('Missing Values')
        st.write(df.isnull().sum())
        
        # Generate summary statistics for the dataset
        st.subheader('Summary Statistics')
        st.write(df.describe())

elif st.session_state['page'] == 'Data Analysis':
    uploaded_file = st.file_uploader("Upload CSV file here", type="csv")   
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=';')

        # Numeric columns for correlation and plotting
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Dropdown for plot type selection
        plot_type = st.selectbox("Select the type of plot to display", 
                                 options=["Heatmap", "Box and Whisker Plots", "Scatter Plots", "Bar Plot", "All"])

        if plot_type == "Heatmap" or plot_type == "All":
            st.subheader('Correlation Heatmap')
            if num_cols:
                selected_columns = st.multiselect('Select columns to include in the heatmap', num_cols, default=num_cols[:3]) 
                if selected_columns:
                    df_filtered = df[selected_columns]
                    corr = df_filtered.corr()
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
                    
                    st.pyplot(fig)
                else:
                    st.write("Please select at least one column to generate the heatmap.")
            else:
                st.write("No numeric columns available for the heatmap.")

        if plot_type == "Box and Whisker Plots" or plot_type == "All":
            st.subheader('Box and Whisker Plots')
            selected_boxplot_cols = st.multiselect('Select columns for Box and Whisker plots', num_cols, default=num_cols[:3])  
            
            if selected_boxplot_cols:
                for i, col in enumerate(selected_boxplot_cols):
                    if i % 3 == 0:
                        cols = st.columns(3)

                    with cols[i % 3]:
                        try:
                            fig, ax = plt.subplots(figsize=(4, 3))  
                            sns.boxplot(x=df[col], ax=ax)
                            ax.set_title(f'Box and Whisker Plot of {col}')
                            st.pyplot(fig)
                        except Exception as e:
                            st.write(f"Error plotting column {col}: {e}")
            else:
                st.write("Please select at least one column to display Box and Whisker plots.")

        if plot_type == "Scatter Plots" or plot_type == "All":
            st.subheader('Scatter Plots')
            selected_scatter_cols = st.multiselect('Select columns for Scatter plots', num_cols, default=num_cols[:3])  
            
            if len(selected_scatter_cols) > 1:
                plot_count = 0
                for i, col1 in enumerate(selected_scatter_cols):
                    for col2 in selected_scatter_cols[i+1:]:
                        if plot_count % 3 == 0:
                            scatter_cols = st.columns(3)  

                        with scatter_cols[plot_count % 3]:
                            fig = px.scatter(df, x=col1, y=col2, title=f'Scatter Plot of {col1} vs {col2}')
                            st.plotly_chart(fig)
                        
                        plot_count += 1
            else:
                st.write("Please select at least two columns to generate Scatter plots.")

        if plot_type == "Bar Plot" or plot_type == "All":
            st.subheader('Bar Plot')
            selected_barplot_col = st.selectbox('Select a column for the Bar plot', num_cols)
            
            if selected_barplot_col:
                df_barplot = df[selected_barplot_col].value_counts()
                
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(x=df_barplot.index, y=df_barplot.values, ax=ax)
                ax.set_title(f'Bar Plot of {selected_barplot_col}')
                ax.set_xlabel(selected_barplot_col)
                ax.set_ylabel('Count')
                
                st.pyplot(fig)
            else:
                st.write("Please select a column to display the Bar plot.")
