from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config
from models import db
from routes.auth import auth_bp
from routes.polls import polls_bp
from routes.votes import votes_bp
import yaml
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Swagger UI configuration
    SWAGGER_URL = '/apidocs'
    API_URL = '/api/openapi.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Polls API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Serve OpenAPI spec file
    @app.route('/api/openapi.yaml')
    def serve_openapi():
        return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'openapi.yaml')
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(polls_bp)
    app.register_blueprint(votes_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'name': 'Polls API',
            'version': '1.0.0',
            'description': 'A Flask-based REST API for voting in polls with different access levels',
            'documentation': {
                'swagger_ui': '/apidocs',
                'openapi_spec': '/api/openapi.yaml'
            },
            'endpoints': {
                'health': '/api/health',
                'auth': {
                    'register': '/api/auth/register',
                    'login': '/api/auth/login'
                },
                'polls': {
                    'list': '/api/polls',
                    'get': '/api/polls/{id}',
                    'create': '/api/polls'
                },
                'votes': {
                    'vote': '/api/votes/poll/{poll_id}',
                    'get_votes': '/api/votes/poll/{poll_id}'
                }
            }
        }), 200
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

