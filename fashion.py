import streamlit as st
import pandas as pd
import seaborn as sns
from streamlit_option_menu import option_menu
import plotly.express as px

# Configuración inicial
st.set_page_config(
    page_title="Fashion Trends Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar CSS
css_file = './style.css'
if os.path.exists(css_file):
    with open(css_file) as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
else:
    st.warning("El archivo de estilos CSS no fue encontrado. Se usará el diseño predeterminado.")

# Título, subtítulo e imagen
st.markdown('<div class="centered_content"><p class="dashboard_title">Fashion Trends Dashboard</p></div>', unsafe_allow_html=True)
st.markdown('<div class="centered_content"><p class="dashboard_subtitle">Analyze and Discover Fashion Trends</p></div>', unsafe_allow_html=True)
st.markdown('<div class="centered_content"><img class="header_image" src="https://media.glamour.com/photos/63a235d04dd4cb9b8e66e522/master/w_1920,c_limit/trends.png" alt="Fashion Media"></div>', unsafe_allow_html=True)

# Menú lateral
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
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"El archivo '{file_path}' no fue encontrado. Asegúrate de que el archivo esté en la ruta correcta.")
    df = pd.DataFrame()  # Dataset vacío para evitar errores
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    df = pd.DataFrame()

# Verifica si el dataset tiene datos
if not df.empty:
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
        if 'price' in df.columns:
            fig = px.histogram(
                df, 
                x='price', 
                nbins=50, 
                title='Price Distribution', 
                marginal='box', # Puedes quitar esto si no quieres una caja resumen
                color_discrete_sequence=["#68b4ff"],
                opacity=0.7
            )
            fig.update_layout(bargap=0.1) # Ajusta el espacio entre barras
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="section_subheading">Top Categories by Sales</p>', unsafe_allow_html=True)
        if 'category' in df.columns and 'sales_count' in df.columns:
            top_categories = df.groupby('category')['sales_count'].sum().nlargest(10).reset_index()
            fig = px.bar(
                top_categories, 
                x='sales_count', 
                y='category', 
                orientation='h', 
                title='Top Categories by Sales',
                color='sales_count', 
                color_continuous_scale='Blues'
            )
            fig.update_layout(yaxis=dict(categoryorder="total ascending"))  # Ordena de menor a mayor
            st.plotly_chart(fig, use_container_width=True)

        
        
    # Insights
    elif selected == "Insights":
        st.markdown('<p class="page_heading">Insights</p>', unsafe_allow_html=True)

        # Row 1: Sales by Category and Gender
        st.markdown('<p class="section_subheading">Sales by Category and Gender</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if 'category' in df.columns and 'sales_count' in df.columns:
                df_category_sales = df.groupby('category')['sales_count'].sum().reset_index()
                fig = px.bar(df_category_sales, x='category', y='sales_count', color="category", title="Sales by Category")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Las columnas necesarias para esta visualización no están disponibles.")

        with c2:
            if 'gender' in df.columns and 'sales_count' in df.columns:
                df_gender_sales = df.groupby('gender')['sales_count'].sum().reset_index()
                fig = px.pie(df_gender_sales, values='sales_count', names='gender', title="Sales by Gender")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Las columnas necesarias para esta visualización no están disponibles.")

        # Row 2: Price Distribution and Reviews
        st.markdown('<p class="section_subheading">Price Distribution and Reviews</p>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            if 'price' in df.columns and 'category' in df.columns:
                fig = px.violin(df, y="price", x="category", color="category", box=True, points="all", title="Price Distribution by Category")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Las columnas necesarias para esta visualización no están disponibles.")

        with c4:
            if 'price' in df.columns and 'reviews_count' in df.columns and 'average_rating' in df.columns and 'product_name' in df.columns:
                fig = px.scatter(df, x="price", y="reviews_count", color="category", size="average_rating",
                                 hover_data=["product_name"], title="Relationship Between Price and Reviews")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Las columnas necesarias para esta visualización no están disponibles.")
else:
    st.warning("El dataset está vacío o no se pudo cargar.")

