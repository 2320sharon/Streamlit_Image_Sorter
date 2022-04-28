import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
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

uploaded_files = st.file_uploader("Choose a jpg file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()
images_list=uploaded_files

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
    if -1 < st.session_state.img_idx < (len(images_list)-1)   :
        row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"good",'Index':st.session_state.img_idx}
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    if st.session_state.img_idx == len(images_list)-1:
        row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"good",'Index':st.session_state.img_idx}
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx} /{ len(images_list)} ')


def no_button():
    if -1 < st.session_state.img_idx < len(images_list)-1 :
        row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"bad",'Index':st.session_state.img_idx}
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == len(images_list)-1:
        row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"good",'Index':st.session_state.img_idx}
        st.session_state.df=pd.concat([st.session_state.df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx}/{ len(images_list)}')


def undo_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= 1
        drop_filename=images_list[st.session_state.img_idx].name
        index=st.session_state.df.loc[st.session_state.df['Filename'] == drop_filename].index.values
        st.session_state.df.drop(index, axis=0, inplace=True)
    else:
        st.warning('Cannot Undo')


if images_list==[]:
    image= Image.open("./assets/new_loading_sniffer.jpg")
else:
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
    else:
        image = Image.open(images_list[st.session_state.img_idx])

st.title("Sniffer🐕")
st.image("./assets/sniffer.jpg")
# Sets num_image=1 if images_list is empty
num_images=(len(images_list)) if (len(images_list))>0 else 1
my_bar = st.progress((st.session_state.img_idx)/num_images)


col1,col2,col3,col4=st.columns(4)
with col1:
    st.button(label="Yes",key="yes_button",on_click=yes_button)
    st.button(label="No",key="no_button",on_click=no_button)
    st.button(label="Undo",key="undo_button",on_click=undo_button)
    
with col2:
    # Display done.jpg when all images are sorted 
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
        st.image(image,width=300)
    else:
        # caption is none when images_list is empty otherwise it is the image name 
        caption = '' if images_list==[] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
        st.image(image, caption=caption,width=300)
    
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
