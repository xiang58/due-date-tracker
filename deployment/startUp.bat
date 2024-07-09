@echo OFF
cd ..
if not exist ".venv" (
    py -m venv .venv
)
set STREAMLIT_ENV=dev
.venv\Scripts\activate && pip install -r requirements.txt && streamlit run src\app.py --server.headless true
