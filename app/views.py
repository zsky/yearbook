#encoding:utf-8
from flask import render_template, redirect, url_for, session,\
        request, flash, abort, make_response, send_from_directory
from werkzeug import secure_filename
from app import app, db
from models import Team, User, Event, Comment, Photo
from forms import RegisterForm, LoginForm, CommentForm
from datetime import datetime, timedelta
import json, md5, os


# users login and logout
@app.route('/login', methods = ['POST'])
def login():
    user = User.query.filter_by(email = request.form['email']).first()
    if user and user.check_password(request.form['password']):
        session['logged_in'] = True
        session['user_id'] = user.id
        return redirect(url_for('profile'))

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    session.pop('user_id',None)
    redirect_to_home = redirect(url_for('index'))
    resp = make_response(redirect_to_home)
    resp.set_cookie('email', expires=0)
    resp.set_cookie('pwd', expires=0)
    return resp

@app.route('/register', methods = ['POST'])
def register():
    user = User(username = request.form['username'],
            email = request.form['email'],
            password = request.form['password'])
    db.session.add(user)
    db.session.commit()
    session['logged_in'] = True
    session['user_id'] = user.id
    return redirect(url_for('profile'))



@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    return render_template('index.html',
            title = 'home')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        teams = user.teams 
    else:
        return redirect(url_for('index'))

    return render_template('profile.html',
            title = 'profile',
            teams = teams)

@app.route('/add_team', methods = ['GET', 'POST'])
def add_team():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        return redirect(url_for('index'))

    if request.method == 'POST':
        team = Team(title = request.form['title'],
            intro = request.form['intro'])
        team.admins.append(user)
        user.teams.append(team)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('add_team.html',
            title = 'add_team')
    
@app.route('/show_team/<int:team_id>')
def show_team(team_id):
    team = Team.query.get(team_id)
    team_events = team.events
    return render_template('show_team.html',
            title = 'show_team',
            team = team,
            events = team_events)


@app.route('/admin_team/<int:team_id>')
def admin_team(team_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        return redirect(url_for('index'))
    
    team = Team.query.get(team_id)
    team_events = team.events.order_by(Event.timestamp.desc())
    print 'hsh'
    for e in team_events:
        for p in e.photos:
            print p.path
    photos = Photo.query.all()
    for p in photos:
        print p.path, p.event_id
        

    if user not in team.admins:
        return redirect(url_for('show_team', team_id=team_id))

    return render_template('admin_team.html',
            title = 'admin_team',
            team = team,
            events = team_events)

@app.route('/add_event', methods = ['POST'])
def add_event():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return redirect(url_for('index'))

    t_id = request.form['team_id'],
    team_id = int(t_id[0])

    event_date = datetime.strptime(request.form['event_time'], '%d %B %Y')
    date_path = event_date.strftime('%Y-%m')
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                'team-'+str(team_id), date_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                'team-'+str(team_id), date_path, filename))

    event = Event(
            title = request.form['event_title'],
            content = request.form['event_content'],
            timestamp = event_date,
            team_id = team_id,
            author_id = user_id
            )
    db.session.add(event)
    db.session.commit()

    photo = Photo(
            path = os.path.join('team-'+str(team_id), date_path, filename),
            event_id = event.id
            )
    db.session.add(photo)
    db.session.commit()
    return redirect(url_for('admin_team', team_id=team_id)) 

def allowed_file(filename):
    return '.' in filename and\
            filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']
