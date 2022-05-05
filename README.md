# Streamlit Customizable Image Sorter 📸
Do you want to apply your own custom functions to your imagery and preview what they look like? 
Well this simple streamlit tool lets you create your own function to modify your imagery, preview what they would look like, then download the modified images.
![image_sorter_github_v1](https://user-images.githubusercontent.com/61564689/167033099-14d10ec5-7fb2-490d-b471-b14f2ebffbee.gif)



## How to Use it 📊
1. Fork Your own copy or clone this repo.
2. Replace the `enhance_img` with your custom function.
![Picture of function to replace](https://user-images.githubusercontent.com/61564689/167032293-8033963e-8ae9-4154-8853-1b72fa3af971.jpg)

3. Make sure your custom function returns a `PIL.Image.Image` otherwise the program won't function properly.
4. Run the command `streamlit run sorter.py` in the directory where your program is located.

## Features ‼️
1. Preview the modified images made by your custom function with preview mode.
2. Apply your custom function image by image and download the individual images.
3. Apply your custom function to all the images at once and download the `.zip`

## Tips for Customization 🎨
1. Check out the offical [Streamlit Docs](https://docs.streamlit.io/) for adding cool components like dropdown menus and more!

## How to Install Streamlit
[Check out Streamlit's Instructions](https://docs.streamlit.io/library/get-started/installation)

## Disclaimers ⚠️
1. This version outputs all images as `.jpg`.
