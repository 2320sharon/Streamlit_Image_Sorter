from turtle import onclick
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image
import os
import glob
from datetime import datetime
import csv

# Initialize Sniffer's states
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0
if 'csv_file' not in st.session_state:
    st.session_state.csv_file=None
if 'df' not in st.session_state:
    st.session_state.df=pd.DataFrame(columns=['Filename','Sorted','Index'])

    
def create_csv(csv_filename=None):
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
        csv_path = csv_filename
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        filename = f"Sniffer_Output_" + d1 + ".csv"
        csv_path = filename
    with open(csv_path, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(["Filename", "Sorted", "index"])
    return csv_path

def yes_button():
    if -1 < st.session_state.img_idx < len(images_list)-1:
        if st.session_state.csv_file is None: 
            st.session_state.csv_file=create_csv()
        row={"Filename":images_list[st.session_state.img_idx],'Sorted':"good",'Index':st.session_state.img_idx}
        # st.session_state.df=st.session_state.df.append(row,ignore_index=True)
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        with open(st.session_state.csv_file, 'a', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow([images_list[st.session_state.img_idx], "good",  st.session_state.img_idx])
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == len(images_list)-1:
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx} {len(images_list)}')

def no_button():
    if -1 < st.session_state.img_idx < len(images_list)-1:
        if st.session_state.csv_file is None: 
            st.session_state.csv_file=create_csv()
        row={"Filename":images_list[st.session_state.img_idx],'Sorted':"bad",'Index':st.session_state.img_idx}
        # st.session_state.df=st.session_state.df.append(row,ignore_index=True)
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        with open(st.session_state.csv_file, 'a', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow([images_list[st.session_state.img_idx], "bad",  st.session_state.img_idx])
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == len(images_list)-1:
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning('No more images to sort')

def undo_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= 1
        drop_filename=images_list[st.session_state.img_idx]
        print(f"drop_filename: {drop_filename}")
        index=st.session_state.df.loc[st.session_state.df['Filename'] == drop_filename].index.values
        st.session_state.df.drop(index, axis=0, inplace=True)
    else:
        st.warning('Cannot Undo')

images_list = glob.glob1("./images", "*jpg")
image = Image.open("./images"+os.sep+images_list[st.session_state.img_idx])

st.title("Sniffer")
st.write( st.session_state.img_idx)
st.write(st.session_state.df)
my_bar = st.progress(st.session_state.img_idx/(len(images_list)-1))


col1,col2,col3=st.columns(3)
with col1:
    st.button(label="Yes",key="yes_button",on_click=yes_button)
    st.button(label="No",key="no_button",on_click=no_button)
    st.button(label="Undo",help="Undo the last sort",key="undo_button",on_click=undo_button)
    
with col2:
    st.image(image, caption=f'Image #{st.session_state.img_idx}',width=300)

st.dataframe(st.session_state.df)



# Button to download the CSV file generated
# @st.cache
# def convert_df(df):
#      # IMPORTANT: Cache the conversion to prevent computation on every rerun
#      return df.to_csv().encode('utf-8')

# csv = convert_df(my_large_df)

# st.download_button(
#      label="Download data as CSV",
#      data=csv,
#      file_name='large_df.csv',
#      mime='text/csv',
#  )

# Upload images button
# HERE