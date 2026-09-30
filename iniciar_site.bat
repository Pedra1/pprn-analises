@echo off
chcp 65001 > nul
title Portal de Resultados PPRN - Policial Penal RN
cls
echo ==============================================================================
echo       PORTAL DE RESULTADOS - POLICIAL PENAL RN (PPRN)
echo ==============================================================================
echo.
echo Iniciando o servidor Streamlit...
echo Abrindo em http://localhost:8501
echo.
python -m streamlit run app.py
pause
