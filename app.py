import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from utils.nlp_processor import preprocess_text
from utils.rag_engine import RAGEngine
from utils.claim_analyzer import ClaimAnalyzer

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tbt.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Load data
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return {}

# Initialize NLP components
rag_engine = None
claim_analyzer = None

def initialize_nlp_components():
    global rag_engine, claim_analyzer
    
    # Load evidence data
    evidence_data = load_json_data('data/evidence_database.json')
    regulatory_standards = load_json_data('data/regulatory_standards.json')
    
    # Initialize RAG engine and claim analyzer
    rag_engine = RAGEngine(evidence_data)
    claim_analyzer = ClaimAnalyzer(regulatory_standards)
    
    logger.info("NLP components initialized successfully")

# Routes
@app.route('/')
def index():
    indian_brands = load_json_data('data/indian_brands.json')
    return render_template('index.html', brands=indian_brands)

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        brand_name = request.form.get('brand_name', '')
        tagline = request.form.get('tagline', '')
        claim = request.form.get('claim', '')
        
        if not all([brand_name, tagline, claim]):
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('index'))
        
        try:
            # Preprocess the inputs
            processed_claim = preprocess_text(claim)
            
            # Get relevant evidence using RAG
            evidence = rag_engine.retrieve_evidence(brand_name, tagline, processed_claim)
            
            # Analyze the claim against evidence
            verdict, score, explanation = claim_analyzer.analyze_claim(
                brand_name, 
                tagline, 
                processed_claim, 
                evidence
            )
            
            # Store analysis results in session
            session['analysis_results'] = {
                'brand_name': brand_name,
                'tagline': tagline,
                'claim': claim,
                'verdict': verdict,
                'score': score,
                'explanation': explanation,
                'evidence': evidence
            }
            
            return redirect(url_for('results'))
            
        except Exception as e:
            logger.error(f"Error analyzing claim: {e}")
            flash(f'An error occurred while analyzing the claim: {str(e)}', 'danger')
            return redirect(url_for('index'))

@app.route('/results')
def results():
    analysis_results = session.get('analysis_results', None)
    if not analysis_results:
        flash('No analysis results found. Please submit a claim for analysis.', 'warning')
        return redirect(url_for('index'))
    
    return render_template('results.html', results=analysis_results)

@app.route('/about')
def about():
    return render_template('about.html')

with app.app_context():
    # Import models
    import models  # noqa: F401
    
    # Create tables
    db.create_all()
    
    # Initialize NLP components
    initialize_nlp_components()
