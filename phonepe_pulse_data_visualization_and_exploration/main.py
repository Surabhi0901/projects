#Importing necessary libraries

import os
import git
import pandas as pd
import json
import mysql.connector as sql
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

#Setting up the page

st.set_page_config(page_title= " Best Algorithm Selection| By Surabhi Yadav",
                   page_icon= ":💵:", 
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by *Surabhi Yadav!*"""})

with st.sidebar:
    selected = option_menu('MENU', ["Map View", "Data Analysis", "Interactive Dashboard"], 
                           icons=["map-fill", "", "bar-chart-line-fill", "clipboard2-pulse-fill"], 
                           menu_icon="menu-up",
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#6739B7"},
                                   "icon": {"font-size": "15px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#6739B7"}})
    
#Cloning the repository

repo_url = 'https://github.com/PhonePe/pulse.git'
local_dir = r'C:\Users\sy090\Downloads\PROJECTS\phonepe_pulse_data_visualization_and_exploration\pulse'
if not os.path.exists(local_dir):
    git.Repo.clone_from(repo_url, local_dir)

#Creating a key value pair for state names
state_dict = {"andaman-&-nicobar-islands": "Andaman & Nicobar", "andhra-pradesh": "Andhra Pradesh",
              "arunachal-pradesh": "Arunachal Pradesh", "assam": "Assam", "bihar": "Bihar", "chandigarh": "Chandigarh",
              "chhattisgarh": "Chhattisgarh", "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
              "delhi": "Delhi", "goa": "Goa", "gujarat": "Gujarat", "haryana": "Haryana", "himachal-pradesh": "Himachal Pradesh",
              "jammu-&-kashmir": "Jammu & Kashmir", "jharkhand": "Jharkhand", "karnataka": "Karnataka", "kerala": "Kerala", 
              "ladakh": "Ladakh", "lakshadweep": "Lakshadweep", "madhya-pradesh": "Madhya Pradesh", "maharashtra": "Maharashtra",
              "manipur": "Manipur", "meghalaya": "Meghalaya", "mizoram": "Mizoram", "nagaland": "Nagaland", "odisha": "Odisha",
              "puducherry": "Puducherry", "punjab": "Punjab", "rajasthan": "Rajasthan", "sikkim": "Sikkim", "tamil-nadu": "Tamil Nadu",
              "telangana": "Telangana", "tripura": "Tripura" , "uttar-pradesh": "Uttar Pradesh", "uttarakhand": "Uttarakhand",
              "west-bengal": "West Bengal"}

#Reading the data and transforming it into suitable format

#Aggregated transaction
path_agg_trans = f"{local_dir}/data/aggregated/transaction/country/india/state/"
agg_state_list=os.listdir(path_agg_trans)

agg_trans={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in agg_state_list:
    p_i=path_agg_trans+i+"/"
    agg_yr=os.listdir(p_i)
    for j in agg_yr:
        p_j=p_i+j+"/"
        agg_yr_list=os.listdir(p_j)
        for k in agg_yr_list:
            p_k=p_j+k
            data=open(p_k,'r')
            D=json.load(data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              agg_trans['Transaction_type'].append(Name)
              agg_trans['Transaction_count'].append(count)
              agg_trans['Transaction_amount'].append(amount)
              agg_trans['State'].append(state_dict[i])
              agg_trans['Year'].append(j)
              agg_trans['Quarter'].append(int(k.strip('.json')))

agg_trans=pd.DataFrame(agg_trans)
# print(agg_trans)
# print(agg_trans.dtypes)

#Aggregated user
path_agg_user = f"{local_dir}/data/aggregated/user/country/india/state/"
agg_state_list=os.listdir(path_agg_user)

agg_user={'State':[], 'Year':[],'Quarter':[],'Registered_users':[], 'App_opens':[]}

for i in agg_state_list:
    p_i=path_agg_user+i+"/"
    agg_yr=os.listdir(p_i)
    for j in agg_yr:
        p_j=p_i+j+"/"
        agg_yr_list=os.listdir(p_j)
        for k in agg_yr_list:
            p_k=p_j+k
            data=open(p_k,'r')
            D=json.load(data)
            registered_users=D['data']['aggregated']['registeredUsers']
            app_opens=D['data']['aggregated']['appOpens']
            agg_user['Registered_users'].append(registered_users)
            agg_user['App_opens'].append(app_opens)
            agg_user['State'].append(state_dict[i])
            agg_user['Year'].append(j)
            agg_user['Quarter'].append(int(k.strip('.json')))

agg_user=pd.DataFrame(agg_user)
# print(agg_user)
# print(agg_user.dtypes)

#Top transaction
path_top_trans = f"{local_dir}/data/top/transaction/country/india/state/"
top_state_list=os.listdir(path_top_trans)

top_trans={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_count':[], 'District_amount':[], 'Pincode':[], 'Pincode_count':[], 'Pincode_amount':[]}

for i in top_state_list:
    p_i=path_top_trans+i+"/"
    top_yr=os.listdir(p_i)
    for j in top_yr:
        p_j=p_i+j+"/"
        top_yr_list=os.listdir(p_j)
        for k in top_yr_list:
            p_k=p_j+k
            data=open(p_k,'r')
            D=json.load(data)
            for z in D['data']['districts']:
              Name=z['entityName']
              count=z['metric']['count']
              amount=z['metric']['amount']
              top_trans['District_name'].append(Name)
              top_trans['District_count'].append(count)
              top_trans['District_amount'].append(amount)
              top_trans['Pincode'].append('None')
              top_trans['Pincode_count'].append('None')
              top_trans['Pincode_amount'].append('None')
              top_trans['State'].append(state_dict[i])
              top_trans['Year'].append(j)
              top_trans['Quarter'].append(int(k.strip('.json')))
            for z in D['data']['pincodes']:
              Name=z['entityName']
              count=z['metric']['count']
              amount=z['metric']['amount']
              top_trans['District_name'].append('None')
              top_trans['District_count'].append('None')
              top_trans['District_amount'].append('None')
              top_trans['Pincode'].append(Name)
              top_trans['Pincode_count'].append(count)
              top_trans['Pincode_amount'].append(amount)
              top_trans['State'].append(state_dict[i])
              top_trans['Year'].append(j)
              top_trans['Quarter'].append(int(k.strip('.json')))

top_trans=pd.DataFrame(top_trans)
# print(top_trans)
# print(top_trans.dtypes)

#Top user
path_top_user = f"{local_dir}/data/top/user/country/india/state/"
top_state_list=os.listdir(path_top_user)

top_user={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_registered_users':[], 'Pincode':[], 'Pincode_registered_users':[]}

for i in top_state_list:
    p_i=path_top_user+i+"/"
    top_yr=os.listdir(p_i)
    for j in top_yr:
        p_j=p_i+j+"/"
        top_yr_list=os.listdir(p_j)
        for k in top_yr_list:
            p_k=p_j+k
            data=open(p_k,'r')
            D=json.load(data)
            for z in D['data']['districts']:
              Name=z['name']
              registered_users=z['registeredUsers']
              top_user['District_name'].append(Name)
              top_user['District_registered_users'].append(registered_users)
              top_user['Pincode'].append('None')
              top_user['Pincode_registered_users'].append('None')
              top_user['State'].append(state_dict[i])
              top_user['Year'].append(j)
              top_user['Quarter'].append(int(k.strip('.json')))
            for z in D['data']['pincodes']:
              Name=z['name']
              registered_users=z['registeredUsers']
              top_user['District_name'].append('None')
              top_user['District_registered_users'].append('None')
              top_user['Pincode'].append(Name)
              top_user['Pincode_registered_users'].append(registered_users)
              top_user['State'].append(state_dict[i])
              top_user['Year'].append(j)
              top_user['Quarter'].append(int(k.strip('.json')))

top_user=pd.DataFrame(top_user)
# print(top_user)
# print(top_user.dtypes)

#Map transaction
path_map_trans = f"{local_dir}/data/map/transaction/hover/country/india/state/"
map_state_list=os.listdir(path_map_trans)

map_trans={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_count':[], 'District_amount':[]}

for i in map_state_list:
    p_i=path_map_trans+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            data=open(p_k,'r')
            D=json.load(data)
            for z in D['data']['hoverDataList']:
              Name=z['name']
              count=z['metric'][0]['count']
              amount=z['metric'][0]['amount']
              map_trans['District_name'].append(Name)
              map_trans['District_count'].append(count)
              map_trans['District_amount'].append(amount)
              map_trans['State'].append(state_dict[i])
              map_trans['Year'].append(j)
              map_trans['Quarter'].append(int(k.strip('.json')))

map_trans=pd.DataFrame(map_trans)
# print(map_trans)
# print(map_trans.dtypes)

#Map user
path_map_user = f"{local_dir}/data/map/user/hover/country/india/state/"
map_state_list=os.listdir(path_map_user)

map_user={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_registered_users':[], 'District_app_opens':[]}

for i in map_state_list:
    p_i=path_map_user+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            data=open(p_k,'r')
            D=json.load(data)
            for key,value in D['data']['hoverData'].items():
              Name=key
              registered_users= value['registeredUsers']
              app_opens = value['appOpens']
              map_user['District_name'].append(Name)
              map_user['District_registered_users'].append(registered_users)
              map_user['District_app_opens'].append(app_opens)
              map_user['State'].append(state_dict[i])
              map_user['Year'].append(j)
              map_user['Quarter'].append(int(k.strip('.json')))

map_user=pd.DataFrame(map_user)
# print(map_user)
# print(map_user.dtypes)

#Storing the data into MySQL DB

#Setting up the connection to MySQL Server
connect = sql.connect(
host = "localhost",
user="root",
password="password",
auth_plugin = "mysql_native_password",
charset='utf8mb4')

#Creating a new youtube database if it doesn't exist 
mycursor = connect.cursor()
mycursor.execute("SET NAMES 'UTF8MB4'")
mycursor.execute("SET CHARACTER SET UTF8MB4")
mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_db")

mycursor.close()
connect.close()

charset = 'utf8mb4'
engine = create_engine('mysql+pymysql://root:password@localhost/phonepe_db?charset={}'.format(charset), echo=False, pool_size=10, max_overflow=20)

#Aggregated transaction to MySQL DB
#agg_trans={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
agg_trans.to_sql('agg_trans', engine, if_exists='append', index=False,
                        dtype = {"State": sqlalchemy.types.VARCHAR(length=225),
                                 "Year": sqlalchemy.types.VARCHAR(length=225),
                                 "Quarter": sqlalchemy.types.INT,
                                 "Transaction_type": sqlalchemy.types.VARCHAR(length=225),
                                 "Transaction_count": sqlalchemy.types.BigInteger,
                                 "Transaction_amount": sqlalchemy.types.FLOAT,})

#agg_user={'State':[], 'Year':[],'Quarter':[],'Registered_users':[], 'App_opens':[]}
agg_user.to_sql('agg_user', engine, if_exists='append', index=False,
                        dtype = {"State": sqlalchemy.types.VARCHAR(length=225),
                                 "Year": sqlalchemy.types.VARCHAR(length=225),
                                 "Quarter": sqlalchemy.types.INT,
                                 "Registered_users": sqlalchemy.types.BigInteger,
                                 "App_opens": sqlalchemy.types.BigInteger,})

#top_trans={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_count':[], 'District_amount':[], 'Pincode':[], 'Pincode_count':[], 'Pincode_amount':[]}
top_trans.to_sql('top_trans', engine, if_exists='append', index=False,
                        dtype = {"State": sqlalchemy.types.VARCHAR(length=225),
                                 "Year": sqlalchemy.types.VARCHAR(length=225),
                                 "Quarter": sqlalchemy.types.INT,
                                 "District_name": sqlalchemy.types.VARCHAR(length=225),
                                 "District_count": sqlalchemy.types.VARCHAR(length=225),
                                 "District_amount": sqlalchemy.types.VARCHAR(length=225),
                                 "Pincode": sqlalchemy.types.VARCHAR(length=225),
                                 "Pincode_count": sqlalchemy.types.VARCHAR(length=225),
                                 "Pincode_amount": sqlalchemy.types.VARCHAR(length=225),})

#top_user={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_registered_users':[], 'Pincode':[], 'Pincode_registered_users':[]}
top_user.to_sql('top_user', engine, if_exists='append', index=False,
                        dtype = {"State": sqlalchemy.types.VARCHAR(length=225),
                                 "Year": sqlalchemy.types.VARCHAR(length=225),
                                 "Quarter": sqlalchemy.types.INT,
                                 "District_name": sqlalchemy.types.VARCHAR(length=225),
                                 "District_registered_users": sqlalchemy.types.VARCHAR(length=225),
                                 "Pincode_registered_users": sqlalchemy.types.VARCHAR(length=225),})

#map_trans={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_count':[], 'District_amount':[]}
map_trans.to_sql('map_trans', engine, if_exists='append', index=False,
                        dtype = {"State": sqlalchemy.types.VARCHAR(length=225),
                                 "Year": sqlalchemy.types.VARCHAR(length=225),
                                 "Quarter": sqlalchemy.types.INT,
                                 "District_name": sqlalchemy.types.VARCHAR(length=225),
                                 "District_count": sqlalchemy.types.BigInteger,
                                 "District_count": sqlalchemy.types.VARCHAR(length=225),})

#map_user={'State':[], 'Year':[],'Quarter':[],'District_name':[], 'District_registered_users':[], 'District_app_opens':[]}
map_user.to_sql('map_user', engine, if_exists='append', index=False,
                        dtype = {"State": sqlalchemy.types.VARCHAR(length=225),
                                 "Year": sqlalchemy.types.VARCHAR(length=225),
                                 "Quarter": sqlalchemy.types.INT,
                                 "District_name": sqlalchemy.types.VARCHAR(length=225),
                                 "District_registered_users": sqlalchemy.types.BigInteger,
                                 "District_app_opens": sqlalchemy.types.BigInteger,})

#Creating an interactive map view

if selected == "Map View":

    st.header("An Interactive Map View of the Phonepe Pulse Data")

    option = st.selectbox("Select a map view:", ("Based on transaction amount", "Based on transaction count", 
    "Based on registered users", "Based on app opens"),
    index=None,
    placeholder="Select viewing option...",)
    
    #Based on transaction amount of each state
    if option == "Based on transaction amount": 
        fig1 = px.choropleth(agg_trans,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Transaction_amount',
                            color_continuous_scale="Viridis",
                            range_color=(200000, 447138250),
                            ) #min: 20003450, max: 4471382500

        fig1.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig1, use_container_width=True)

    #Based on transaction count of each state
    if option == "Based on transaction count":
        fig2 = px.choropleth(agg_trans,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Transaction_count',
                            color_continuous_scale="Viridis",
                            range_color=(24941, 489366),
                            ) #min: 24941, max: 4893667

        fig2.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig2, use_container_width=True)

    #Based on registered users of each state
    if option == "Based on registered users":
        fig3 = px.choropleth(agg_user,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Registered_users',
                            color_continuous_scale="Viridis",
                            range_color=(5597940, 10895052),
                            ) #min: 249794, max: 10895052

        fig3.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig3, use_container_width=True)

    #Based on app opens of each state
    if option == "Based on app opens":
        fig4 = px.choropleth(agg_user,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='App_opens',
                            color_continuous_scale="Viridis",
                            range_color=(70155650, 285587581),
                            ) #515565, 285587581

        fig4.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig4, use_container_width=True)

#Analyzing the data

if selected == "Data Analysis":
    
    st.header("Exploration of the Phonepe Pulse Data and gaining some Basic Insights from it")

    question_tosql = st.selectbox("Select a question:",[
            "1. Top 10 states  based on the transaction amount",
            "2. Top 10 states based on the transaction count",
            "3. Top 10 states based on number of registered users",
            "4. Top 10 states based on app opens",
            "5. Top 10 districts (and corresponding states) based on the transaction amount",
            "6. Top 10 pincodes (and corresponding states) based on the transaction amount",
            "7. Top 10 districts (and corresponding states) based on number of registered users",
            "8. Top 10 pincodes (and corresponding states) based on number of registered users",
            "9. List of year and their respective transaction amount",
            "10. List of year and their respective transaction count"
            ],index=None, placeholder="Select a question...",)

    connect_for_question = pymysql.connect(host='localhost', user='root', password='password', db='phonepe_db')
    cursor = connect_for_question.cursor()

    if question_tosql == '1. Top 10 states  based on the transaction amount':
        cursor.execute("SELECT agg_trans.State, SUM(agg_trans.Transaction_amount) AS Total_Transaction_Amount FROM agg_trans GROUP BY agg_trans.State ORDER BY Total_Transaction_Amount DESC LIMIT 10;")
        result_1 = cursor.fetchall()
        df1 = pd.DataFrame(result_1, columns=['State', 'Transaction_amount']).reset_index(drop=True)
        df1.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df1)
        with col2:
            fig=px.bar(df1,x="State",y="Transaction_amount")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '2. Top 10 states based on the transaction count':

        cursor.execute("SELECT agg_trans.State, SUM(agg_trans.Transaction_count) AS Total_Transaction_Count FROM agg_trans GROUP BY agg_trans.State ORDER BY Total_Transaction_Count DESC LIMIT 10;")
        result_2 = cursor.fetchall()
        df2 = pd.DataFrame(result_2,columns=['State','Transaction_count']).reset_index(drop=True)
        df2.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df2)
        with col2:
            fig=px.bar(df2,x="State",y="Transaction_count")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '3. Top 10 states based on number of registered users':

        cursor.execute("SELECT agg_user.State, SUM(agg_user.Registered_users) AS Total_Registered_Users FROM agg_user GROUP BY agg_user.State ORDER BY Total_Registered_Users DESC LIMIT 10;")
        result_3 = cursor.fetchall()
        df3 = pd.DataFrame(result_3,columns=['State', 'Registered_users']).reset_index(drop=True)
        df3.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df3)
        with col2:
            fig=px.bar(df3,x="State",y="Registered_users")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    elif question_tosql == '4. Top 10 states based on app opens':
        cursor.execute("SELECT agg_user.State, SUM(agg_user.App_opens) AS Total_App_Opens FROM agg_user GROUP BY agg_user.State ORDER BY Total_App_Opens DESC LIMIT 10;")
        result_4 = cursor.fetchall()
        df4 = pd.DataFrame(result_4,columns=['State', 'App_opens']).reset_index(drop=True)
        df4.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df4)
        with col2:
            fig=px.bar(df4,x="State",y="App_opens")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '5. Top 10 districts (and corresponding states) based on the transaction amount':
        cursor.execute("SELECT top_trans.District_name, top_trans.State, SUM(top_trans.District_amount) AS Total_Transaction_Amount FROM top_trans GROUP BY top_trans.District_name, top_trans.State ORDER BY Total_Transaction_Amount DESC LIMIT 10;")
        result_5= cursor.fetchall()
        df5 = pd.DataFrame(result_5,columns=['District', 'State', 'Transaction_amount']).reset_index(drop=True)
        df5.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df5)
        with col2:
            fig=px.bar(df5,x="District",y="Transaction_amount")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '6. Top 10 pincodes (and corresponding states) based on the transaction amount':
        cursor.execute("SELECT top_trans.Pincode, top_trans.State, SUM(top_trans.Pincode_amount) AS Total_Transaction_Amount FROM top_trans GROUP BY top_trans.Pincode, top_trans.State ORDER BY Total_Transaction_Amount DESC LIMIT 10;")
        result_6= cursor.fetchall()
        df6 = pd.DataFrame(result_6,columns=['Pincode', 'State', 'Transaction_amount']).reset_index(drop=True)
        df6.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df6)
        with col2:
            pincode_integers = list(range(1, len(df6['Pincode']) + 1))
            pincode_mapping = dict(zip(pincode_integers, df6['Pincode']))
            fig = px.bar(df6, x=pincode_integers, y="Transaction_amount")
            fig.update_xaxes(title_text="Pincode", tickvals=pincode_integers, ticktext=list(pincode_mapping.values()))
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '7. Top 10 districts (and corresponding states) based on number of registered users':
        cursor.execute("SELECT top_user.District_name, top_user.State, SUM(top_user.District_registered_users) AS Total_District_registered_users FROM top_user GROUP BY top_user.District_name, top_user.State ORDER BY Total_District_registered_users DESC LIMIT 10;")
        result_7= cursor.fetchall()
        df7 = pd.DataFrame(result_7,columns=['District', 'State', 'Registered_users']).reset_index(drop=True)
        df7.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df7)
        with col2:
            fig=px.bar(df7,x="District",y="Registered_users")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '8. Top 10 pincodes (and corresponding states) based on number of registered users':
        cursor.execute("SELECT top_user.Pincode, top_user.State, SUM(top_user.Pincode_registered_users) AS Total_Pincode_registered_users FROM top_user GROUP BY top_user.Pincode, top_user.State ORDER BY Total_Pincode_registered_users DESC LIMIT 10;")
        result_8= cursor.fetchall()
        df8 = pd.DataFrame(result_8,columns=['Pincode','State', 'Registered_users']).reset_index(drop=True)
        df8.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df8)
        with col2:
            pincode_integers = list(range(1, len(df8['Pincode']) + 1))
            pincode_mapping = dict(zip(pincode_integers, df8['Pincode']))
            fig = px.bar(df8, x=pincode_integers, y="Registered_users")
            fig.update_xaxes(title_text="Pincode", tickvals=pincode_integers, ticktext=list(pincode_mapping.values()))
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    elif question_tosql == '9. List of year and their respective transaction amount':
        cursor.execute("SELECT agg_trans.Year, SUM(agg_trans.Transaction_amount) AS Total_Transaction_Amount FROM agg_trans GROUP BY agg_trans.Year ORDER BY Total_Transaction_Amount DESC;")
        result_9= cursor.fetchall()
        df9 = pd.DataFrame(result_9,columns=['Year','Transaction_amount']).reset_index(drop=True)
        df9.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df9)
        with col2:
            fig=px.bar(df9,x="Year",y="Transaction_amount")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    elif question_tosql == '10. List of year and their respective transaction count':
        cursor.execute("SELECT agg_trans.Year, SUM(agg_trans.Transaction_count) AS Total_Transaction_Count FROM agg_trans GROUP BY agg_trans.Year ORDER BY Total_Transaction_Count DESC;")
        result_10= cursor.fetchall()
        df10 = pd.DataFrame(result_10,columns=['Year','Transaction_count']).reset_index(drop=True)
        df10.index += 1
        col1,col2 = st.columns(2)
        with col1:
            st.write(df10)
        with col2:
            fig=px.bar(df10,x="Year",y="Transaction_count")
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    connect_for_question.close()        

#Creating an interactive dashboard

if selected == "Interactive Dashboard":

    st.header("An Interactive Dashboard to Visualize the Phonepe Pulse Data")

    col1,col2= st.columns([1,1.5],gap="large")
    with col1:
        st.markdown("<h2 style='color: white; font-size: 20px;'>Select the criteria to visualize the data:</h2>", unsafe_allow_html=True)
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
        Type = st.selectbox("**Type**", ("Transactions", "Users"))
    
    with col2:
        st.info(
                """
                #### The following basic insights can be gained from this interactive dashboard:
                - Ranking of states in the selected Year and Quarter.
                - Top 10 State, District and Pincode based on total number of transaction and total amount spent on phonepe.
                - Top 10 State, District and Pincode based on total number of phonepe users and frequency of app opening.
                """ 
                )
        
    connect_for_int_dash = pymysql.connect(host='localhost', user='root', password='password', db='phonepe_db')
    cursor = connect_for_int_dash.cursor()


#Transactions    
    if Type == "Transactions":

        #State
        st.markdown("### :white[State]")
        cursor.execute(f"SELECT agg_trans.State, SUM(agg_trans.Transaction_count) AS Total_Transaction_Count, SUM(agg_trans.Transaction_amount) AS Total_Transaction_Amount FROM agg_trans WHERE agg_trans.Year = {Year} AND agg_trans.Quarter = {Quarter} GROUP BY agg_trans.State ORDER BY Total_Transaction_Amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_Count','Transaction_Amount'])
        fig = px.pie(df, values='Transaction_Amount',
                            names='State',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_Count'],
                            labels={'Transaction_Count':'Transaction_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        #District
        st.markdown("### :white[District]")
        cursor.execute(f"SELECT top_trans.District_name, SUM(top_trans.District_count) as Total_Transaction_Count, SUM(top_trans.District_amount) AS Total_Transaction_Amount FROM top_trans WHERE top_trans.Year = {Year} AND top_trans.Quarter = {Quarter} GROUP BY top_trans.District_name ORDER BY Total_Transaction_Amount DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction_Count','Transaction_Amount'])

        fig = px.pie(df, values='Transaction_Amount',
                            names='District',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_Count'],
                            labels={'Transaction_Count':'Transaction_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
        
        #Pincode
        st.markdown("### :white[Pincode]")
        cursor.execute(f"SELECT top_trans.Pincode, SUM(top_trans.Pincode_count) AS Total_Transaction_Count, SUM(top_trans.Pincode_amount) AS Total_Transaction_Amount FROM top_trans WHERE top_trans.Year = {Year} AND top_trans.Quarter = {Quarter} GROUP BY Pincode ORDER BY Total_Transaction_Amount DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transaction_Count','Total_Transaction_Amount'])
        fig = px.pie(df, values='Total_Transaction_Amount',
                            names='Pincode',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Transaction_Count'],
                            labels={'Transaction_Count':'Transaction_Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        #Payment type vs. Transaction count
        st.markdown("## :white[Payment Type vs. Transaction count]")
        cursor.execute(f"SELECT agg_trans.Transaction_type, SUM(agg_trans.Transaction_count) AS Total_Transaction_Count, SUM(agg_trans.Transaction_amount) AS Total_Transaction_Amount FROM agg_trans WHERE agg_trans.Year= {Year} AND agg_trans.Quarter = {Quarter} GROUP BY agg_trans.Transaction_type ORDER BY agg_trans.Transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Payment_type', 'Total_Transaction_Count','Total_Transaction_Amount'])

        fig = px.bar(df,
                     title='Payment Type vs. Transaction count',
                     x="Payment_type",
                     y="Total_Transaction_Count",
                     orientation='v',
                     color='Total_Transaction_Amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)

        #District vs. Transaction count          
        st.markdown("## :white[District vs. Transaction count  ]")

        selected_state = st.selectbox("Select a state:", ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 
                                                          'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 
                                                          'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 
                                                          'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 
                                                          'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
                                                          'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 
                                                          'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 
                                                          'Uttarakhand', 'West Bengal'), index=None, placeholder="Select a state...")
        
        cursor.execute(f"SELECT map_trans.State, map_trans.District_name, map_trans.Year, map_trans.Quarter, SUM(map_trans.District_count) AS Total_Transaction_Count, SUM(map_trans.District_amount) AS Total_Transaction_Amount FROM map_trans WHERE map_trans.Year = {Year} AND map_trans.Quarter = {Quarter} AND map_trans.State = '{selected_state}' AND map_trans.District_name IS NOT NULL GROUP BY map_trans.State, map_trans.District_name, map_trans.Year, map_trans.Quarter ORDER BY map_trans.State, map_trans.District_name")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter', 'Total_Transaction_Count','Total_Transaction_Amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transaction_Count",
                     orientation='v',
                     color='Total_Transaction_Amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

# Users         
    if Type == "Users":

        #State
        st.markdown("### :white[State]")
        cursor.execute(f"SELECT agg_user.State, SUM(agg_user.Registered_users) AS Total_Users, sum(agg_user.App_opens) AS Total_Appopens FROM agg_user WHERE agg_user.Year = {Year} and agg_user.Quarter = {Quarter} GROUP BY agg_user.State ORDER BY Total_Users DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        fig = px.pie(df, values='Total_Users',
                            names='State',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Appopens'],
                            labels={'Total_Appopens':'Total_Appopens'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
        
        #District
        st.markdown("### :white[District]")
        cursor.execute(f"select map_user.District_name, SUM(District_registered_users) AS Total_Users, SUM(District_app_opens) AS Total_Appopens FROM map_user WHERE map_user.Year = {Year} AND map_user.Quarter = {Quarter} GROUP BY District_name ORDER BY Total_Users DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.pie(df, values='Total_Users',
                            names='District',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Appopens'],
                            labels={'Total_Appopens':'Total_Appopens'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
            
        #Pincode
        st.markdown("### :white[Pincode]")
        cursor.execute(f"SELECT top_user.Pincode, SUM(Pincode_registered_users) AS Total_Users FROM top_user WHERE top_user.Year = {Year} AND top_user.Quarter = {Quarter} GROUP BY Pincode ORDER BY Total_Users DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
        fig = px.pie(df, values='Total_Users',
                            names='Pincode',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

        #District vs. Total Users
        st.markdown("## :white[District vs. Total Users]")
        selected_state = st.selectbox("Select a state:", ('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 
                                                          'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 
                                                          'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 
                                                          'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 
                                                          'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
                                                          'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 
                                                          'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 
                                                          'Uttarakhand', 'West Bengal'), index=None, placeholder="Select a state...")
        
        cursor.execute(f"SELECT map_user.State, map_user.Year, map_user.Quarter, map_user.District_name, SUM(map_user.District_registered_users) AS Total_Users, SUM(map_user.District_app_opens) AS Total_Appopens FROM map_user WHERE map_user.Year = {Year} AND map_user.Quarter = {Quarter} AND map_user.State = '{selected_state}' GROUP BY map_user.State, map_user.District_name, map_user.Year, map_user.Quarter ORDER BY map_user.State, map_user.District_name")
        
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Year', 'Quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
    
    connect_for_int_dash.close()        