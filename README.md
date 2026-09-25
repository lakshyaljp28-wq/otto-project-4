# Air Standard Otto Cycle Simulator

Interactive Streamlit web app for calculating Air-Standard Otto Cycle thermal efficiency, mean effective pressure (MEP), state properties, and plotting the P-V diagram.

## Files
- `app.py` - Main Streamlit application
- `requirements.txt` - Required Python libraries

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Upload `app.py` and `requirements.txt` to a GitHub repository and deploy `app.py` using Streamlit Community Cloud.

## Assumptions
- Air-standard Otto cycle
- Ideal gas
- Constant specific heats
- gamma = 1.4
- R = 287 J/(kg K)
