#Importing necessary libraries

import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd
import matplotlib
matplotlib.use('Agg') #To not let streamlit crash because of Matplotlib GUI integration
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from dtale.views import startup
from dtale.app import get_instance
import plotly.express as px

#Initializing the session state

if 'airbnb_data' not in st.session_state:
    st.session_state.airbnb_data = None
if 'airbnb_df' not in st.session_state:
    st.session_state.airbnb_df = None

#Setting up dtale

def save_to_dtale(df):
    startup(data_id="1", data=df)

def retrieve_from_dtale():
    return get_instance("1").data

#Setting the page configuration

st.set_page_config(page_title= "Airbnb Data Analysis| By Surabhi Yadav",
                   page_icon= ":🏡:", 
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by *Surabhi Yadav!*"""})

with st.sidebar:

  select = option_menu("Main Menu", ["Data Preprocessing", "EDA", "Data Summary", "Data Exploration", "PowerBI Dashboard"],
                      icons=["funnel-fill", "graph-up", "clipboard-data-fill", "map-fill", "bar-chart-fill"], 
                      menu_icon="menu-up",
                      default_index=0,
                      orientation="vertical",
                      styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#FF5A5F"},
                                   "icon": {"font-size": "15px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}})
  
#Part I: Data Cleaning and Preprocessing

if select == "Data Preprocessing":

    st.header("Airbnb Data Preprocessing", divider = "gray")
    st.write("")
    st.subheader("Connection establishment with MongoDB Atlas")
    connect = st.button("Connect to MongoDB Atlas", use_container_width = True)
    if connect:
        #Connecting to MongoDB
        client = pymongo.MongoClient("mongodb+srv://sy09012000:aBmzDFJSExfXrVj8@cluster0.mam36xj.mongodb.net/?retryWrites=true&w=majority")

        #Accessing airbnb data
        db = client["sample_airbnb"]
        collection = db["listingsAndReviews"]

        st.session_state.airbnb_data = collection.find()
        st.success("The connection has been established successfully!")

    st.write("")
    st.subheader("Fetching the data from MongoDB Atlas")
    fetch = st.button("Fetch Data", use_container_width = True)
    if fetch:
        airbnb_list = []
        for i in st.session_state.airbnb_data:
            data = dict(Id = i['_id'],
                        Listing_url = i['listing_url'],
                        Name = i.get('name'),
                        Description = i['description'],
                        House_rules = i.get('house_rules'),
                        Property_type = i['property_type'],
                        Room_type = i['room_type'],
                        Bed_type = i['bed_type'],
                        Min_nights = int(i['minimum_nights']),
                        Max_nights = int(i['maximum_nights']),
                        Cancellation_policy = i['cancellation_policy'],
                        Accomodates = i['accommodates'],
                        Total_bedrooms = i.get('bedrooms'),
                        Total_beds = i.get('beds'),
                        Availability_365 = i['availability']['availability_365'],
                        Price = i['price'],
                        Security_deposit = i.get('security_deposit'),
                        Cleaning_fee = i.get('cleaning_fee'),
                        Extra_people = i['extra_people'],
                        Guests_included= i['guests_included'],
                        No_of_reviews = i['number_of_reviews'],
                        Review_scores = i['review_scores'].get('review_scores_rating'),
                        Amenities = ', '.join(i['amenities']),
                        Host_id = i['host']['host_id'],
                        Host_name = i['host']['host_name'],
                        Street = i['address']['street'],
                        Country = i['address']['country'],
                        Country_code = i['address']['country_code'],
                        Location_type = i['address']['location']['type'],
                        Longitude = i['address']['location']['coordinates'][0],
                        Latitude = i['address']['location']['coordinates'][1],
                        Is_location_exact = i['address']['location']['is_location_exact']
            )
            airbnb_list.append(data)

        st.session_state.airbnb_df = pd.DataFrame(airbnb_list)
        st.dataframe(st.session_state.airbnb_df)
        st.success("The data has been fetched successfully!")

    #Changing features of object data type to float type
    st.write("")
    st.subheader("Conversion of object type data to numeric type of necessary data")
    obj_to_num = st.button("Convert object type data to numeric type", use_container_width = True)
    if obj_to_num:
        columns_to_convert = ['Price', 'Security_deposit', 'Cleaning_fee', 'Extra_people', 'Guests_included']
        for col in columns_to_convert:
            st.session_state.airbnb_df[col] = st.session_state.airbnb_df[col].apply(lambda x: str(x) if isinstance(x, object) else x)
            # st.session_state.airbnb_df[col] = st.session_state.airbnb_df[col].apply(lambda x: float(x) if isinstance(x, str) else x)
            st.session_state.airbnb_df[col] = st.session_state.airbnb_df[col].apply(lambda x: float(x) if isinstance(x, str) and x != 'None' else None)

        st.dataframe(st.session_state.airbnb_df)
        st.success("The conversion has been done successfully!")

    st.write("")
    st.subheader("Fill up of missing values with necessary measures of central tendencies (moct)")
    filling_up_missing_values = st.button("Fill up w/ moct", use_container_width = True)
    if filling_up_missing_values:
        #Filling missing values with necessary measures of central tendencies
        st.session_state.airbnb_df['Total_bedrooms'] = st.session_state.airbnb_df['Total_bedrooms'].fillna(st.session_state.airbnb_df['Total_bedrooms'].mode()[0])
        st.session_state.airbnb_df['Total_beds'] = st.session_state.airbnb_df['Total_beds'].fillna(st.session_state.airbnb_df['Total_beds'].median())
        st.session_state.airbnb_df['Security_deposit'] = st.session_state.airbnb_df['Security_deposit'].fillna(st.session_state.airbnb_df['Security_deposit'].median())
        st.session_state.airbnb_df['Cleaning_fee'] = st.session_state.airbnb_df['Cleaning_fee'].fillna(st.session_state.airbnb_df['Cleaning_fee'].median())
        st.session_state.airbnb_df['Review_scores'] = st.session_state.airbnb_df['Review_scores'].fillna(st.session_state.airbnb_df['Review_scores'].median())
        st.dataframe(st.session_state.airbnb_df)
        st.success("The filling up of missing values has been done successfully!")

    st.write("")
    st.subheader("Fill up of empty values with necessary values")
    filling_up_empty_values = st.button("Fill up empty values", use_container_width = True)
    if filling_up_empty_values:
        #Filling empty values in some other columns
        st.session_state.airbnb_df['Description'] = st.session_state.airbnb_df['Description'].replace(to_replace='', value='No Description Provided')
        st.session_state.airbnb_df['House_rules'] = st.session_state.airbnb_df['House_rules'].replace(to_replace='', value='No House rules Provided')
        st.session_state.airbnb_df['Amenities'] = st.session_state.airbnb_df['Amenities'].replace(to_replace='', value='Not Available')
        st.dataframe(st.session_state.airbnb_df)
        st.success("The filling up of empty values has been done successfully!")

    # Removal of duplicated values
    st.write("")
    st.subheader("Removal of duplicate values")
    remove = st.button("Remove duplicate data", use_container_width=True)
    if remove:
        # Checking for the duplicate records and dropping them
        st.session_state.airbnb_df = st.session_state.airbnb_df.drop(labels=list(st.session_state.airbnb_df[st.session_state.airbnb_df.Name.duplicated(keep=False)].index))
        st.session_state.airbnb_df.reset_index(drop=True, inplace=True)
        st.dataframe(st.session_state.airbnb_df)
        st.success("The removal of duplicated values has been done successfully!")

#Part II: EDA (Both Normal and Automated)
if select == "EDA":
    st.header("EDA on Preprocessed Airbnb Data", divider = "gray")

    #General EDA
    st.write("")
    st.subheader("General EDA")
    show_general_eda = st.button("Show General EDA", use_container_width = True)
    if show_general_eda:  

        #Histogram
        st.write("")
        st.subheader("Histogram Plots")

        # Histogram of numerical columns
        numerical_columns = ['Min_nights', 'Max_nights', 'Accomodates', 'Total_bedrooms', 'Total_beds', 'Availability_365', 
                             'Price', 'Security_deposit', 'Cleaning_fee', 'Extra_people', 'Guests_included', 'No_of_reviews', 'Review_scores']
        num_plots = len(numerical_columns)
        num_cols = min(num_plots, 3)  
        num_rows = (num_plots - 1) // num_cols + 1 if num_plots > 1 else 1 

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))

        if num_plots > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, col in enumerate(numerical_columns):
            sns.histplot(st.session_state.airbnb_df[col], ax=axes[i], kde=True, bins=20)  # Adjust bins as needed
            axes[i].set_title(col)

        for i in range(num_plots, num_rows * num_cols):
            fig.delaxes(axes[i])

        plt.tight_layout()

        st.pyplot(fig)

        #Boxplot
        st.write("")
        st.subheader("Boxplots")
        #numerical_columns = st.session_state.airbnb_df.select_dtypes(include=['int64', 'float64']).columns
        numerical_columns = ['Min_nights', 'Max_nights', 'Accomodates', 'Total_bedrooms', 'Total_beds', 'Availability_365', 
                             'Price', 'Security_deposit', 'Cleaning_fee', 'Extra_people', 'Guests_included', 'No_of_reviews', 'Review_scores']
        num_plots = len(numerical_columns)
        num_cols = min(num_plots, 3)  
        num_rows = (num_plots - 1) // num_cols + 1 if num_plots > 1 else 1 

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))

        if num_plots > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        for i, col in enumerate(numerical_columns):
            sns.boxplot(data=st.session_state.airbnb_df[col], ax=axes[i])
            axes[i].set_title(col)

        for i in range(num_plots, num_rows * num_cols):
            fig.delaxes(axes[i])

        plt.tight_layout()

        st.pyplot(fig)

        #Scatter plots
        st.write("")
        st.subheader("Scatterplots")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Numeric-Numeric Scatterplot
        sns.scatterplot(x='Price', y='No_of_reviews', data=st.session_state.airbnb_df, ax=axes[0, 0])
        axes[0, 0].set_title('Price vs. Number of Reviews')

        # Categorical-Numeric Scatterplot
        sns.scatterplot(x='Property_type', y='Price', data=st.session_state.airbnb_df, ax=axes[0, 1])
        axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=90)
        axes[0, 1].set_title('Property Type vs. Price')

        # Numeric-Numeric-Size Scatterplot
        sns.scatterplot(x='Price', y='No_of_reviews', size='Accomodates', data=st.session_state.airbnb_df, ax=axes[1, 0])
        axes[1, 0].set_title('Price vs. Number of Reviews (Sized by Accomodates)')

        # Pairwise Scatterplot
        sns.scatterplot(x='Price', y='No_of_reviews', data=st.session_state.airbnb_df, ax=axes[1, 1])
        axes[1, 1].set_title('Price vs. Number of Reviews')

        plt.tight_layout()
        st.pyplot(fig)

        # Numeric-Numeric-Color Scatterplot
        fig, ax = plt.subplots(figsize=(10, 8))
        scatterplot = sns.scatterplot(x='Price', y='No_of_reviews', hue='Property_type', data=st.session_state.airbnb_df, ax=ax)
        ax.set_title('Price vs. Number of Reviews (Colored by Property Type)')
        ax.set_xlim(0, 8000)
        scatterplot.legend(loc='upper left', bbox_to_anchor=(1, 1))
        st.pyplot(fig)   

        #Swarm plot
        # swarm_plot = sns.catplot(x='Property_type', y='Room_type', data=st.session_state.airbnb_df, kind='swarm')
        # swarm_plot.set_xticklabels(rotation=45)  # Rotate x-axis labels for better readability

        # st.write("This plot shows the distribution of room types for different property types using a swarm plot.")
        # st.pyplot(swarm_plot) #causing diaplay issue in streamlit

        #Strip plot
        st.subheader("Distribution of room types for different property types using a strip plot")
        strip_plot = sns.catplot(x='Property_type', y='Room_type', data=st.session_state.airbnb_df, kind='strip')
        strip_plot.set_xticklabels(rotation=90, fontsize = 6)  # Rotate x-axis labels for better readability
        strip_plot.set_yticklabels(fontsize = 6) 
        st.pyplot(strip_plot)

        #Heatmap
        st.write("")
        st.subheader("Heatmap")
        numerical_columns = ['Min_nights', 'Max_nights', 'Accomodates', 'Total_bedrooms', 'Total_beds', 'Availability_365', 
                             'Price', 'Security_deposit', 'Cleaning_fee', 'Extra_people', 'Guests_included', 'No_of_reviews', 'Review_scores']
        numeric_df = st.session_state.airbnb_df[numerical_columns]
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", mask = mask)
        plt.title('Correlation Heatmap')
        plt.xlabel('Features')
        plt.ylabel('Features')
        st.pyplot(plt)

        #Other plots
        st.write("")
        st.subheader("Some important Barplots")
        fig, ax = plt.subplots(figsize=(10, 8))
        top_property_types = st.session_state.airbnb_df['Property_type'].value_counts().head(10)
        custom_colors = sns.color_palette('pastel', n_colors=len(top_property_types))
        ax = sns.countplot(data=st.session_state.airbnb_df, y='Property_type', order=top_property_types.index, hue='Property_type', palette=custom_colors, legend=False)
        ax.set_title("Top 10 property types available")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 8))
        top_host_names = st.session_state.airbnb_df['Host_name'].value_counts().head(10)
        custom_colors = sns.color_palette('pastel', n_colors=len(top_host_names))
        subset_colors = custom_colors[:7] 
        ax = sns.countplot(data=st.session_state.airbnb_df, y='Host_name', order=top_host_names.index, hue='Host_name', palette=subset_colors, legend=False)
        ax.set_title("Top 10 Hosts with Highest number of Listings")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax = sns.countplot(data=st.session_state.airbnb_df, x='Room_type', hue='Room_type', palette='pastel', legend=False)
        ax.set_title("Total listings in each room type")
        st.pyplot(fig)
        
    # Automated EDA
    st.write("")
    st.subheader("Automated EDA")
    show_automated_eda = st.button("Show Automated EDA", use_container_width = True)
    if show_automated_eda:
        save_to_dtale(st.session_state.airbnb_df)
        st.markdown('<iframe src="/dtale/main/1" width="1000" height="600"></iframe>', unsafe_allow_html=True)
        st.markdown('<a href="/dtale/main/1" target="_blank">Open D-Tale</a>', unsafe_allow_html=True)

#Part III: Data Summary/ Overview   

if select == "Data Summary":
    st.header("Summary of the Airbnb Data", divider = "gray")
    st.write("")
    country = st.multiselect('Select Country',sorted(st.session_state.airbnb_df.Country.unique()))
    st.write("")
    property_type = st.multiselect('Select Property_type',sorted(st.session_state.airbnb_df.Property_type.unique()))
    st.write("")
    room_type = st.multiselect('Select Room_type',sorted(st.session_state.airbnb_df.Room_type.unique()))
    st.write("")
    min_price = st.session_state.airbnb_df.Price.min()
    max_price = st.session_state.airbnb_df.Price.max()
    price_range = st.slider('Select Price Range', min_price, max_price, (min_price, max_price))

    query = f'Country in {country} & Room_type in {room_type} & Property_type in {property_type} & Price >= {price_range[0]} & Price <= {price_range[1]}'
    
    df = st.session_state.airbnb_df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
    fig = px.bar(df,
                    title='Top 10 Property Types',
                    x='Listings',
                    y='Property_type',
                    orientation='h',
                    color='Property_type',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True) 

    df = st.session_state.airbnb_df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
    fig = px.bar(df,
                    title='Top 10 Hosts with highest number of Listings',
                    x='Listings',
                    y='Host_name',
                    orientation='h',
                    color='Host_name',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig,use_container_width=True)

    df = st.session_state.airbnb_df.query(query).groupby(["Room_type"]).size().reset_index(name="Counts")
    fig = px.pie(df,
                    title='Total Listings in each Room types',
                    names='Room_type',
                    values='Counts',
                    # color_discrete_sequence=px.colors.sequential.Accent,
                    color_discrete_sequence=px.colors.qualitative.Dark2,
                    width=800,
                    height=600
                )
    fig.update_traces(textposition='outside', textinfo='value+label')
    st.plotly_chart(fig,use_container_width=True)
    
    country_df = st.session_state.airbnb_df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
    fig = px.choropleth(country_df,
                        title='Total Listings in each Country',
                        locations='Country',
                        locationmode='country names',
                        color='Total_Listings',
                        color_continuous_scale=px.colors.sequential.Viridis,
                        width=800,
                        height=600
                        )
    st.plotly_chart(fig,use_container_width=True)

#Part IV: Explore
if select == "Data Exploration":

    st.header("Exploration of the Airbnb Data", divider = "gray")

    st.write("")
    country = st.multiselect('Select Country',sorted(st.session_state.airbnb_df.Country.unique()))
    st.write("")
    property_type = st.multiselect('Select Property_type',sorted(st.session_state.airbnb_df.Property_type.unique()))
    st.write("")
    room_type = st.multiselect('Select Room_type',sorted(st.session_state.airbnb_df.Room_type.unique()))
    st.write("")
    min_price = st.session_state.airbnb_df.Price.min()
    max_price = st.session_state.airbnb_df.Price.max()
    price_range = st.slider('Select Price Range', min_price, max_price, (min_price, max_price))

    query = f'Country in {country} & Room_type in {room_type} & Property_type in {property_type} & Price >= {price_range[0]} & Price <= {price_range[1]}'
    
    st.write("")
    st.subheader("Price Analysis")
        
    pr_df = st.session_state.airbnb_df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
    fig = px.bar(data_frame=pr_df,
                    x='Room_type',
                    y='Price',
                    color='Price',
                    title='Avg Price in each Room type'
                )
    st.plotly_chart(fig,use_container_width=True)

    country_df = st.session_state.airbnb_df.query(query).groupby('Country',as_index=False)['Price'].mean()
    fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color= 'Price', 
                                    hover_data=['Price'],
                                    locationmode='country names',
                                    size='Price',
                                    title= 'Avg Price in each Country',
                                    color_continuous_scale='viridis',
                                    width=800,
                                    height=600
                        )
    st.plotly_chart(fig,use_container_width=True)
    
    st.write("")
    st.subheader("Availability Analysis")
    
    fig = px.box(data_frame=st.session_state.airbnb_df.query(query),
                    x='Room_type',
                    y='Availability_365',
                    color='Room_type',
                    title='Availability by Room type'
                )
    st.plotly_chart(fig,use_container_width=True)
    
    country_df = st.session_state.airbnb_df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
    country_df.Availability_365 = country_df.Availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df,
                                    locations='Country',
                                    color= 'Availability_365', 
                                    hover_data=['Availability_365'],
                                    locationmode='country names',
                                    size='Availability_365',
                                    title= 'Avg Availability in each Country',
                                    color_continuous_scale='viridis',
                                    width=800,
                                    height=600
                        )
    st.plotly_chart(fig,use_container_width=True)

#Part V: PowerBI Dashboard
if select == "PowerBI Dashboard":

    st.header("PowerBI Dashboard", divider = "gray")

    st.write("")
    st.components.v1.iframe("https://app.powerbi.com/reportEmbed?reportId=c36a17e6-1540-4f8d-9210-6e2f5949ef2e&autoAuth=true&ctid=51d0f2ee-919c-4fa2-bc10-e1b032991c40", width=1000, height=600)