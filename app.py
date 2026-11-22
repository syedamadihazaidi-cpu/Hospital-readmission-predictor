import os
from pathlib import Path
import pandas as pd
import streamlit as st
import joblib

st.set_page_config(page_title='Readmission AI | Patient Risk Explorer', page_icon='🩺', layout='centered')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(145deg,#f1f8fb 0%,#f9fbfd 52%,#eaf7f3 100%);color:#102a43;}
.block-container {max-width:860px;padding-top:2.2rem;}
.hero {background:linear-gradient(115deg,#103c55,#087e80);padding:34px;border-radius:24px;color:white;box-shadow:0 15px 35px #163b5320;margin-bottom:25px;}
.hero h1 {font-size:2.1rem;color:white;margin:0 0 8px;}
.hero p {color:#d9f5f2;margin:0;}
.small-label {font-size:.85rem;letter-spacing:.12em;text-transform:uppercase;color:#bbf7e5;font-weight:700;}
.result {background:white;border:1px solid #dce9ec;border-radius:20px;padding:25px;margin-top:20px;box-shadow:0 8px 24px #0a3e5020;}
.score {font-size:3.5rem;font-weight:700;color:#087e80;line-height:1.2;}
.disclaimer {font-size:.88rem;color:#526d7b;}
div.stButton > button[kind="primary"] {background:#087e80;border-radius:12px;border:0;font-weight:700;padding:0.65rem 1.5rem;}
</style>''', unsafe_allow_html=True)

st.markdown('''<section class="hero"><div class="small-label">Healthcare analytics lab</div><h1>🩺 Hospital Readmission Predictor</h1><p>Explore a machine-learning model using just three patient encounter details.</p></section>''', unsafe_allow_html=True)

MODEL_PATH = Path(__file__).with_name('hospital_readmission_3features.pkl')
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.subheader('Enter patient details')
st.caption('This model was trained using age-group midpoints, hospital stay and number of diagnoses.')
with st.form('patient'):
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.selectbox('Age (years)', [5,15,25,35,45,55,65,75,85,95], index=5, help='Age is represented by the midpoint of a 10-year category.')
    with c2:
        stay = st.number_input('Hospital stay (days)', min_value=1, max_value=14, value=7, step=1)
    with c3:
        diagnoses = st.number_input('Number of diagnoses', min_value=1, max_value=30, value=3, step=1)
    submitted = st.form_submit_button('Analyze patient', type='primary', use_container_width=True)

if submitted:
    if not MODEL_PATH.exists():
        st.error('Model file not found. Place hospital_readmission_3features.pkl in the same folder as app.py.')
    else:
        try:
            model = load_model()
            patient = pd.DataFrame([{'age': age, 'time_in_hospital': stay, 'number_diagnoses': diagnoses}])
            score = float(model.predict_proba(patient)[0, 1]) * 100
            pred = int(model.predict(patient)[0])
            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.caption('MODEL ESTIMATE · EARLY READMISSION')
            st.markdown(f'<div class="score">{score:.2f}%</div>', unsafe_allow_html=True)
            st.progress(min(max(score / 100, 0), 1))
            st.markdown('**Model classification:** ' + ('Early readmission (1)' if pred else 'No early readmission (0)'))
            st.caption('The classification uses the trained model’s default decision threshold. The score is not a calibrated clinical risk estimate.')
            st.markdown('</div>', unsafe_allow_html=True)
            with st.expander('View model inputs'):
                st.dataframe(patient, hide_index=True, use_container_width=True)
        except Exception as exc:
            st.error(f'Could not generate prediction: {exc}')

st.divider()
st.markdown('**About this demonstration**')
st.markdown('<p class="disclaimer">Based on a historical diabetes hospital encounter dataset. This is an educational model, not a validated medical device. Do not use its output for diagnosis, treatment, discharge, or other clinical decisions. Do not enter personally identifiable patient information.</p>', unsafe_allow_html=True)
