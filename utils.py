import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import pandas as pd

@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

def analyze_shelf(img):
    model = load_model()
    
    # ✅ CORRECT YOLOv8 PARAMETERS (imgsz, not size)
    results = model(img, imgsz=960, conf=0.3, iou=0.5, verbose=False)[0]
    
    # Get detections safely
    if results.boxes is not None and len(results.boxes) > 0:
        counts = results.boxes.cls.cpu().numpy()  # Class IDs
        df = pd.DataFrame({'class': counts})
        counts_dict = df['class'].value_counts().to_dict()
        total_stock = len(counts)
    else:
        counts_dict = {}
        total_stock = 0
    
    # Annotated image with labels
    annotated = results.plot()
    
    return annotated, counts_dict, total_stock





