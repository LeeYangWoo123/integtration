@echo off
echo [1/2] Verifying installation of required libraries and graph engines...
python -m pip install streamlit sympy numpy matplotlib

echo.
echo [2/2] Run the program...
python -m streamlit run app.py
pause