# Hospital Readmission Predictor — Local Website

## 1. Put your trained model in this folder
Copy the model downloaded from Google Colab into this folder, named exactly:
`hospital_readmission_3features.pkl`

The model must be the **3-feature model** trained on numeric age midpoints, `time_in_hospital`, and `number_diagnoses`. The model file is not included in this starter package.

## 2. Run locally on Windows
Install Python 3.10+ if needed. Double-click `start_windows.bat`, or open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Open http://localhost:8501 on your own machine.

## 3. Share with a public HTTPS link (Cloudflare Quick Tunnel)
Install `cloudflared` from Cloudflare's official documentation: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

Keep Streamlit running in its terminal. In a **second** terminal run:

```bash
cloudflared tunnel --url http://localhost:8501
```

Cloudflare will print a temporary `https://...trycloudflare.com` link. Share that link with testers. The link works while both Streamlit and cloudflared remain running and your computer is online. Quick Tunnel links can change when restarted and are intended for testing, not production uptime.

## Safety and privacy
Only load your own trusted `.pkl` file. Pickle files can execute code when loaded. Do not accept real patient identifiers or use this model for clinical decisions. This model's original evaluation showed weak sensitivity; validate performance before making any consequential claims. For long-term public hosting use a managed deployment, access controls, monitoring and an appropriate privacy review.

## Troubleshooting
- `Model file not found`: place the `.pkl` beside `app.py`.
- `ModuleNotFoundError`: rerun `python -m pip install -r requirements.txt`.
- Scikit-learn version warning: match the version used in Colab when you saved the model.
- Port 8501 busy: stop the previous Streamlit process before restarting.
