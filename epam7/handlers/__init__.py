# app/__init__.py içinde
# from handlers.pull_requests import bp as pull_requests_bp

def create_app():
    app = Flask(__name__)
    
    # Blueprint'i register et
    app.register_blueprint(pull_requests_bp)
    
    return app