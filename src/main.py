#!/usr/bin/env python3
"""
GeoConsulta - Web-Based Geospatial Query and Visualization Platform
Main Flask application entry point

Author: Manus AI
License: MIT
"""

from flask import Flask, render_template
from flask_cors import CORS
import os
from routes.establishments import establishments_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:password@localhost/geoconsulta'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(establishments_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        """Serve the main application page."""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy', 'service': 'geoconsulta'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Development server configuration
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting GeoConsulta server on port {port}")
    print(f"🌍 Access the application at: http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
