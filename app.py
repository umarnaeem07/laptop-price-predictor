import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the model and dataframe
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

st.title("Laptop Price Predictor")

# Brand
company = st.selectbox('Brand', df['Company'].unique())

# Type of laptop
type = st.selectbox('Type', df['TypeName'].unique())

# RAM
ram = st.selectbox('RAM (in GB)', [2,4,6,8,12,16,24,32,64])

# Weight
weight = st.number_input('Weight of the Laptop (in kg)')

# Touchscreen
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])

# IPS
ips = st.selectbox('IPS', ['No', 'Yes'])

# Screen Size
screen_size = st.number_input('Screen Size (in inches)')

# Resolution
resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])

# CPU
cpu = st.selectbox('CPU Brand', df['Cpu brand'].unique())

# HDD
hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1000, 2000])

# SSD
ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1000])

# GPU
gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())

# OS
os = st.selectbox('OS', df['os'].unique())

if st.button('Predict Price'):
    if screen_size == 0.0:
        st.error('Please enter a valid screen size.')
    else:
        # Query point formatting
        ppi = None
        if touchscreen == 'Yes':
            touchscreen = 1
        else:
            touchscreen = 0

        if ips == 'Yes':
            ips = 1
        else:
            ips = 0

        X_res = int(resolution.split('x')[0])
        Y_res = int(resolution.split('x')[1])

        ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size

        query = pd.DataFrame(
            [[company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os]],
            columns=['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 'Ips', 'ppi', 'Cpu brand', 'HDD', 'SSD', 'Gpu brand', 'os']
        )

        prediction = pipe.predict(query)
        st.title(f"The predicted price of this laptop is ₹{int(np.exp(prediction[0]))}")
