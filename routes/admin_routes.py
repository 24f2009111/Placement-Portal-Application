from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, CompanyProfile, StudentProfile, PlacementDrive, Application

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    total_students = StudentProfile.query.count()
    total_companies = CompanyProfile.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    return render_template('admin/dashboard.html', total_students=total_students, 
                         total_companies=total_companies, total_drives=total_drives, 
                         total_applications=total_applications)

@admin_bp.route('/companies')
@login_required
def manage_companies():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    pending = CompanyProfile.query.filter_by(approval_status='pending').all()
    approved = CompanyProfile.query.filter_by(approval_status='approved').all()
    rejected = CompanyProfile.query.filter_by(approval_status='rejected').all()
    return render_template('admin/companies.html', pending=pending, approved=approved, rejected=rejected)

@admin_bp.route('/approve-company/<int:company_id>')
@login_required
def approve_company(company_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = 'approved'
    db.session.commit()
    flash(f'{company.name} approved successfully.', 'success')
    return redirect(url_for('admin.manage_companies'))

@admin_bp.route('/reject-company/<int:company_id>')
@login_required
def reject_company(company_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    company = CompanyProfile.query.get_or_404(company_id)
    company.approval_status = 'rejected'
    db.session.commit()
    flash(f'{company.name} rejected.', 'warning')
    return redirect(url_for('admin.manage_companies'))

@admin_bp.route('/drives')
@login_required
def manage_drives():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    pending_drives = PlacementDrive.query.filter_by(status='pending').all()
    approved_drives = PlacementDrive.query.filter_by(status='approved').all()
    return render_template('admin/drives.html', pending=pending_drives, approved=approved_drives)

@admin_bp.route('/approve-drive/<int:drive_id>')
@login_required
def approve_drive(drive_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'approved'
    db.session.commit()
    flash(f'Drive {drive.job_title} approved.', 'success')
    return redirect(url_for('admin.manage_drives'))

@admin_bp.route('/reject-drive/<int:drive_id>')
@login_required
def reject_drive(drive_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'rejected'
    db.session.commit()
    flash(f'Drive {drive.job_title} rejected.', 'warning')
    return redirect(url_for('admin.manage_drives'))

@admin_bp.route('/students')
@login_required
def manage_students():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    query = request.args.get('q')
    if query:
        students = StudentProfile.query.filter(
            (StudentProfile.name.ilike(f'%{query}%')) |
            (StudentProfile.contact.ilike(f'%{query}%'))
        ).all()
    else:
        students = StudentProfile.query.all()
    return render_template('admin/students.html', students=students, query=query)

@admin_bp.route('/deactivate-student/<int:student_id>')
@login_required
def deactivate_student(student_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    student = StudentProfile.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    user.is_active = False
    db.session.commit()
    flash(f'Student {student.name} deactivated.', 'warning')
    return redirect(url_for('admin.manage_students'))
