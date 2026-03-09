from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from models import db, CompanyProfile, PlacementDrive, Application, StudentProfile

company_bp = Blueprint('company', __name__, url_prefix='/company')

class PlacementDriveForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    eligibility = TextAreaField('Eligibility Criteria', validators=[DataRequired()])
    deadline = DateTimeField('Application Deadline', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Create Drive')

@company_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'company':
        return redirect(url_for('index'))
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    return render_template('company/dashboard.html', company=company, drives=drives)

@company_bp.route('/create-drive', methods=['GET', 'POST'])
@login_required
def create_drive():
    if current_user.role != 'company':
        return redirect(url_for('index'))
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if company.approval_status != 'approved':
        flash('Your company is not approved yet.', 'warning')
        return redirect(url_for('company.dashboard'))
    form = PlacementDriveForm()
    if form.validate_on_submit():
        drive = PlacementDrive(company_id=company.id, job_title=form.job_title.data,
                              job_description=form.job_description.data,
                              eligibility=form.eligibility.data, deadline=form.deadline.data)
        db.session.add(drive)
        db.session.commit()
        flash('Placement drive created. Awaiting admin approval.', 'success')
        return redirect(url_for('company.dashboard'))
    return render_template('company/create_drive.html', form=form)

@company_bp.route('/drive/<int:drive_id>')
@login_required
def view_drive(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('index'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if drive.company_id != company.id:
        return redirect(url_for('index'))
    applications = Application.query.filter_by(drive_id=drive_id).all()
    return render_template('company/view_drive.html', drive=drive, applications=applications)

@company_bp.route('/update-application-status/<int:app_id>/<status>')
@login_required
def update_application_status(app_id, status):
    if current_user.role != 'company':
        return redirect(url_for('index'))
    application = Application.query.get_or_404(app_id)
    drive = PlacementDrive.query.get(application.drive_id)
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if drive.company_id != company.id:
        return redirect(url_for('index'))
    if status in ['shortlisted', 'selected', 'rejected']:
        application.status = status
        db.session.commit()
        flash(f'Application status updated to {status}.', 'success')
    return redirect(url_for('company.view_drive', drive_id=drive.id))

@company_bp.route('/edit-drive/<int:drive_id>', methods=['GET', 'POST'])
@login_required
def edit_drive(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('index'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if drive.company_id != company.id:
        return redirect(url_for('index'))
    form = PlacementDriveForm()
    if form.validate_on_submit():
        drive.job_title = form.job_title.data
        drive.job_description = form.job_description.data
        drive.eligibility = form.eligibility.data
        drive.deadline = form.deadline.data
        db.session.commit()
        flash('Drive updated successfully.', 'success')
        return redirect(url_for('company.dashboard'))
    elif request.method == 'GET':
        form.job_title.data = drive.job_title
        form.job_description.data = drive.job_description
        form.eligibility.data = drive.eligibility
        form.deadline.data = drive.deadline
    return render_template('company/edit_drive.html', form=form, drive=drive)

@company_bp.route('/delete-drive/<int:drive_id>')
@login_required
def delete_drive(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('index'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if drive.company_id != company.id:
        return redirect(url_for('index'))
    db.session.delete(drive)
    db.session.commit()
    flash('Drive deleted successfully.', 'success')
    return redirect(url_for('company.dashboard'))
