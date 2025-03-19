import json
from datetime import datetime

class HealthAnalyzer:
    def __init__(self):
        # Predefined analysis templates for each class
        self.analysis_templates = {
            'COVID-19': {
                'health_status': "Potential COVID-19 related cardiac manifestations detected",
                'risk_level': "high",
                'symptoms_causes': (
                    "Common symptoms include chest pain, shortness of breath, "
                    "arrhythmias, and myocardial injury. COVID-19 can affect "
                    "heart function through direct viral damage or inflammatory response."
                ),
                'recommendations': (
                    "1. Seek immediate medical attention\n"
                    "2. Monitor oxygen levels\n"
                    "3. Follow COVID-19 isolation protocols\n"
                    "4. Regular cardiac monitoring\n"
                    "5. Rest and proper medication as prescribed"
                )
            },
            'Myocardial Infarction': {
                'health_status': "Signs of Myocardial Infarction (Heart Attack) detected",
                'risk_level': "high",
                'symptoms_causes': (
                    "Critical condition indicating blocked blood flow to heart muscle. "
                    "Common causes include coronary artery blockage, blood clots, "
                    "and plaque buildup. Symptoms: severe chest pain, shortness of "
                    "breath, nausea, and cold sweats."
                ),
                'recommendations': (
                    "1. IMMEDIATE EMERGENCY MEDICAL ATTENTION REQUIRED\n"
                    "2. Take prescribed medications\n"
                    "3. Cardiac rehabilitation program\n"
                    "4. Lifestyle modifications\n"
                    "5. Regular follow-up with cardiologist"
                )
            },
            'Abnormal Heartbeat': {
                'health_status': "Irregular heart rhythm detected",
                'risk_level': "medium",
                'symptoms_causes': (
                    "Arrhythmia can be caused by heart disease, stress, medications, "
                    "or electrolyte imbalances. Symptoms may include palpitations, "
                    "dizziness, fatigue, and shortness of breath."
                ),
                'recommendations': (
                    "1. Consult a cardiologist\n"
                    "2. Monitor heart rate regularly\n"
                    "3. Avoid triggers (caffeine, stress)\n"
                    "4. Maintain balanced diet\n"
                    "5. Regular exercise as approved by doctor"
                )
            },
            'History of MI': {
                'health_status': "ECG indicates previous Myocardial Infarction",
                'risk_level': "medium",
                'symptoms_causes': (
                    "Previous heart attack has left characteristic changes in ECG. "
                    "This indicates increased risk for future cardiac events. "
                    "Regular monitoring and preventive care is essential."
                ),
                'recommendations': (
                    "1. Regular cardiac check-ups\n"
                    "2. Strict medication adherence\n"
                    "3. Heart-healthy diet\n"
                    "4. Supervised exercise program\n"
                    "5. Risk factor management"
                )
            },
            'Normal': {
                'health_status': "Normal ECG pattern",
                'risk_level': "low",
                'symptoms_causes': (
                    "ECG shows normal heart rhythm and conduction. No significant "
                    "abnormalities detected in the electrical activity of the heart."
                ),
                'recommendations': (
                    "1. Regular health check-ups\n"
                    "2. Maintain healthy lifestyle\n"
                    "3. Regular exercise\n"
                    "4. Balanced diet\n"
                    "5. Stress management"
                )
            }
        }

    def analyze_health(self, ecg_class, confidence):
        """
        Generate detailed health analysis based on ECG classification
        """
        try:
            # Get base analysis from template
            analysis = self.analysis_templates.get(ecg_class, self.analysis_templates['Normal']).copy()

            # Add confidence context
            if confidence < 0.5:
                analysis['health_status'] += " (Low confidence prediction - please consult healthcare provider)"

            return analysis

        except Exception as e:
            raise Exception(f"Failed to analyze health: {str(e)}")

    def generate_report(self, ecg_class, health_analysis):
        """Generate HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"ecg_report_{timestamp}.html"

        html_content = f"""
        <html>
        <head>
            <title>ECG Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f5f5f5; padding: 20px; border-radius: 10px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                .high-risk {{ color: red; }}
                .medium-risk {{ color: orange; }}
                .low-risk {{ color: green; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ECG Analysis Report</h1>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>

            <div class="section">
                <h2>Classification Result</h2>
                <p>Detected Condition: <strong>{ecg_class}</strong></p>
            </div>

            <div class="section">
                <h2>Health Assessment</h2>
                <p>{health_analysis['health_status']}</p>
                <p>Risk Level: <span class="{health_analysis['risk_level']}-risk">
                    {health_analysis['risk_level'].upper()}
                </span></p>
            </div>

            <div class="section">
                <h2>Symptoms and Causes</h2>
                <p>{health_analysis['symptoms_causes']}</p>
            </div>

            <div class="section">
                <h2>Recommendations</h2>
                <p>{health_analysis['recommendations']}</p>
            </div>
        </body>
        </html>
        """

        return report_name, html_content