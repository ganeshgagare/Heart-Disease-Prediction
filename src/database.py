from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, Boolean, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
import json
from time import sleep
from sqlalchemy.exc import OperationalError

# Get database URL from environment or use SQLite as fallback
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ecg_analysis.db')

# Create engine with connection pooling and retry mechanism
def create_db_engine(retries=3):
    for attempt in range(retries):
        try:
            engine = create_engine(
                DATABASE_URL,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800  # Recycle connections after 30 minutes
            )
            engine.connect()  # Test the connection
            return engine
        except OperationalError as e:
            if attempt == retries - 1:
                raise Exception(f"Failed to connect to database after {retries} attempts: {str(e)}")
            sleep(1)  # Wait before retrying

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class ECGAnalysis(Base):
    """Model for storing ECG analysis results"""
    __tablename__ = "ecg_analyses"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    filename = Column(String)
    ecg_class = Column(String)  # COVID-19, MI, etc.
    class_probabilities = Column(Text)  # JSON string of probabilities
    health_status = Column(Text)
    risk_level = Column(String)
    symptoms_causes = Column(Text)
    recommendations = Column(Text)
    report_path = Column(String)

    # Store extracted features
    mean_intensity = Column(Float)
    std_intensity = Column(Float)
    percentile_25 = Column(Float)
    percentile_75 = Column(Float)
    contour_area = Column(Float)
    contour_length = Column(Float)
    freq_mean = Column(Float)
    freq_std = Column(Float)
    freq_max = Column(Float)

def get_db():
    """Get database session with retry mechanism"""
    retries = 3
    for attempt in range(retries):
        try:
            db = SessionLocal()
            from sqlalchemy import text
            db.execute(text('SELECT 1'))  # Test the connection
            return db
        except OperationalError as e:
            if attempt == retries - 1:
                raise Exception(f"Failed to get database session after {retries} attempts: {str(e)}")
            sleep(1)  # Wait before retrying
        finally:
            db.close()

def save_analysis(
    filename: str,
    ecg_class: str,
    class_probabilities: float,
    features: list,
    health_analysis: dict,
    report_path: str,
    db=None
):
    """Save analysis results to database with retry mechanism"""
    if db is None:
        db = get_db()

    try:
        analysis = ECGAnalysis(
            filename=filename,
            ecg_class=ecg_class,
            class_probabilities=str(class_probabilities),
            health_status=health_analysis['health_status'],
            risk_level=health_analysis['risk_level'],
            symptoms_causes=health_analysis['symptoms_causes'],
            recommendations=health_analysis['recommendations'],
            report_path=report_path,
            mean_intensity=features[0],
            std_intensity=features[1],
            percentile_25=features[2],
            percentile_75=features[3],
            contour_area=features[4],
            contour_length=features[5],
            freq_mean=features[6],
            freq_std=features[7],
            freq_max=features[8]
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to save analysis: {str(e)}")
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)