import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from models import db, StudentProfile, PlacementDrive, Application

student_bp = Blueprint('student', __name__, url_prefix='/student')

# form for editing profile and uploading resume
class StudentProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    contact = StringField('Contact')
    resume = FileField('Resume (PDF)', validators=[FileAllowed(['pdf'], 'PDF only')])
    submit = SubmitField('Save')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    applied_drives = db.session.query(PlacementDrive, Application).join(Application).filter(
        Application.student_id == student.id
    ).all()
    return render_template('student/dashboard.html', student=student, applied_drives=applied_drives)

@student_bp.route('/available-drives')
@login_required
def available_drives():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    applied_drive_ids = db.session.query(Application.drive_id).filter(
        Application.student_id == student.id
    ).all()
    applied_ids = [drive_id[0] for drive_id in applied_drive_ids]
    drives = PlacementDrive.query.filter_by(status='approved').filter(
        ~PlacementDrive.id.in_(applied_ids)
    ).all()
    return render_template('student/available_drives.html', drives=drives)

@student_bp.route('/apply/<int:drive_id>')
@login_required
def apply_for_drive(drive_id):
    if current_user.role != 'student':
        return redirect(url_for('index'))
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    drive = PlacementDrive.query.get_or_404(drive_id)
    # Check if already applied
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        flash('You have already applied for this drive.', 'warning')
        return redirect(url_for('student.available_drives'))
    application = Application(student_id=student.id, drive_id=drive_id)
    db.session.add(application)
    db.session.commit()
    flash('Applied successfully!', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/applications')
@login_required
def view_applications():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    applications = Application.query.filter_by(student_id=student.id).all()
    return render_template('student/applications.html', applications=applications)

@student_bp.route('/history')
@login_required
def placement_history():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    selected_applications = Application.query.filter_by(student_id=student.id, status='selected').all()
    return render_template('student/history.html', placements=selected_applications)

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    form = StudentProfileForm()
    if form.validate_on_submit():
        student.name = form.name.data
        student.contact = form.contact.data
        # handle resume upload
        if form.resume.data:
            filename = secure_filename(form.resume.data.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER')
            form.resume.data.save(os.path.join(upload_folder, filename))
            student.resume = filename
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student.profile'))
    elif request.method == 'GET':
        form.name.data = student.name
        form.contact.data = student.contact
    return render_template('student/profile.html', student=student, form=form)
