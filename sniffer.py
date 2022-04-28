# from turtle import onclick
# from matplotlib.ticker import MaxNLocator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image
import os
import glob
from datetime import datetime

st.set_page_config(
     page_title="Sniffer",
     page_icon="🐕",
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "# Sniffer. Sort your *extremely* cool images!"
     }
 )

def create_csv_name(csv_filename:str=None)->str:
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        csv_filename = f"Sniffer_Output_" + d1 + ".csv"
    return csv_filename

# Initialize Sniffer's states
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0
if 'df' not in st.session_state:
    st.session_state.df=pd.DataFrame(columns=['Filename','Sorted','Index'])

def create_csv():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    st.session_state.df.to_csv().encode('utf-8')
    return st.session_state.df.to_csv().encode('utf-8')

def yes_button():
    if -1 < st.session_state.img_idx < len(images_list)-1:
        row={"Filename":images_list[st.session_state.img_idx],'Sorted':"good",'Index':st.session_state.img_idx}
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == len(images_list)-1:
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx} {len(images_list)}')

def no_button():
    if -1 < st.session_state.img_idx < len(images_list)-1:
        row={"Filename":images_list[st.session_state.img_idx],'Sorted':"bad",'Index':st.session_state.img_idx}
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
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
        index=st.session_state.df.loc[st.session_state.df['Filename'] == drop_filename].index.values
        st.session_state.df.drop(index, axis=0, inplace=True)
    else:
        st.warning('Cannot Undo')

images_list = glob.glob1("./images", "*jpg")
image = Image.open("./images"+os.sep+images_list[st.session_state.img_idx])

st.title("Sniffer🐕")
st.image("./assets/sniffer.jpg")
my_bar = st.progress(st.session_state.img_idx/(len(images_list)-1))


col1,col2,col3,col4=st.columns(4)
with col1:
    st.button(label="Yes",key="yes_button",on_click=yes_button)
    st.button(label="No",key="no_button",on_click=no_button)
    st.button(label="Undo",key="undo_button",on_click=undo_button)
    
with col2:
    st.image(image, caption=f'{images_list[st.session_state.img_idx]}',width=300)
    
with col4:
    st.download_button(
     label="Download data as CSV 💻",
     data=create_csv(),
     file_name= create_csv_name(),
     mime='text/csv',
 )

with st.expander("See Dataset Details 📈"):
    st.dataframe(st.session_state.df)
    st.bar_chart(st.session_state.df['Sorted'].value_counts())
