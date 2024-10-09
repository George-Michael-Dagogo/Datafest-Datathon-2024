import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from psycopg2 import sql

def get_connection():
    # Replace these with your actual database credentials
    return psycopg2.connect(database_url)

def get_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        return [table[0] for table in cur.fetchall()]

def get_column_types(conn, table):
    with conn.cursor() as cur:
        cur.execute(sql.SQL("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = {}
        """).format(sql.Literal(table)))
        return {col: dtype for col, dtype in cur.fetchall()}

def visualize_database():
    st.title("Database Visualization")

    try:
        conn = get_connection()
    except psycopg2.Error as e:
        st.error(f"Unable to connect to the database: {e}")
        return

    table_names = get_tables(conn)

    if not table_names:
        st.error("No tables found in the database.")
        return

    selected_table = st.selectbox("Select a table to visualize", table_names)

    # Fetch data from the selected table
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(selected_table))
    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning(f"The table '{selected_table}' is empty.")
        return

    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(df)

    # Visualizations
    st.subheader("Visualizations")

    column_types = get_column_types(conn, selected_table)
    numeric_columns = [col for col, dtype in column_types.items() if dtype in ('integer', 'bigint', 'double precision', 'numeric')]
    categorical_columns = [col for col, dtype in column_types.items() if dtype in ('character varying', 'text', 'character')]

    if numeric_columns and categorical_columns:
        # 1. Bar chart
        x_axis = st.selectbox("Select X-axis (categorical)", categorical_columns)
        y_axis = st.selectbox("Select Y-axis (numeric)", numeric_columns)
        fig1 = px.bar(df, x=x_axis, y=y_axis, title=f'{y_axis} by {x_axis}')
        st.plotly_chart(fig1)

        # 2. Pie chart
        pie_column = st.selectbox("Select column for pie chart", categorical_columns)
        pie_counts = df[pie_column].value_counts()
        fig2 = px.pie(values=pie_counts.values, names=pie_counts.index, title=f'Distribution of {pie_column}')
        st.plotly_chart(fig2)

        # 3. Scatter plot
        x_scatter = st.selectbox("Select X-axis for scatter plot", numeric_columns)
        y_scatter = st.selectbox("Select Y-axis for scatter plot", [col for col in numeric_columns if col != x_scatter])
        color_scatter = st.selectbox("Select color category for scatter plot", categorical_columns)
        fig3 = px.scatter(df, x=x_scatter, y=y_scatter, color=color_scatter, title=f'{y_scatter} vs {x_scatter} colored by {color_scatter}')
        st.plotly_chart(fig3)
    else:
        st.warning("Not enough variety in column types to create all visualizations. Please ensure you have both numeric and categorical data.")

    conn.close()

# Add this function to your main app
if __name__ == "__main__":
    # ... (your existing code)
    
    # Add a new option in the sidebar
    page = st.sidebar.selectbox("Choose a page", ["Home", "Add Item", "View Inventory", "Update Item", "Delete Item", "Visualizations"])

    if page == "Visualizations":
        visualize_database()
    
    # ... (rest of your existing code)