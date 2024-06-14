import streamlit as st
import pickle
import numpy as np

# Load the model
model = pickle.load(open('Model.pkl', 'rb'))

# Custom CSS for styling
def set_custom_style():
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0;
            color: #333;
            font-family: Arial, sans-serif;
        }
        .stApp {
            max-width: 600px; /* Adjusted maximum width */
            padding: 2rem;
            margin: auto;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto; /* Centers the button */
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stTextInput > div > div > input {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 10px 14px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 0.1rem rgba(76, 175, 80, 0.25);
        }
        .stSelectbox > div > div > select {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 10px 14px;
            font-size: 16px;
            background-color: #fff;
            transition: border-color 0.3s ease;
        }
        .stSelectbox > div > div > select:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 0.1rem rgba(76, 175, 80, 0.25);
        }
        .stSlider > div > div > div {
            background-color: #4CAF50 !important; /* Green color for slider bar */
            border-radius: 10px; /* Rounded corners for slider bar */
            height: 8px; /* Height of the slider bar */
            margin-bottom: 16px; /* Space below the slider */
        }
        .stSlider > div > div > div > div {
            background-color: transparent !important; /* Transparent background for slider thumb */
            transition: background-color 0.3s ease;
            position: relative;
            height: 20px; /* Height of the slider thumb */
            width: 20px; /* Width of the slider thumb */
            margin-top: -16px; /* Adjust the vertical position of the slider thumb */
        }
        .stSlider > div > div > div > div:before {
            content: "";
            width: 10px;
            height: 10px;
            background-color: #4CAF50; /* Green color for slider thumb */
            border-radius: 50%;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        .stSlider > div > div > div > div > div {
            background-color: transparent !important; /* Transparent background for slider value */
            position: absolute;
            bottom: 100%; /* Position above the thumb */
            left: 50%;
            transform: translateX(-50%);
            color: black !important; /* Black color for slider value */
            padding: 5px 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .stSlider > div > div > div > div[data-baseweb='block'] {
            background-color: transparent !important;
            color: black !important;
        }
        .stSlider > div > div > div > div[data-baseweb='value'] {
            background-color: transparent !important;
            color: black !important;
        }
        .stSlider > div > div > div > div[data-baseweb='tick'] {
            background-color: transparent !important;
            color: black !important;
        }
        .stSlider > div > div > div > div[data-baseweb='tick'][data-index='0'],
        .stSlider > div > div > div > div[data-baseweb='tick'][data-index='1'] {
            background-color: transparent !important;
            color: black !important;
        }
        .stMarkdown {
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply custom styles
set_custom_style()

# Title and header with centered alignment
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #4CAF50;'>Heart Disease Prediction</h1>
        <p style='font-size: 18px;'>Predicting the likelihood of heart disease based on various factors</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input fields for the features
age = st.slider("Age", min_value=0, max_value=120, value=59, step=1)
sex = st.selectbox("Sex", ["Female", "Male"])
cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"])
trestbps = st.slider("Resting Blood Pressure (mm Hg)", min_value=80, max_value=200, value=140, step=1)
chol = st.slider("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=221, step=1)
fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["No", "Yes"])
restecg = st.selectbox("Resting Electrocardiographic Results", ["Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"])
thalach = st.slider("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=164, step=1)
exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
oldpeak = st.slider("ST Depression Induced by Exercise", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
slope = st.selectbox("Slope of the Peak Exercise ST Segment", ["Upsloping", "Flat", "Downsloping"])
ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy", [0, 1, 2, 3, 4])
thal = st.selectbox("Thalassemia", ["Normal", "Fixed Defect", "Reversible Defect"])

# Make prediction
if st.button("Predict"):
    sex_code = 1 if sex == "Male" else 0
    fbs_code = 1 if fbs == "Yes" else 0
    exang_code = 1 if exang == "Yes" else 0
    slope_code = slope.index(slope)
    thal_code = thal.index(thal)
    cp_code = cp.index(cp)
    restecg_code = restecg.index(restecg)
    
    features = np.array([[age, sex_code, cp_code, trestbps, chol, fbs_code, restecg_code, thalach, exang_code, oldpeak, slope_code, ca, thal_code]])
    prediction = model.predict(features)
    
    if prediction[0] == 1:
        st.success("The model predicts that the patient has heart disease.")
    else:
        st.success("The model predicts that the patient does not have heart disease.")

# Footer with attribution
st.markdown("---")
st.markdown("Created with ❤️ by Debadutta")
