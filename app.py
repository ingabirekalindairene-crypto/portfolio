"""
Portfolio Backend System - Flask Application
Author: Ingabire Kalinda Irene
Database: SQLite with SQLAlchemy ORM
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Initialize Database
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for frontend requests

# =====================================================
# DATABASE MODELS
# =====================================================

class Project(db.Model):
    """Project Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(500), nullable=False)  # Comma-separated
    image_url = db.Column(db.String(500))
    github_link = db.Column(db.String(500))
    live_link = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'technologies': self.technologies.split(','),
            'image_url': self.image_url,
            'github_link': self.github_link,
            'live_link': self.live_link,
            'date_created': self.date_created.strftime('%Y-%m-%d')
        }

class Skill(db.Model):
    """Skill Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # e.g., Frontend, Backend, Tools
    proficiency = db.Column(db.String(50))  # Beginner, Intermediate, Advanced
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'proficiency': self.proficiency,
            'description': self.description
        }

class Education(db.Model):
    """Education Model"""
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    field_of_study = db.Column(db.String(200), nullable=False)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'school_name': self.school_name,
            'degree': self.degree,
            'field_of_study': self.field_of_study,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'description': self.description
        }

class Experience(db.Model):
    """Experience Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'position': self.position,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description
        }

class ContactMessage(db.Model):
    """Contact Form Messages Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(300), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_received = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'date_received': self.date_received.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read
        }

class Profile(db.Model):
    """Profile Information Model"""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200))
    bio = db.Column(db.Text)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(200))
    github_url = db.Column(db.String(500))
    linkedin_url = db.Column(db.String(500))
    profile_image = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'title': self.title,
            'bio': self.bio,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'github_url': self.github_url,
            'linkedin_url': self.linkedin_url,
            'profile_image': self.profile_image
        }

# =====================================================
# API ROUTES - FOR FRONTEND
# =====================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

@app.route('/api/projects/<int:id>', methods=['GET'])
def get_project(id):
    """Get single project"""
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict())

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all skills"""
    skills = Skill.query.all()
    return jsonify([skill.to_dict() for skill in skills])

@app.route('/api/education', methods=['GET'])
def get_education():
    """Get all education"""
    education = Education.query.all()
    return jsonify([edu.to_dict() for edu in education])

@app.route('/api/experience', methods=['GET'])
def get_experience():
    """Get all experience"""
    experience = Experience.query.all()
    return jsonify([exp.to_dict() for exp in experience])

@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get profile information"""
    profile = Profile.query.first()
    if profile:
        return jsonify(profile.to_dict())
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/messages', methods=['POST'])
def submit_message():
    """Submit contact form message"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ('name', 'email', 'subject', 'message')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    message = ContactMessage(
        name=data['name'],
        email=data['email'],
        subject=data['subject'],
        message=data['message']
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Message saved successfully'}), 201

# =====================================================
# ADMIN ROUTES
# =====================================================

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    """Admin dashboard"""
    projects_count = Project.query.count()
    messages_count = ContactMessage.query.count()
    new_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    return render_template('admin_dashboard.html', 
                         projects_count=projects_count,
                         messages_count=messages_count,
                         new_messages=new_messages)

# =====================================================
# PROJECTS MANAGEMENT
# =====================================================

