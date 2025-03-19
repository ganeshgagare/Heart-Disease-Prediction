import streamlit as st
import plotly.graph_objects as go
import numpy as np

def plot_feature_importance(features, importance_scores):
    """
    Create a bar plot of feature importance
    """
    feature_names = [
        'Mean Intensity',
        'Std Intensity',
        '25th Percentile',
        '75th Percentile',
        'Contour Area',
        'Contour Length',
        'Freq Mean',
        'Freq Std',
        'Freq Max'
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=feature_names,
            y=importance_scores,
            marker_color='lightblue'
        )
    ])
    
    fig.update_layout(
        title="Feature Importance",
        xaxis_title="Features",
        yaxis_title="Importance Score",
        xaxis_tickangle=-45
    )
    
    return fig

def display_results(prediction, confidence, features):
    """
    Display classification results with styling
    """
    result = "Normal" if not prediction else "Abnormal"
    color = "green" if not prediction else "red"
    
    st.markdown(
        f"""
        <div style='
            padding: 20px;
            border-radius: 10px;
            background-color: {color}22;
            border: 2px solid {color}
        '>
            <h2 style='color: {color}'>Classification: {result}</h2>
            <p>Confidence: {confidence:.2%}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
