#encoding:utf-8
from flask import render_template, redirect, url_for, session,\
        request, flash, abort, make_response, send_from_directory
from werkzeug import secure_filename
from app import app, db
from models import Team, User, Event, Comment, Photo, Tag, Category, Message
from datetime import datetime, timedelta
import json, md5, os, re
import uuid
from PIL import Image
from oauth import google, douban, get_auth, get_token, get_info


def auth_register(profile):
    u = User.query.filter_by(email = profile['email']).first()
    if u:
        session['logged_in'] = True
        session['user_id'] = u.id
        return redirect(url_for('profile'))

    user = User(username = profile['username'], 
            email = profile['email'],
            password = profile['password']) 
    image_url = profile.get('image_url')
    if image_url:
        user.image_url = image_url
    else:
        user.image_url = app.config['DEFAULT_USER_IMG']
    db.session.add(user)
    db.session.commit()
    session['logged_in'] = True
    session['user_id'] = user.id
    return redirect(url_for('profile'))

@app.route('/auth_douban')
def auth_douban():
    return redirect(get_auth(douban))

@app.route('/auth_douban_callback')
def auth_douban_callback():
    if request.method == 'GET':
        code = request.args.get('code', '')
        token = get_token(douban, code)
        info_res = get_info(douban, token)
        info_json = json.loads(info_res)
        profile = {
                'email': 'douban' + info_json['uid'],
                'username': info_json['name'],
                'image_url': info_json['avatar'],
                'password': 'douban'
                }
        return auth_register(profile)
    
@app.route('/auth_google')
def auth_google():
    return redirect(get_auth(google))

@app.route('/auth_google_callback')
def auth_google_callback():
    if request.method == 'GET':
        code = request.args.get('code', '')
        token = get_token(google, code)
        info_res = get_info(google, token)
        info_json = json.loads(info_res)
        plus_name = info_json['displayName']
        image = info_json['image']['url']
        emails = info_json['emails']
        for i in emails:
            if i['type'] == 'account':
                email = i['value']
                break
        profile = {
                'email': email,
                'username': plus_name,
                'image_url': image,
                'password': 'google'
                }
        return auth_register(profile)
    


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
#    resp.set_cookie('email', expires=0)
#    resp.set_cookie('pwd', expires=0)
    return resp

@app.route('/register', methods = ['POST'])
def register():
    user = User(username = request.form['username'],
            email = request.form['email'],
            password = request.form['password'])
    user.image_url = app.config['DEFAULT_USER_IMG']
    db.session.add(user)
    db.session.commit()
    session['logged_in'] = True
    session['user_id'] = user.id
    return redirect(url_for('profile'))



@app.route('/')
@app.route('/index')
def index():
    tags = Tag.query.all()
    return render_template('index.html',
            tags = tags,
            title = 'home')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        teams = user.teams 
        messages = user.messages.filter_by(state='unread').order_by(Message.timestamp.desc())
    else:
        return redirect(url_for('index'))

    return render_template('profile.html',
            title = 'profile',
            user = user,
            teams = teams,
            messages = messages)

@app.route('/update_photo', methods = ['POST'])
def update_photo():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        return redirect(url_for('index'))

    file = request.files['user_image']
    im = Image.open(file.stream)
    img_name = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1]

    start_x = float(request.form['crop_x'])*im.size[0]
    start_y = float(request.form['crop_y'])*im.size[1]
    end_x = start_x + float(request.form['crop_width'])*im.size[0]
    end_y = start_y + float(request.form['crop_height'])*im.size[1]
    box = (int(start_x), int(start_y), int(end_x), int(end_y))
    region = im.crop(box)

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                'user_photos', 'user-'+str(user.id))
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    region.save(save_path + '/' + img_name)

    # delete old image 
    old_image_path = app.config['UPLOAD_FOLDER'] + user.image_url[16:]
    if os.path.isfile(old_image_path):
        os.remove(old_image_path)

    user.image_url = '../static/upload/user_photos/user-' + str(user.id) + '/' + img_name
    db.session.add(user)
    db.session.commit()
    
    return user.image_url 

@app.route('/team_photo', methods = ['POST'])
def team_photo():
    file = request.files['user_image']
    im = Image.open(file.stream)
    img_name = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1]

    start_x = float(request.form['crop_x'])*im.size[0]
    start_y = float(request.form['crop_y'])*im.size[1]
    end_x = start_x + float(request.form['crop_width'])*im.size[0]
    end_y = start_y + float(request.form['crop_height'])*im.size[1]
    box = (int(start_x), int(start_y), int(end_x), int(end_y))
    region = im.crop(box)

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'team_photos')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    region.save(save_path + '/' + img_name)


    image_url = '../static/upload/team_photos/' + img_name
    
    return image_url 

@app.route('/update_profile', methods = ['GET', 'POST'])
def update_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        return redirect(url_for('index'))
    if request.method == 'POST':
        return 's'

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

        image_url = request.form['image_url']
        if image_url:
            team.image_url = image_url
        else:
            team.image_url = app.config['DEFAULT_TEAM_IMG']
        team.admins.append(user)
        user.teams.append(team)
        db.session.add(team)
        db.session.commit()
        # add tags
        add_tags = request.form['tags'].split(',')
        for t in add_tags:
            t = t.strip()
            if Tag.query.filter_by(title=t).count() == 0 and t:
                new_t = Tag(title = t)
                db.session.add(new_t)
                team.tags.append(new_t)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('add_team.html',
            title = 'add_team')
    
