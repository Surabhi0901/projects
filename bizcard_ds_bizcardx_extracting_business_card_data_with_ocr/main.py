#Importing necessary libraries

import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3

#Initializing the session state

if 'concat_df' not in st.session_state:
    st.session_state.concat_df = None

#Setting up the page

st.set_page_config(page_title= "Business Card Information Extraction using OCR| By Surabhi Yadav",
                   page_icon= ":🪪:", 
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by *Surabhi Yadav!*"""})

with st.sidebar:

  select= option_menu("Main Menu", ["Upload", "Modify", "Delete"],
                      icons=["upload", "funnel-fill", "trash3-fill"], 
                      menu_icon="menu-up",
                      default_index=0,
                      orientation="vertical",
                      styles={"nav-link": {"font-size": "15px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#007acc"},
                                   "icon": {"font-size": "15px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#007acc"}})

#Converting image to text

def image_to_text(path):

  image_input = Image.open(path)
  image_array = np.array(image_input)
  reader = easyocr.Reader(['en'])
  text = reader.readtext(image_array, detail= 0)
  return text, image_input

#Extracting text from image

states_with_gaps = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
                    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
                    "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]

states_without_gaps = ["AndhraPradesh", "ArunachalPradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "HimachalPradesh",
                       "Jharkhand", "Karnataka", "Kerala", "MadhyaPradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
                       "Punjab", "Rajasthan", "Sikkim", "TamilNadu", "Telangana", "Tripura", "UttarPradesh", "Uttarakhand", "WestBengal"]

def extracted_text(text):
    extracted_dict = {
        "NAME": [],
        "DESIGNATION": [],
        "COMPANY_NAME": [], 
        "CONTACT": [],
        "EMAIL": [],
        "WEBSITE": [],
        "ADDRESS": [],
        "PINCODE": []
    }

    extracted_dict["NAME"].append(text[0])
    extracted_dict["DESIGNATION"].append(text[1])

    for i in range(2, len(text)):
        if text[i].startswith("+") or (text[i].replace("-", "").isdigit() and '-' in text[i]):
            extracted_dict["CONTACT"].append(text[i])
        elif "@" in text[i] and ".com" in text[i]:
            extracted_dict["EMAIL"].append(text[i])
        elif "WWW" in text[i] or "www" in text[i] or "Www" in text[i] or "wWw" in text[i] or "wwW" in text[i]:
            small = text[i].lower()
            extracted_dict["WEBSITE"].append(small)
        elif any(state in text[i] for state in states_with_gaps) or any(state in text[i] for state in states_without_gaps) or text[i].isdigit():
            extracted_dict["PINCODE"].append(text[i])
        elif re.match(r'^[A-Za-z]', text[i]):
            extracted_dict["COMPANY_NAME"].append(text[i])
        else:
            remove_colon = re.sub(r'[,;]', '', text[i])
            extracted_dict["ADDRESS"].append(remove_colon)

    for key, value in extracted_dict.items():
        if len(value) > 0:
            joined_value = " ".join(value)
            extracted_dict[key] = [joined_value]
        else:
            value = "NA"
            extracted_dict[key] = [value]

    return extracted_dict

#Uploading the image

if select == "Upload":

  st.header("Bizcard Information Upload & Storage", divider="blue")
  st.write("")
  
  st.subheader("Upload the business card here")
  img = st.file_uploader(label = "", type= ["png","jpg","jpeg"])

  #Displaying the image
  if img is not None:
    st.image(img, width= None)
    text_image, image_input= image_to_text(img)
    text_dict = extracted_text(text_image)

    if text_dict:
      st.success("Text from the image extracted successfully!")
      text_df = pd.DataFrame(text_dict)
    else:
      st.error("No text found in the image")
      text_df = pd.DataFrame(columns=["NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE", "ADDRESS", "PINCODE"])

    st.write("")
    st.write("")
    st.subheader("Extracted information:")
     #Converting image to bytes
    if text_dict: 
      image_bytes = io.BytesIO()
      image_input.save(image_bytes, format="PNG")
      image_data = image_bytes.getvalue()

      data = {"IMAGE": [image_data]}
      image_df = pd.DataFrame(data)
      concat_df = pd.concat([text_df, image_df], axis=1)
      st.session_state.concat_df = concat_df
      st.dataframe(concat_df)
    else:
      st.session_state.concat_df = text_df  
      st.dataframe(text_df)

    save_button = st.button("Save", use_container_width = True)

    if save_button:

      db = sqlite3.connect("bizcard_db")
      cursor = db.cursor()

      #Creating the table

      create_table_query = '''CREATE TABLE IF NOT EXISTS bizcard_tbl(name varchar(225),
                                                                          designation varchar(225),
                                                                          company_name varchar(225),
                                                                          contact varchar(225),
                                                                          email varchar(225),
                                                                          website text,
                                                                          address text,
                                                                          pincode varchar(225),
                                                                          image text)'''

      cursor.execute(create_table_query)
      db.commit()

      insert_query = '''INSERT INTO bizcard_tbl(name, designation, company_name, contact, email, website, address, pincode, image)
                                                    values(?,?,?,?,?,?,?,?,?)'''

      data_temp = st.session_state.concat_df.values.tolist()[0]
      cursor.execute(insert_query,data_temp)
      db.commit()

      st.success("Saved successfully!")

      #Fetching the entire data from the database table
      st.write("")
      st.subheader("The entire saved information:")
      db = sqlite3.connect("bizcard_db")
      cursor = db.cursor()
      select_query = "SELECT * FROM bizcard_tbl"
      cursor.execute(select_query)
      table = cursor.fetchall()
      db.commit()

      table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE", "ADDRESS", "PINCODE", "IMAGE"))

      st.dataframe(table_df)

#Modifying the text data

if select == "Modify":    
      
      st.header("Bizcard Information Modification & Storage", divider = "blue")
      st.write("")

      db = sqlite3.connect("bizcard_db")
      cursor = db.cursor()
      select_query = "SELECT * FROM bizcard_tbl"
      cursor.execute(select_query)
      table = cursor.fetchall()
      db.commit()

      table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE", "ADDRESS", "PINCODE", "IMAGE"))

      st.subheader("Select the name")
      selected_name = st.selectbox("", table_df["NAME"])
      st.write("")
      st.write("")

      temp_df = table_df[table_df["NAME"] == selected_name]

      copy_df = temp_df.copy() 

      if not temp_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            mdf_name = st.text_input("Name", temp_df["NAME"].iloc[0])
            mdf_designation = st.text_input("Designation", temp_df["DESIGNATION"].iloc[0])
            mdf_company_name = st.text_input("Company_name", temp_df["COMPANY_NAME"].iloc[0])
            mdf_contact = st.text_input("Contact", temp_df["CONTACT"].iloc[0])

            copy_df["NAME"] = mdf_name
            copy_df["DESIGNATION"] = mdf_designation
            copy_df["COMPANY_NAME"] = mdf_company_name
            copy_df["CONTACT"] = mdf_contact

        with col2:
            mdf_website = st.text_input("Website", temp_df["WEBSITE"].iloc[0])
            mdf_address = st.text_input("Address", temp_df["ADDRESS"].iloc[0])
            mdf_pincode = st.text_input("Pincode", temp_df["PINCODE"].iloc[0])
            mdf_email = st.text_input("Email", temp_df["EMAIL"].iloc[0])

            copy_df["WEBSITE"] = mdf_website
            copy_df["ADDRESS"] = mdf_address
            copy_df["PINCODE"] = mdf_pincode
            copy_df["EMAIL"] = mdf_email

        st.write("")
        st.write("")
        st.write("")
        st.subheader("Preview of the information being saved:")
        st.dataframe(copy_df)

        commit_button = st.button("Commit", use_container_width = True)

        if commit_button:

            db = sqlite3.connect("bizcard_db")
            cursor = db.cursor()

            cursor.execute(f"DELETE FROM bizcard_tbl WHERE NAME = '{selected_name}'")
            db.commit()

            insert_query = '''INSERT INTO bizcard_tbl(name, designation, company_name,contact, email, website, address, pincode, image)
                                                            values(?,?,?,?,?,?,?,?,?)'''

            data_temp = copy_df.values.tolist()[0]
            cursor.execute(insert_query,data_temp)
            db.commit()

            st.success("Modified Successfully!")

            st.write("")
            st.subheader("The entire saved information:")
            db = sqlite3.connect("bizcard_db")
            cursor = db.cursor()
            select_query = "SELECT * FROM bizcard_tbl"
            cursor.execute(select_query)
            table = cursor.fetchall()
            db.commit()

            table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE", "ADDRESS", "PINCODE", "IMAGE"))

            st.dataframe(table_df)

#Deleting an unnecessary entry

if select == "Delete":

  st.header("Bizcard Information Deletion", divider='blue')
  st.write("")
  
  db = sqlite3.connect("bizcard_db")
  cursor = db.cursor()

  col1,col2 = st.columns(2)
  with col1:

    cursor.execute("SELECT NAME FROM bizcard_tbl")
    name_table = cursor.fetchall()
    db.commit()

    names = []

    for i in name_table:
      names.append(i[0])

    st.subheader("Select the name")
    name_select = st.selectbox("", names, key="name_select")

  with col2:

    select_query = f"SELECT DESIGNATION FROM bizcard_tbl WHERE NAME ='{name_select}'"

    cursor.execute(select_query)
    designation_table = cursor.fetchall()
    db.commit()

    designations = []

    for i in designation_table:
      designations.append(i[0])

    st.subheader("Select the designation")
    designation_select = st.selectbox("", designations, key="designation_select")

  if name_select and designation_select:
    col1,col2 = st.columns(2)

    with col1:
      st.write(f"Selected Name : {name_select}")
      st.write("")
      st.write("")

    with col2:
      st.write(f"Selected Designation : {designation_select}")
      st.write("")

    remove_button = st.button("Delete", use_container_width= True)

    if remove_button:

      cursor.execute(f"DELETE FROM bizcard_tbl WHERE NAME ='{name_select}' AND DESIGNATION = '{designation_select}'")
      db.commit()

      st.warning("Deleted Succesfully!")