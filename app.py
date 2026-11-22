from pathlib import Path
import html
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CarePulse | Readmission Insights", page_icon="💙", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
:root{--navy:#10243c;--teal:#087f82;--muted:#64748b}
html,body,[class*="css"],.stApp{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(circle at 85% 0%,#e2f6f3 0%,transparent 34%),linear-gradient(160deg,#f7fbfe,#f0f6fa 65%,#f6fafc);color:var(--navy)}
.block-container{max-width:1120px;padding-top:1.35rem;padding-bottom:3rem}
header[data-testid="stHeader"]{background:transparent}
h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.035em;color:#10243c}
.brandbar{display:flex;justify-content:space-between;align-items:center;padding:9px 0 22px;gap:12px;flex-wrap:wrap}
.brand{font-family:Manrope,sans-serif;font-size:1.13rem;font-weight:800;color:#10243c}
.brandmark{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:11px;background:#0c7d83;color:white;margin-right:9px}
.brandtag{font-size:.78rem;font-weight:700;color:#087f82;background:#e1f5f1;border:1px solid #c2e8e2;border-radius:100px;padding:8px 12px}
.hero{position:relative;overflow:hidden;border-radius:26px;background:linear-gradient(118deg,#122b48 0%,#16465b 54%,#0b7d7c 100%);padding:42px 44px 46px;box-shadow:0 16px 35px #123c4d20;margin-bottom:25px}
.hero:before{content:'';position:absolute;width:350px;height:350px;border:1px solid #ffffff24;border-radius:50%;right:-55px;top:-140px;box-shadow:0 0 0 60px #ffffff08,0 0 0 125px #ffffff06}
.hero .eyebrow{color:#9de6d9;font-size:.76rem;letter-spacing:.16em;font-weight:800;text-transform:uppercase;margin-bottom:14px}
.hero h1{position:relative;max-width:660px;font-size:clamp(2rem,4.1vw,3.25rem);line-height:1.13;color:white!important;margin:0 0 15px;font-weight:800}
.hero p{position:relative;color:#d3e9ed;max-width:610px;font-size:1.03rem;line-height:1.7;margin:0}
.hero-pills{display:flex;gap:9px;flex-wrap:wrap;margin-top:24px;position:relative}
.hero-pills span{border:1px solid #ffffff3c;background:#ffffff12;border-radius:100px;padding:7px 12px;color:#e9faf9;font-size:.79rem;font-weight:600}
.section-head{margin:18px 0 12px}.section-head h2{font-size:1.5rem;margin:0 0 5px}.section-head p{font-size:.91rem;color:#607588;margin:0}
[data-testid="stForm"]{background:#ffffff;border:1px solid #e0ebf1;border-radius:22px;padding:27px 27px 23px;box-shadow:0 8px 32px #18334a0b}
[data-testid="stForm"] label{font-weight:700;color:#203950}
[data-testid="stForm"] [data-baseweb="select"]>div,[data-testid="stForm"] [data-baseweb="input"]>div{border-radius:11px;background:#f8fbfd;border-color:#dbe6eb;min-height:47px}
[data-testid="stForm"] button[kind="primary"]{background:linear-gradient(100deg,#087f82,#0c9b94);color:white;border:0;border-radius:12px;min-height:52px;font-weight:800;font-size:1rem;box-shadow:0 8px 18px #0b85842c}
[data-testid="stForm"] button[kind="primary"]:hover{background:#096e73;color:white;border:0}
.info-strip{display:flex;gap:12px;align-items:center;border-radius:14px;background:#e9f7f5;border:1px solid #d3ebe8;padding:13px 17px;color:#35646b;font-size:.85rem;margin-top:16px}
.result-panel{background:#fff;border:1px solid #dce9ed;border-radius:22px;padding:28px;box-shadow:0 10px 32px #12384b0d;margin:18px 0}
.result-top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.result-kicker{font-size:.75rem;letter-spacing:.13em;font-weight:800;color:#64788a;text-transform:uppercase}
.result-score{font-family:Manrope,sans-serif;font-size:clamp(2.8rem,7vw,4.4rem);font-weight:800;line-height:1.2;letter-spacing:-.06em;color:#087f82;margin:8px 0 14px}
.meter{height:13px;background:#e7eff2;border-radius:50px;overflow:hidden;margin:4px 0 14px}.meter-fill{height:100%;background:linear-gradient(90deg,#19b7a6,#087f82);border-radius:50px}
.classification{font-weight:800;color:#16384d;margin-bottom:8px}.result-note{font-size:.86rem;color:#627688;line-height:1.6}
.feature-card{background:#fff;border:1px solid #e1eaf0;border-radius:16px;padding:18px;min-height:112px;box-shadow:0 5px 18px #12384b08}
.feature-icon{font-size:1.4rem;margin-bottom:8px}.feature-title{font-weight:800;font-size:.94rem;color:#183b50}.feature-copy{font-size:.8rem;color:#718294;margin-top:4px;line-height:1.5}
.footer{font-size:.8rem;color:#687f8d;line-height:1.7;margin-top:12px;padding:12px 2px}
@media(max-width:650px){.hero{padding:30px 24px}.hero h1{font-size:2rem}[data-testid="stForm"]{padding:18px}.result-panel{padding:20px}}
</style>""", unsafe_allow_html=True)

st.markdown('''<div class="brandbar"><div class="brand"><span class="brandmark">✚</span> CarePulse <span style="color:#9aafbd;font-weight:500">/ AI Lab</span></div><div class="brandtag">● Educational demonstration</div></div>''', unsafe_allow_html=True)
st.markdown('''<section class="hero"><div class="eyebrow">Machine learning · Healthcare analytics</div><h1>Smarter insights into<br>hospital readmission.</h1><p>Explore how age, hospital stay, and number of diagnoses influence a machine-learning model's prediction of early readmission.</p><div class="hero-pills"><span>✦ Random Forest model</span><span>◷ 30-day readmission</span><span>▤ 3 patient inputs</span></div></section>''', unsafe_allow_html=True)

st.markdown('''<div class="section-head"><h2>Patient encounter details</h2><p>Enter three values to explore the model's estimated readmission score.</p></div>''', unsafe_allow_html=True)
with st.form("patient_form"):
    col1,col2,col3=st.columns(3, gap="medium")
    with col1:
        age=st.selectbox("Patient age group",options=[5,15,25,35,45,55,65,75,85,95],index=5,format_func=lambda v:f"{v-5}–{v+5} years",help="The model uses the midpoint of each 10-year age bracket.")
    with col2:
        stay=st.number_input("Hospital stay (days)",min_value=1,max_value=14,value=7,step=1,help="Length of the hospital encounter in days.")
    with col3:
        diagnoses=st.number_input("Number of diagnoses",min_value=1,max_value=30,value=3,step=1,help="Number of recorded diagnoses for the encounter.")
    st.write("")
    submitted=st.form_submit_button("✦  Generate prediction",type="primary",use_container_width=True)

st.markdown('''<div class="info-strip">🔒 &nbsp;Use fictional or de-identified inputs only. This demonstration does not collect patient names or IDs.</div>''', unsafe_allow_html=True)

MODEL_PATH=Path(__file__).with_name("hospital_readmission_3features.pkl")
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

if submitted:
    if not MODEL_PATH.exists():
        st.error("Model file missing: upload hospital_readmission_3features.pkl beside app.py in GitHub.")
    else:
        try:
            model=load_model()
            patient=pd.DataFrame([{"age":int(age),"time_in_hospital":int(stay),"number_diagnoses":int(diagnoses)}])
            probability=float(model.predict_proba(patient)[0,1])*100
            predicted=int(model.predict(patient)[0])
            score=f"{probability:.2f}%"
            label="Early readmission (class 1)" if predicted else "No early readmission (class 0)"
            st.markdown(f'''<div class="result-panel"><div class="result-top"><span class="result-kicker">Model estimate · Readmission within 30 days</span><span style="color:#0b817e;font-weight:800;font-size:.8rem">● Prediction ready</span></div><div class="result-score">{html.escape(score)}</div><div class="meter"><div class="meter-fill" style="width:{probability:.4f}%"></div></div><div class="classification">Classification: {html.escape(label)}</div><div class="result-note">This is an uncalibrated machine-learning score, not a clinically validated risk probability. The classification uses the model's default decision threshold.</div></div>''',unsafe_allow_html=True)
            with st.expander("View exact inputs used by the model"):
                st.dataframe(patient,use_container_width=True,hide_index=True)
        except Exception as exc:
            st.error(f"Could not generate prediction: {exc}")
            st.info("If you see a SimpleImputer attribute error, match the scikit-learn version in requirements.txt to the version used when saving the model in Colab, then redeploy.")

st.markdown('''<div class="section-head" style="margin-top:30px"><h2>How it works</h2><p>A simple demonstration of machine-learning inference using historical encounter data.</p></div>''',unsafe_allow_html=True)
a,b,c=st.columns(3,gap="medium")
with a:st.markdown('''<div class="feature-card"><div class="feature-icon">🧾</div><div class="feature-title">1. Enter details</div><div class="feature-copy">Select an age bracket and enter stay duration and diagnosis count.</div></div>''',unsafe_allow_html=True)
with b:st.markdown('''<div class="feature-card"><div class="feature-icon">🧠</div><div class="feature-title">2. Run the model</div><div class="feature-copy">A saved Random Forest processes the three encounter features.</div></div>''',unsafe_allow_html=True)
with c:st.markdown('''<div class="feature-card"><div class="feature-icon">📊</div><div class="feature-title">3. Explore the output</div><div class="feature-copy">Review the model score and its predicted readmission class.</div></div>''',unsafe_allow_html=True)

st.markdown('''<div class="footer"><strong>Research and teaching use only.</strong> Built from a historical diabetes hospital encounter dataset. This tool is not a validated medical device and must not be used for clinical diagnosis, treatment, discharge, or patient-care decisions. No identifiable patient data should be entered.</div>''',unsafe_allow_html=True)