@app.route('/admin/projects', methods=['GET'])
def manage_projects():
    """View all projects"""
    projects = Project.query.all()
    return render_template('manage_projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
def add_project():
    """Add new project"""
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            technologies=request.form['technologies'],
            image_url=request.form.get('image_url'),
            github_link=request.form.get('github_link'),
            live_link=request.form.get('live_link')
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project added successfully!', 'success')
        return redirect(url_for('manage_projects'))
    
    return render_template('add_project.html')

@app.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Edit project"""
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.technologies = request.form['technologies']
        project.image_url = request.form.get('image_url')
        project.github_link = request.form.get('github_link')
        project.live_link = request.form.get('live_link')
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('manage_projects'))
    
    return render_template('edit_project.html', project=project)

@app.route('/admin/projects/delete/<int:id>', methods=['POST'])
def delete_project(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('manage_projects'))

# =====================================================
# SKILLS MANAGEMENT
# =====================================================

@app.route('/admin/skills', methods=['GET'])
def manage_skills():
    """View all skills"""
    skills = Skill.query.all()
    return render_template('manage_skills.html', skills=skills)

@app.route('/admin/skills/add', methods=['GET', 'POST'])
def add_skill():
    """Add new skill"""
    if request.method == 'POST':
        skill = Skill(
            name=request.form['name'],
            category=request.form['category'],
            proficiency=request.form.get('proficiency'),
            description=request.form.get('description')
        )
        
        db.session.add(skill)
        db.session.commit()
        
        flash('Skill added successfully!', 'success')
        return redirect(url_for('manage_skills'))
    
    return render_template('add_skill.html')

@app.route('/admin/skills/edit/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):
    """Edit skill"""
    skill = Skill.query.get_or_404(id)
    
    if request.method == 'POST':
        skill.name = request.form['name']
        skill.category = request.form['category']
        skill.proficiency = request.form.get('proficiency')
        skill.description = request.form.get('description')
        
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('manage_skills'))
    
    return render_template('edit_skill.html', skill=skill)

@app.route('/admin/skills/delete/<int:id>', methods=['POST'])
def delete_skill(id):
    """Delete skill"""
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('manage_skills'))

# =====================================================
# MESSAGES MANAGEMENT
# =====================================================

@app.route('/admin/messages', methods=['GET'])
def view_messages():
    """View all contact messages"""
    messages = ContactMessage.query.order_by(ContactMessage.date_received.desc()).all()
    return render_template('view_messages.html', messages=messages)

@app.route('/admin/messages/read/<int:id>', methods=['POST'])
def mark_message_read(id):
    """Mark message as read"""
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    flash('Message marked as read', 'success')
    return redirect(url_for('view_messages'))

@app.route('/admin/messages/delete/<int:id>', methods=['POST'])
def delete_message(id):
    """Delete message"""
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('view_messages'))

# =====================================================
# PROFILE MANAGEMENT
# =====================================================

@app.route('/admin/profile', methods=['GET', 'POST'])
def manage_profile():
    """Manage profile information"""
    profile = Profile.query.first()
    
    if request.method == 'POST':
        if profile:
            profile.full_name = request.form['full_name']
            profile.title = request.form['title']
            profile.bio = request.form['bio']
            profile.email = request.form['email']
            profile.phone = request.form['phone']
            profile.location = request.form['location']
            profile.github_url = request.form.get('github_url')
            profile.linkedin_url = request.form.get('linkedin_url')
        else:
            profile = Profile(
                full_name=request.form['full_name'],
                title=request.form['title'],
                bio=request.form['bio'],
                email=request.form['email'],
                phone=request.form['phone'],
                location=request.form['location'],
                github_url=request.form.get('github_url'),
                linkedin_url=request.form.get('linkedin_url')
            )
            db.session.add(profile)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('manage_profile'))
    
    return render_template('manage_profile.html', profile=profile)

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# =====================================================
# CREATE TABLES & SAMPLE DATA
# =====================================================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Project.query.first():
            print("Database already initialized")
            return
        
        # Create sample profile
        profile = Profile(
            full_name="Ingabire Kalinda Irene",
            title="Software Developer Student",
            bio="BTEC IT Level 3 Extended Diploma student passionate about software development",
            email="ingabire.kalinda@example.com",
            phone="+250 788 788 799",
            location="Kigali, Rwanda",
            github_url="https://github.com/yourusername",
            linkedin_url="https://linkedin.com/in/yourusername"
        )
        db.session.add(profile)
        
        # Create sample project
        project = Project(
            title="Elle Steps - Elegant Ladies Shoes Shop",
            description="A responsive e-commerce website for a premium ladies' footwear store",
            technologies="HTML5,CSS3,Bootstrap,JavaScript",
            github_link="https://github.com/yourusername/elle-steps",
            live_link="https://example.com"
        )
        db.session.add(project)
        
        # Create sample skills
        skills_data = [
            Skill(name="HTML5", category="Frontend", proficiency="Advanced"),
            Skill(name="CSS3", category="Frontend", proficiency="Advanced"),
            Skill(name="JavaScript", category="Frontend", proficiency="Intermediate"),
            Skill(name="Python", category="Backend", proficiency="Intermediate"),
            Skill(name="Flask", category="Backend", proficiency="Beginner"),
            Skill(name="Database Design", category="Tools", proficiency="Intermediate"),
        ]
        for skill in skills_data:
            db.session.add(skill)
        
        # Create sample education
        education = Education(
            school_name="Your School",
            degree="Extended Diploma",
            field_of_study="BTEC IT Level 3",
            start_year=2024,
            end_year=2026
        )
        db.session.add(education)
        
        # Create sample experience
        experience = Experience(
            title="Academic Projects",
            company="Self",
            position="Student Developer",
            description="Working on various web development projects"
        )
        db.session.add(experience)
        
        db.session.commit()
        print("Database initialized with sample data!")

    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Database initialization note: {e}")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
