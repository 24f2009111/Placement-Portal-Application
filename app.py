from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from models import db, User
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from routes.student_routes import student_bp
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'placement_portal_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company.dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(role='admin').first():
            admin = User(username='admin', email='admin@example.com', 
                        password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin created with credentials - username: admin, password: admin123")
    app.run(debug=True)