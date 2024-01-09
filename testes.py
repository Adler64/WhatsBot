from pathlib import Path
import streamlit as st
import glob
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from pathlib import Path
from time import sleep

if 'pagina_central' not in st.session_state:
    st.session_state.pagina_central = 'home'
    