from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from models import db, User, CompanyProfile, StudentProfile

auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CompanyRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField('Company Name', validators=[DataRequired()])
    hr_contact = StringField('HR Contact')
    website = StringField('Website')
    submit = SubmitField('Register')

class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField('Full Name', validators=[DataRequired()])
    contact = StringField('Contact')
    submit = SubmitField('Register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data) and user.is_active:
            # company must also be approved
            if user.role == 'company':
                company = CompanyProfile.query.filter_by(user_id=user.id).first()
                if not company or company.approval_status != 'approved':
                    flash('Company account not approved yet or has been rejected.', 'warning')
                    return redirect(url_for('auth.login'))
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials or account inactive.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        # prevent duplicate usernames/emails
        if User.query.filter((User.username==form.username.data)|(User.email==form.email.data)).first():
            flash('Username or email already exists.', 'danger')
            return render_template('register_company.html', form=form)
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role='company')
        db.session.add(user)
        db.session.commit()
        company = CompanyProfile(user_id=user.id, name=form.name.data, hr_contact=form.hr_contact.data, website=form.website.data)
        db.session.add(company)
        db.session.commit()
        flash('Registration successful. Await admin approval.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('register_company.html', form=form)

@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        if User.query.filter((User.username==form.username.data)|(User.email==form.email.data)).first():
            flash('Username or email already exists.', 'danger')
            return render_template('register_student.html', form=form)
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role='student')
        db.session.add(user)
        db.session.commit()
        student = StudentProfile(user_id=user.id, name=form.name.data, contact=form.contact.data)
        db.session.add(student)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register_student.html', form=form)
