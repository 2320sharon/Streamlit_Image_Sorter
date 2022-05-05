import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image,ImageEnhance
from datetime import datetime
from io import BytesIO
import zipfile


uploaded_files = st.file_uploader("Choose a jpg file",type=['png', 'jpg','jpeg'], accept_multiple_files=True)
for uploaded_file in uploaded_files:
     bytes_data = uploaded_file.read()
images_list=uploaded_files

with st.sidebar:
    st.title("Settings")
    preview_selection = st.radio(
        "Would you like to  preview your images?",
        ('Yes', 'No'),index=1)


# Initialize the session state to have the current image index=0
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0

# Ensure img_idx will always be within images_list
if st.session_state.img_idx > (len(images_list)):
    st.session_state.img_idx = (len(images_list)-1) if (len(images_list)-1)>0 else 0


def next_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1)   :
        st.session_state.img_idx += 1
    elif st.session_state.img_idx ==(len(images_list)):
        st.success('All images have been sorted!')
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx} /{ len(images_list)} ')


def back_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= 1
    else:
        st.warning('Cannot Undo')

if images_list==[]:
    image= Image.open("./assets/new_loading_sniffer.jpg")
else:
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
    else:
        image = Image.open(images_list[st.session_state.img_idx])


# Sets num_image=1 if images_list is empty
num_images=(len(images_list)) if (len(images_list))>0 else 1


try:
    my_bar = st.progress((st.session_state.img_idx)/num_images)
except st.StreamlitAPIException:
    my_bar = st.progress(0)


col1,col2,col3,col4=st.columns(4)
with col1:
    st.button(label="Next",key="next_button",on_click=next_button)
    st.button(label="Back",key="back_button",on_click=back_button)
    
with col2:
    # Display done.jpg when all images are sorted 
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
        st.image(image,width=300)
    else:
        # caption is "" when images_list is empty otherwise its image name 
        caption = '' if images_list==[] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
        st.image(image, caption=caption,width=300)

# EXAMPLE FUNCTIONS THAT CAN BE APPLIED  TO IMAGES
# --------------------------------------------------------
# 1. Replace this function with your custom function you want to apply to your imagery.
# 2. Ensure it returns PIL.Image.Image
def enhance_img(image:"PIL.JpegImagePlugin.JpegImageFile")->'PIL.Image.Image':
    image_copy=image.copy()
    enhancer = ImageEnhance.Contrast(image_copy)
    im_output = enhancer.enhance(3)
    return im_output
# --------------------------------------------------------

def create_zip():
    names=list(map(lambda n:n.name,images_list))
    #Add your function to apply to all the images.Replace enhance_img with your own function
    pil_imgs=[]
    for result in images_list:
       pil_imgs.append(enhance_img(Image.open(result)))
    # BytesIO Buffer holds all images as bytes this later  be used to create zip file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # For each image save it to its own bytes buffer then save it to zipfile's buffer
        for cnt,file_name in enumerate(names):
            img_buffer = BytesIO()
            pil_imgs[cnt].save(img_buffer,format="JPEG")
            zip_file.writestr(file_name, img_buffer.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

def create_img_download():
    """create_img_download returns a BytesIO buffer with the data for the image at the current img_index
     after applying the custom function (in this example enhance_img())

    Example #1:
    enhance_img() is the function applied to the current image. It returns a Pil.Image.Image with contrast increased.
    This function is applied to the image before it is saved to the BytesIO buffer,so that the downloaded image has
    the higher contrast applied to it.

    Returns:
        BytesIO: buffer containing the modified image data
    """
    img_index=st.session_state.img_idx
    # download the last image if the user has already seen it
    if img_index>=len(images_list):
        img_index=(len(images_list)-1)
    # Make sure the images list is not empty and the index is valid
    if 0<=img_index<(len(images_list)) and images_list !=  []:
        img=images_list[img_index]
        # Open the image before passing to the your custom function
        img = Image.open(img)
        # Modify the following line to use your custom function. Ensure your function returns PIL.Image.Image
        result_img=enhance_img(img)
        # Shows a mini preview of the image to download
        if preview_selection == 'Yes':
            st.image(result_img)
        buffer=BytesIO()
        # Save the modified image to the buffer as a JPEG file
        # Modify the following line if you want to save in another format (ex. PNG)
        result_img.save(buffer,format="JPEG")
        # Get the download ready bytes from the buffer 
        byte_im=buffer.getvalue()
        return byte_im
        

with col4:
    
    if len(images_list)>0 :
        # current image index is used to create the file name for download_img_button
        img_index=min((len(images_list)-1),st.session_state.img_idx)

        download_zip_button=st.download_button(
        label="Download this Image ⛺",
        data=create_img_download(),
        file_name= images_list[img_index].name,
        mime='image/jpg',
        )
    
        download_img_button=st.download_button(
        label="Download All Images as .zip 📦",
        data=create_zip(),
        file_name= "dataset.zip",
        )
