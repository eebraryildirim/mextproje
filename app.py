import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from PyPDF2 import PdfReader
from pages_2.dataset import dataset_function
from pdf2image import convert_from_path
import io
import matplotlib.pyplot as plt

st.header("Uygulama v1")
