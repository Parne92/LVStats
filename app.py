from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, current_user, logout_user


app = Flask(__name__, static_folder='static')
#csrf = CSRFProtect(app)


app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# Initialize the database connection
db = SQLAlchemy(app)

from models import Player, Game

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Player.query.get(int(id))


@app.route('/', methods=['GET'])
def index():
    print('Request for home page received')
    players = Player.query.all()
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    print('Request for about page received')
    players = Player.query.all()
    return render_template('about.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    print('Request for home page received')
    players = Player.query.order_by(Player.rating).all()
    return render_template('dashboard.html', players = players)


@app.route('/<int:id>', methods=['GET'])
def player(id):
    player = Player.query.where(Player.id == id).first()
    games = Game.query.where(Game.playerid == id).order_by(Game.game_date.desc())
    return render_template('details.html', player = player, games=games)

@app.route('/games/<int:id>', methods=['GET'])
@login_required
def game(id):
    all_games = Game.query.order_by(Game.game_date.desc()).limit(5).all()
    player = Player.query.where(Player.id == id).first()
    return render_template("game.html", games = all_games, player = player)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Player.query.filter_by(username = username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('player',id = user.id))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup',methods = ['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Player.query.filter_by(username=username).first()

    if(user):
        flash('Username already exists!')
        return redirect(url_for('signup'))
    
    new_user = Player(username=username, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/<int:id>', methods=['GET'])
def details(id):
    restaurant = Player.query.where(Player.id == id).first()
    reviews = Game.query.where(Game.playerid == id)
    return render_template('details.html', player=restaurant, games=reviews)

@app.route('/game/<int:id>', methods=['POST'])
#@csrf.exempt
def add_review(id):
    try:
        goals = request.values.get('goals')
        if(goals == "None"):
            goals = 0.0
        position = request.values.get('position')
        assists = request.values.get('assists')
        if(assists == "None"):
            assists = 0.0
        tackles = request.values.get('tackles')
        if(tackles == "None"):
            tackles = 0.0
        saves = request.values.get('saves')
        if(saves == "None"):
            saves = 0.0
        time = request.values.get('time')
    except (KeyError):
        #Redisplay the question voting form.
        return render_template('add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        game = Game()
        #reporting = get_logged_user()
        game.playerid = id
        game.game_date = datetime.now()
        game.goals = goals
        game.assists = assists
        game.tackles = tackles
        game.saves = saves
        game.time = time
        #game.playerid = 
        game.rating = calculate_rating(position,goals,assists,tackles,saves,time)
        game.position = position
        db.session.add(game)
        db.session.commit()

    return redirect(url_for('details', id=id))

def calculate_rating(position,goals,assists,tackles,saves,time):
        goals = float(goals)
        assists = float(assists)
        tackles = float(tackles)
        saves = float(saves)
        time = float(time)
        points_per_minute = (goals + assists) / time
        tackles_per_minute = tackles / time
        saves_per_minute = saves / time

        if(position == "Forward"):
            rating = (1.5*goals) + assists + tackles + points_per_minute
        elif(position == "Midfielder"):
            rating = goals + (1.5*assists) + tackles + points_per_minute
        elif(position == "Defender"):
            rating = goals + assists + (1.5 * tackles) + tackles_per_minute + points_per_minute
        elif(position == "Goalkeeper"):
            rating = (goals*4) + (assists * 2) + ((saves/10) * 9) + saves_per_minute
        return rating


@app.context_processor
def utility_processor():

    def games_rating(id):
        games = Game.query.where(Game.playerid == id)

        ratings = []
        game_count = 0
        for game in games:
            ratings += [game.rating]
            game_count += 1

        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        avg_rating = "{:.2f}".format(avg_rating)
        return {'avg_rating': avg_rating, 'game_count': game_count}

    return dict(games_rating=games_rating)