@app.route('/search_user', methods=['POST'])
def search_user():
    search_name = request.form['search_name']
    search_user = User.query.filter_by(username=search_name)
    has_user = User.query.filter_by(username=search_name).count() > 0
    return render_template('user_info.html',
            users = search_user,
            has_user = has_user)

@app.route('/show_team/<int:team_id>')
def show_team(team_id):
    is_member = False
    is_admin = False
    team = Team.query.get(team_id)
    if 'user_id' in session:
        print 'user_id',session['user_id']
        user_id = session['user_id']
        user = User.query.get(user_id)
        is_member = user.is_member(team)
        is_admin = user.is_admin(team)

    print 'is_admin', is_admin
    team_events = team.events
    return render_template('show_team.html',
            title = 'show_team',
            team = team,
            is_member = is_member,
            is_admin = is_admin,
            events = team_events)

@app.route('/tag_teams', methods=['POST'])
def tag_teams():
    tag_id = request.form['tag_id']
    tag = Tag.query.get(tag_id)
    teams = tag.teams
    return render_template('team_entries.html',
            teams = teams)

@app.route('/search_teams', methods=['POST'])
def search_teams():
    words = request.form['words']
    teams = Team.query.all()
    results = []
    for t in teams:
        title_match = re.findall(words, t.title)
        if title_match:
            results.append(t)
    for t in teams:
        intro_match = re.findall(words, t.intro)
        if intro_match:
            results.append(t)

    return render_template('team_entries.html',
            teams = results)

@app.route('/admin_team/<int:team_id>')
def admin_team(team_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        return redirect(url_for('index'))
    
    team = Team.query.get(team_id)
    team_events = team.events.order_by(Event.timestamp.desc())
    team_categories = team.categories
        

    if user not in team.admins:
        return redirect(url_for('show_team', team_id=team_id))

    return render_template('admin_team.html',
            title = 'admin_team',
            team = team,
            events = team_events,
            categories = team_categories)

@app.route('/show_members', methods=['POST'])
def show_members():
    t_id = request.form['t_id']
    team = Team.query.get(t_id)
    members = team.members
    return render_template('members.html',
            team = team,
            members = members)

@app.route('/add_category', methods = ['GET', 'POST'])
def add_category():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return redirect(url_for('index'))

    t_id = request.form['team_id']
    # add catogriess
    add_categories = request.form['categories'].split(',')
    for c in add_categories:
        c = c.strip()
        if Category.query.filter_by(title=c).count() == 0 and c:
            new_c = Category(title = c, team_id = t_id)
            db.session.add(new_c)
    db.session.commit()

    return redirect(url_for('admin_team', team_id=t_id)) 

@app.route('/del_event/<int:e_id>')
def del_event(e_id):
    e = Event.query.get(e_id)
    if e != None:
        db.session.delete(e)
        db.session.commit()
    return 'ok'


@app.route('/add_event', methods = ['POST'])
def add_event():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return redirect(url_for('index'))

    print 'add event func'
    print request.form
    t_id = request.form['team_id']
    team_id = int(t_id[0])

    if request.form['event_time']:
        event_date = datetime.strptime(request.form['event_time'], '%d %B %Y')
    else:
        event_date = datetime.now()

    event = Event(
            title = request.form['event_title'],
            content = request.form['event_content'],
            timestamp = event_date,
            team_id = team_id,
            author_id = user_id
            )
    # category
    c_id = request.form['category_id'],
    print 'c_id', c_id
    if c_id[0]:
        print 'has category'
        event.category_id = c_id
    db.session.add(event)
    db.session.commit()

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

@app.route('/load_comments', methods=['POST'])
def load_comments():
    e_id = request.form['e_id']
    event = Event.query.get(e_id)
    comments = event.comments.order_by(Comment.timestamp.desc())
    return render_template('comments.html',
            comments = comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return redirect(url_for('index'))
    e_id = request.form['e_id']
    event = Event.query.get(e_id)
    c = Comment(body = request.form['c_body'],
            timestamp = datetime.now(),
            user_id = user_id,
            event_id = request.form['e_id'])
    db.session.add(c)
    db.session.commit()
    return render_template('comments.html',
            comments = [c])

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        return redirect(url_for('index'))
    m_type = request.form['m_type']
    # user apply for joining team
    if m_type == 'join_team':
        m_body = request.form['m_body']
        team_id = request.form['t_id']
        team = Team.query.get(team_id)
        team_admins = team.admins
        for admin in team_admins:
            print admin.id
            m = Message(from_id = user_id,
                  to_id = admin.id,
                 m_type = m_type,
                 join_team = team_id,
                 body = m_body)
            db.session.add(m)
    elif m_type == 'invite':
        print 'invite'
        m = Message(from_id = user_id,
                to_id = request.form['to_id'],
                m_type = m_type,
                join_team = request.form['t_id'], 
                body = 'invite you')
        db.session.add(m)


    db.session.commit()
    res = { "f_id": m.from_id,
            "t_id": m.to_id,
            "m_body": m.body
            }
    return json.dumps(res)  

@app.route('/deal_message', methods=['POST'])
def deal_message():
    if 'logged_in' in session:
        pass
    else:
        return redirect(url_for('index'))

    m_id = request.form['m_id']
    message = Message.query.get(m_id)
    message.state = 'read'

    if message.m_type == 'invite':
        m_user = User.query.get(message.to_id)
    elif message.m_type == 'join_team':
        m_user = User.query.get(message.from_id)

    if request.form['command'] == 'accept':
        m_team = Team.query.get(message.join_team)
        m_user.teams.append(m_team)
        db.session.add(m_team)

    db.session.add(message)
    db.session.commit()

    return 'ok'
