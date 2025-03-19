import streamlit as st
from PIL import Image
import numpy as np
import io
from datetime import datetime
import base64

from src.model import ECGClassifier
from src.preprocessor import ECGPreprocessor
from src.features import FeatureExtractor
from src.utils import plot_feature_importance, display_results
from src.database import save_analysis
from src.analysis import HealthAnalyzer

# Page config
st.set_page_config(
    page_title="ECG Analysis Tool",
    layout="wide"
)

# Initialize components
@st.cache_resource
def load_model():
    return ECGClassifier()

model = load_model()
health_analyzer = HealthAnalyzer()

# Title and description
st.title("ECG Analysis Tool")
st.markdown("""
This tool analyzes ECG images to classify heart conditions and provide health insights.
Upload a clear image of an ECG reading to get started.
""")

# File upload
uploaded_file = st.file_uploader(
    "Choose an ECG image",
    type=['png', 'jpg', 'jpeg']
)

if uploaded_file is not None:
    try:
        # Load and display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded ECG", use_container_width=True)

        with st.spinner("Processing ECG..."):
            # Preprocess image
            preprocessed = ECGPreprocessor.preprocess_image(image)

            # Extract features
            features = FeatureExtractor.extract_features(preprocessed)

            # Get prediction
            predicted_class, confidence = model.predict(features)

            # Display classification result
            st.subheader("Classification Result")
            
            # Map the predicted class to standardized output format
            class_description = {
                'COVID-19': "ECG images of COVID-19 patient",
                'Myocardial Infarction': "ECG images of Myocardial Infarction",
                'Abnormal Heartbeat': "ECG images of patient that have abnormal heart beats",
                'History of MI': "ECG images of patient having history of myocardial infarction",
                'Normal': "Normal person ECG Images"
            }
            
            description = class_description.get(predicted_class, predicted_class)
            
            st.markdown(f"""
            **Detected Condition:** {description}  
            **Confidence:** {confidence*100:.1f}%
            """)

            # Get health analysis for the predicted class
            health_analysis = health_analyzer.analyze_health(
                predicted_class,
                confidence
            )

            # Generate report
            report_name, report_html = health_analyzer.generate_report(
                predicted_class,
                health_analysis
            )

            # Save to database
            analysis = save_analysis(
                filename=uploaded_file.name,
                ecg_class=predicted_class,
                class_probabilities=confidence,
                features=features.tolist(),
                health_analysis=health_analysis,
                report_path=report_name
            )

            # Display preprocessed image and feature analysis
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Preprocessed ECG")
                st.image(preprocessed, caption="Preprocessed Image", use_container_width=True)

            with col2:
                st.subheader("Feature Analysis")
                importance_scores = np.abs(features) / np.sum(np.abs(features))
                fig = plot_feature_importance(features, importance_scores)
                st.plotly_chart(fig, use_container_width=True)

            # Display health analysis
            st.subheader("Health Analysis")
            st.write(f"**Status:** {health_analysis['health_status']}")
            st.write(f"**Risk Level:** {health_analysis['risk_level'].upper()}")
            st.write("**Symptoms and Causes:**")
            st.write(health_analysis['symptoms_causes'])
            st.write("**Recommendations:**")
            st.write(health_analysis['recommendations'])

            # Provide download link for report
            st.download_button(
                label="Download Report",
                data=report_html,
                file_name=report_name,
                mime="text/html"
            )

            # Display analysis timestamp
            st.info(f"Analysis saved at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
else:
    # Display sample image and instructions when no file is uploaded
    st.info("""
        Please upload an ECG image to begin analysis.

        Guidelines for best results:
        - Use clear, high-resolution images
        - Ensure the ECG grid is visible
        - Avoid blurry or distorted images
        - Supported formats: PNG, JPG, JPEG
    """)