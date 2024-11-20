import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import plotly.express as px

# Cargar CSS
with open('./style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Título, subtítulo e imagen
st.markdown('<div class="centered_content"><p class="dashboard_title">Fashion Trends Dashboard</p></div>', unsafe_allow_html=True)
st.markdown('<div class="centered_content"><p class="dashboard_subtitle">Analyze and Discover Fashion Trends</p></div>', unsafe_allow_html=True)
st.markdown('<div class="centered_content"><img class="header_image" src="https://media.glamour.com/photos/63a235d04dd4cb9b8e66e522/master/w_1920,c_limit/trends.png" alt="Fashion Media"></div>', unsafe_allow_html=True)


with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "EDA", "Insights"],
        icons=["house", "bar-chart", "gear"],
        default_index=1,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#6C63FF",
            },
            "nav-link-selected": {"background-color": "#6C63FF"},
        },
    )

# Cargar el dataset
file_path = 'fashion_data_2018_2022.csv'
df = pd.read_csv(file_path)


# Inicio
if selected == "Home":
    st.markdown('<p class="page_heading">Welcome to the Fashion Trends Analysis App</p>', unsafe_allow_html=True)
    st.markdown('<p class="page_content">Explore fashion data trends to make informed choices in style and purchasing.</p>', unsafe_allow_html=True)

# EDA
elif selected == "EDA":
    st.markdown('<p class="page_heading">Exploratory Data Analysis</p>', unsafe_allow_html=True)

    if st.checkbox("Show raw data"):
        st.dataframe(df)

    st.markdown('<p class="section_subheading">Summary Statistics</p>', unsafe_allow_html=True)
    st.write(df.describe())

    st.markdown('<p class="section_subheading">Price Distribution</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    sns.histplot(df['price'], kde=True, ax=ax, color="#68b4ff")
    st.pyplot(fig)


    st.markdown('<p class="section_subheading">Top Categories by Sales</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    top_categories = df.groupby('category')['sales_count'].sum().nlargest(10).reset_index()
    sns.barplot(data=top_categories, x='sales_count', y='category', ax=ax, palette="cool")
    st.pyplot(fig)



# Insights
elif selected == "Insights":
    st.markdown('<p class="page_heading">Insights</p>', unsafe_allow_html=True)

    # Row 1: Sales by Category and Gender
    st.markdown('<p class="section_subheading">Sales by Category and Gender</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        def plot_category_sales():
            df_category_sales = df.groupby('category')['sales_count'].sum().reset_index()
            fig = px.bar(df_category_sales, x='category', y='sales_count', color="category", title="Sales by Category")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",  # Fondo del contenedor
                plot_bgcolor="rgba(0,0,0,0)",  # Fondo del gráfico
                title=dict(font=dict(size=20))  # Opcional: Tamaño del título
            )
            st.plotly_chart(fig, use_container_width=True)
        plot_category_sales()

    with c2:
        def plot_gender_sales():
            df_gender_sales = df.groupby('gender')['sales_count'].sum().reset_index()
            fig = px.pie(df_gender_sales, values='sales_count', names='gender', title="Sales by Gender")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=dict(font=dict(size=20))
            )
            st.plotly_chart(fig, use_container_width=True)
        plot_gender_sales()

    # Row 2: Price Distribution and Reviews
    st.markdown('<p class="section_subheading">Price Distribution and Reviews</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        def plot_price_distribution():
            fig = px.violin(df, y="price", x="category", color="category", box=True, points="all", title="Price Distribution by Category")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=dict(font=dict(size=20))
            )
            st.plotly_chart(fig, use_container_width=True)
        plot_price_distribution()

    with c4:
        def plot_reviews_vs_price():
            fig = px.scatter(df, x="price", y="reviews_count", color="category", size="average_rating",
                             hover_data=["product_name"], title="Relationship Between Price and Reviews")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=dict(font=dict(size=20))
            )
            st.plotly_chart(fig, use_container_width=True)
        plot_reviews_vs_price()
