import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db, User, Message, MessageReaction, MessageType, DeleteType, FoodMemory, PhotoMemory, PeriodData
from forms import LoginForm, RegistrationForm, MessageForm, ProfileForm, FoodMemoryForm, PhotoMemoryForm, ContactForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET",
                                "romantic_secret_key_for_love")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    # Fallback to local PostgreSQL if no DATABASE_URL is set
    database_url = 'postgresql://postgres:password@localhost:5432/loveapp'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi', 'wav', 'mp3',
    'm4a'
}
DATA_FOLDER = 'data'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_period_data():
    """Load period tracking data from JSON file"""
    data_file = os.path.join(DATA_FOLDER, 'period_data.json')
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_period": None, "cycle_length": 26, "predictions": []}


def save_period_data(data):
    """Save period tracking data to JSON file"""
    data_file = os.path.join(DATA_FOLDER, 'period_data.json')
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)


def calculate_next_periods(last_period_str, cycle_length, num_periods=3):
    """Calculate next period dates"""
    try:
        last_period = datetime.strptime(last_period_str, '%Y-%m-%d')
        predictions = []

        for i in range(1, num_periods + 1):
            next_period = last_period + timedelta(days=cycle_length * i)
            predictions.append({
                'date':
                next_period.strftime('%Y-%m-%d'),
                'formatted_date':
                next_period.strftime('%B %d, %Y'),
                'days_until': (next_period - datetime.now()).days
            })

        return predictions
    except ValueError:
        return []


# Create database tables
# Create or update database tables
with app.app_context():
    db.create_all()

    # Update or create user with email 'navaneet@example.com' to username 'navaneet'
    user1 = User.query.filter_by(email='navaneet@example.com').first()
    if user1:
        # Check if the desired username 'navaneet' is taken by another user
        existing_navaneet = User.query.filter_by(username='navaneet').first()
        if existing_navaneet and existing_navaneet.email != 'navaneet@example.com':
            logging.error(
                "Username 'navaneet' is already taken by another user with email %s.",
                existing_navaneet.email)
        else:
            user1.username = 'navaneet'
            user1.first_name = 'Navaneet'
            user1.last_name = ''
            if not user1.check_password('112404'):
                user1.set_password('112404')
    else:
        # Only create a new user if the username 'navaneet' is not taken
        if not User.query.filter_by(username='navaneet').first():
            user1 = User(username='navaneet',
                         email='navaneet@example.com',
                         first_name='Navaneet',
                         last_name='')
            user1.set_password('112404')
            db.session.add(user1)
        else:
            logging.error(
                "Cannot create user: username 'navaneet' is already taken.")

    # Update or create user with email 'spurthi@example.com' to username 'darling'
    user2 = User.query.filter_by(email='spurthi@example.com').first()
    if user2:
        # Check if the desired username 'darling' is taken by another user
        existing_darling = User.query.filter_by(username='darling').first()
        if existing_darling and existing_darling.email != 'spurthi@example.com':
            logging.error(
                "Username 'darling' is already taken by another user with email %s.",
                existing_darling.email)
        else:
            user2.username = 'darling'
            user2.first_name = 'Darling'
            user2.last_name = ''
            if not user2.check_password('112404'):
                user2.set_password('112404')
    else:
        # Only create a new user if the username 'darling' is not taken
        if not User.query.filter_by(username='darling').first():
            user2 = User(username='darling',
                         email='spurthi@example.com',
                         first_name='Darling',
                         last_name='')
            user2.set_password('112404')
            db.session.add(user2)
        else:
            logging.error(
                "Cannot create user: username 'darling' is already taken.")

    db.session.commit()
    logging.info("Updated or created users: navaneet and darling")


# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Update last seen
            user.last_seen = datetime.utcnow()
            db.session.commit()

            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.get_display_name()}!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('auth/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if we already have 2 users
    if User.query.count() >= 2:
        flash('Registration is closed. Only two users are allowed.', 'error')
        return redirect(url_for('login'))

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    # Get the other user for chat
    other_user = User.query.filter(User.id != current_user.id).first()

    # Get recent messages count
    unread_count = Message.query.filter_by(
        receiver_id=current_user.id,
        is_read=False).filter(~Message.deleted_for_receiver,
                              ~Message.deleted_for_everyone).count()

    return render_template('home.html',
                           other_user=other_user,
                           unread_count=unread_count)


@app.route('/why')
def why():
    return render_template('why.html')


@app.route('/favorites')
def favorites():
    # Sample favorites data
    favorites_data = {
        'movies': [{
            'name':
            'The Notebook',
            'emoji':
            '💕',
            'description':
            'Because you cry every time and it\'s adorable'
        }, {
            'name': 'Pride and Prejudice',
            'emoji': '📚',
            'description': 'Your favorite comfort movie'
        }, {
            'name': 'Studio Ghibli Films',
            'emoji': '🌸',
            'description': 'Your magical world of wonder'
        }],
        'songs': [{
            'name': 'Your favorite love song',
            'emoji': '🎵',
            'description': 'The one that always makes you smile'
        }, {
            'name': 'That song from our first date',
            'emoji': '💖',
            'description': 'Our special melody'
        }, {
            'name': 'Your shower singing anthem',
            'emoji': '🚿',
            'description': 'You sound like an angel'
        }],
        'quotes': [{
            'text': 'You are my today and all of my tomorrows',
            'emoji': '💫'
        }, {
            'text': 'In you, I\'ve found the love of my life',
            'emoji': '❤️'
        }, {
            'text': 'You are my sunshine on cloudy days',
            'emoji': '☀️'
        }],
        'perfumes': [{
            'name': 'Your signature scent',
            'emoji': '🌺',
            'description': 'The one that drives me crazy'
        }, {
            'name': 'Special occasion perfume',
            'emoji': '✨',
            'description': 'For our date nights'
        }]
    }
    return render_template('favorites.html', favorites=favorites_data)


@app.route('/food')
@login_required
def food():
    # Get food memories from database
    food_memories = FoodMemory.query.filter_by(
        user_id=current_user.id).order_by(FoodMemory.priority.desc()).all()

    # If no food memories exist, create some default ones
    if not food_memories:
        default_foods = [{
            'place': 'Our Favorite Café',
            'dish': 'Vanilla Latte with Heart Art',
            'caption':
            'The way your eyes light up when they make the perfect heart',
            'location': 'Downtown',
            'priority': 5
        }, {
            'place': 'That Italian Place',
            'dish': 'Carbonara Pasta',
            'caption': 'You always save me the last bite',
            'location': 'Little Italy',
            'priority': 4
        }, {
            'place': 'Ice Cream Paradise',
            'dish': 'Strawberry Cheesecake',
            'caption': 'Your happy dance when they have your favorite flavor',
            'location': 'Beach Boardwalk',
            'priority': 3
        }]

        for food_data in default_foods:
            food_memory = FoodMemory(user_id=current_user.id, **food_data)
            db.session.add(food_memory)

        db.session.commit()
        food_memories = FoodMemory.query.filter_by(
            user_id=current_user.id).order_by(
                FoodMemory.priority.desc()).all()

    return render_template('food.html', foods=food_memories)


@app.route('/apology')
def apology():
    return render_template('apology.html')


@app.route('/memories')
def memories():
    # Get all uploaded images
    images = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                images.append(filename)
    return render_template('memories.html', images=images)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('No file selected')
        return redirect(url_for('memories'))

    file = request.files['image']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('memories'))

    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Image uploaded successfully!')

    else:
        flash('Invalid file type. Please upload an image.')

    return redirect(url_for('memories'))


@app.route('/period')
@login_required
def period():
    # Get user's period data from database
    period_data = PeriodData.query.filter_by(user_id=current_user.id).first()

    if not period_data:
        return render_template('period.html',
                               period_data=None,
                               predictions=[],
                               period_history=[],
                               last_period=None,
                               cycle_length=26,
                               days_until_next=None,
                               today=datetime.now().date())

    # Calculate predictions and history
    predictions = []
    period_history = []

    if period_data.last_period:
        last_period = period_data.last_period
        cycle_length = period_data.cycle_length or 26
        today = datetime.now().date()

        # Calculate next 3 periods with durations
        for i in range(3):
            next_date = last_period + timedelta(days=cycle_length * (i + 1))
            days_until = (next_date - today).days
            predictions.append({
                'date':
                next_date,
                'days_until':
                days_until,
                'days_until_abs':
                abs(days_until),  # 👈 Add this key
                'formatted_date':
                next_date.strftime('%B %d, %Y'),
                'duration':
                '3 days'
            })

        # Generate period history (last 6 months)
        for i in range(6):
            past_date = last_period - timedelta(days=cycle_length * i)
            if past_date <= today:
                cycle_days = cycle_length if i > 0 else None
                period_history.append({
                    'date':
                    past_date,
                    'cycle_days':
                    cycle_days,
                    'duration':
                    '3 days',
                    'is_past':
                    past_date < today,
                    'is_current':
                    False,
                    'formatted_date':
                    past_date.strftime('%B %d, %Y')
                })

        # Calculate days until next period
        next_period = last_period + timedelta(days=cycle_length)
        days_until_next = (next_period -
                           today).days if next_period > today else 0

        return render_template('period.html',
                               period_data=period_data,
                               predictions=predictions,
                               period_history=period_history,
                               last_period=last_period,
                               cycle_length=cycle_length,
                               days_until_next=days_until_next,
                               today=today)

    return render_template('period.html',
                           period_data=period_data,
                           predictions=[],
                           period_history=[],
                           last_period=None,
                           cycle_length=26,
                           days_until_next=None,
                           today=datetime.now().date())


@app.route('/update_period', methods=['POST'])
@login_required
def update_period():
    last_period_str = request.form.get('last_period')
    cycle_length = int(request.form.get('cycle_length', 26))

    if last_period_str:
        try:
            last_period = datetime.strptime(last_period_str, '%Y-%m-%d').date()

            # Update or create period data
            period_data = PeriodData.query.filter_by(
                user_id=current_user.id).first()
            if not period_data:
                period_data = PeriodData(user_id=current_user.id,
                                         last_period=last_period,
                                         cycle_length=cycle_length)
                db.session.add(period_data)
            else:
                period_data.last_period = last_period
                period_data.cycle_length = cycle_length
                period_data.updated_at = datetime.utcnow()

            db.session.commit()
            flash('Period tracking updated successfully!')
        except ValueError:
            flash('Please enter a valid date')
    else:
        flash('Please enter a valid date')

    return redirect(url_for('period'))


@app.route('/journal')
def journal():
    affirmations = [
        "You are enough, just as you are", "You are magic in human form",
        "You're the best thing that ever happened to me",
        "Your smile lights up my entire world", "You are loved beyond measure",
        "You are stronger than you know", "You are my favorite person",
        "You make everything better", "You are absolutely beautiful",
        "You are my heart's home"
    ]
    return render_template('journal.html', affirmations=affirmations)


@app.route('/about_her')
@login_required
def about_her():
    # Comprehensive profile data for Darling
    profile_data = {
        'name': 'Darling',
        'age': 22,
        'height': '5\'4"',
        'birthday': 'March 15, 2002',
        'dress_sizes': {
            'dress': 'Medium / Size 8-10',
            'top': 'Medium / Size 8',
            'bottom': 'Medium / Size 28-30',
            'shoes': 'Size 7',
            'bra': '34B',
            'ring': 'Size 6',
            'jeans': 'Size 28-30 / Medium'
        },
        'favorites': {
            'color': 'Soft Pink, Lavender, Rose Gold, Cream',
            'flower':
            'Roses (especially pink), Peonies, Cherry Blossoms, Baby\'s Breath',
            'perfume':
            'Sweet & Floral - Victoria\'s Secret Love Spell, Bath & Body Works Japanese Cherry Blossom',
            'style': 'Feminine & Romantic, Boho-chic, Soft aesthetics',
            'food': 'Italian cuisine, Sushi, Chocolate desserts, Fresh fruit',
            'drinks': 'Bubble tea, Iced coffee, Fruit smoothies, Rosé wine',
            'music': 'Taylor Swift, Billie Eilish, Lana Del Rey, K-Pop',
            'movies': 'Romance, Disney movies, Feel-good comedies',
            'books': 'Romance novels, Self-help, Poetry',
            'activities':
            'Photography, Journaling, Shopping, Spa days, Nature walks',
            'animals': 'Dogs (especially small breeds), Cats, Butterflies',
            'seasons': 'Spring and early Summer',
            'time_of_day': 'Golden hour (sunset)',
            'weather': 'Sunny with a gentle breeze',
            'scents': 'Vanilla, Cherry blossom, Fresh linen, Ocean breeze'
        },
        'personality_traits': {
            'positive': [
                'Kind-hearted', 'Creative', 'Empathetic', 'Adventurous',
                'Genuine', 'Playful'
            ],
            'love_languages': [
                'Words of Affirmation', 'Quality Time', 'Physical Touch',
                'Gift Giving'
            ],
            'hobbies': [
                'Photography', 'Journaling', 'Reading', 'Yoga', 'Cooking',
                'Art & Crafts'
            ],
            'dreams': [
                'Travel the world', 'Start a creative business',
                'Create beautiful memories'
            ]
        },
        'dislikes': {
            'general': 'Loud noises, Crowded spaces, Being rushed, Conflict',
            'food': 'Very spicy food, Bitter vegetables',
            'weather': 'Extreme cold, Heavy rain',
            'activities': 'High-pressure situations, Horror movies'
        },
        'important_dates': {
            'birthday': 'March 15, 2002',
            'anniversary': 'To be celebrated soon!',
            'first_date': 'A beautiful memory in the making',
            'first_met': 'The day everything changed',
            'special_moments': 'Every day with you is special'
        },
        'physical_details': {
            'hair': 'Beautiful and soft',
            'eyes': 'Sparkling and expressive',
            'smile': 'Lights up the whole room',
            'style': 'Effortlessly elegant and feminine'
        }
    }
    return render_template('about_her.html', profile=profile_data)


@app.route('/chat')
@login_required
def chat():
    other_user = User.query.filter(User.id != current_user.id).first()
    if not other_user:
        flash('No other user found to chat with.', 'error')
        return redirect(url_for('home'))

    form = MessageForm()
    return render_template('chat.html', other_user=other_user, form=form)


@app.route('/api/messages')
@login_required
def get_messages():
    other_user = User.query.filter(User.id != current_user.id).first()
    if not other_user:
        return jsonify([])

    # Get messages between current user and other user
    messages = Message.query.filter((
        (Message.sender_id == current_user.id)
        & (Message.receiver_id == other_user.id)) | (
            (Message.sender_id == other_user.id)
            & (Message.receiver_id == current_user.id))).order_by(
                Message.timestamp.asc()).all()

    # Format messages for frontend
    message_list = []
    for msg in messages:
        # Always include message data, let frontend handle visibility
        message_data = {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'sender_name': msg.sender.get_display_name(),
            'content': msg.content,
            'message_type': msg.message_type.value,
            'file_url': msg.file_url,
            'timestamp': msg.timestamp.isoformat(),
            'is_read': msg.is_read,
            'is_edited': msg.is_edited,
            'reactions': msg.get_reactions_summary(),
            'can_delete': msg.sender_id == current_user.id,
            'deleted_for_everyone': msg.deleted_for_everyone,
            'deleted_for_sender': msg.deleted_for_sender,
            'deleted_for_receiver': msg.deleted_for_receiver
        }
        message_list.append(message_data)

    return jsonify(message_list)


@app.route('/api/send_message', methods=['POST'])
@login_required
def api_send_message():
    other_user = User.query.filter(User.id != current_user.id).first()
    if not other_user:
        return jsonify({'error': 'No recipient found'}), 400

    data = request.get_json() or {}
    content = data.get('content', '').strip()
    file_url = data.get('file_url', '')
    message_type = MessageType.TEXT

    if file_url:
        if any(ext in file_url.lower() for ext in ['.mp4', '.mov', '.avi']):
            message_type = MessageType.VIDEO
        else:
            message_type = MessageType.IMAGE

    if not content and not file_url:
        return jsonify({'error': 'Message cannot be empty'}), 400

    message = Message(sender_id=current_user.id,
                      receiver_id=other_user.id,
                      content=content,
                      message_type=message_type,
                      file_url=file_url)

    db.session.add(message)
    db.session.commit()

    message_data = {
        'id': message.id,
        'sender_id': message.sender_id,
        'sender_name': current_user.get_display_name(),
        'content': message.content,
        'message_type': message.message_type.value,
        'file_url': message.file_url,
        'timestamp': message.timestamp.strftime('%H:%M'),
        'is_read': False,
        'is_edited': False,
        'reactions': {},
        'can_delete': True
    }

    return jsonify({
        'status': 'success',
        'success': True,
        'message_id': message.id,
        'message': message_data
    })


@app.route('/api/upload_file', methods=['POST'])
@login_required
def upload_chat_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file and file.filename:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = f"{timestamp}{filename}"

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        file_url = url_for('static', filename=f'uploads/{filename}')
        return jsonify({'status': 'success', 'file_url': file_url})

    return jsonify({'error': 'Invalid file'}), 400


@app.route('/api/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    # Only sender can delete messages
    if message.sender_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    delete_type = request.json.get('delete_type', 'for_me')

    if delete_type == 'for_everyone':
        message.delete_for_user(current_user.id, DeleteType.FOR_EVERYONE)
    else:
        message.delete_for_user(current_user.id, DeleteType.FOR_ME)

    return jsonify({'status': 'success'})


@app.route('/api/react_message/<int:message_id>', methods=['POST'])
@login_required
def react_to_message(message_id):
    message = Message.query.get_or_404(message_id)
    emoji = request.json.get('emoji', '❤️')

    # Check if user already reacted
    existing_reaction = MessageReaction.query.filter_by(
        message_id=message_id, user_id=current_user.id).first()

    if existing_reaction:
        if existing_reaction.emoji == emoji:
            # Remove reaction if same emoji
            db.session.delete(existing_reaction)
        else:
            # Update reaction
            existing_reaction.emoji = emoji
    else:
        # Add new reaction
        reaction = MessageReaction(message_id=message_id,
                                   user_id=current_user.id,
                                   emoji=emoji)
        db.session.add(reaction)

    db.session.commit()

    return jsonify({
        'status': 'success',
        'reactions': message.get_reactions_summary()
    })


@app.route('/delete_image/<filename>')
def delete_image(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash('Image deleted successfully!')
        else:
            flash('Image not found.')
    except Exception as e:
        flash('Error deleting image.')

    return redirect(url_for('memories'))


@app.route('/add_food_item', methods=['POST'])
@login_required
def add_food_item():
    place = request.form.get('place')
    dish = request.form.get('dish')
    location = request.form.get('location')
    caption = request.form.get('caption')
    priority = int(request.form.get('priority', 1))

    # Create new food memory
    food_memory = FoodMemory(user_id=current_user.id,
                             place=place,
                             dish=dish,
                             location=location,
                             caption=caption,
                             priority=priority)

    db.session.add(food_memory)
    db.session.commit()

    flash('Food item added successfully!')
    return redirect(url_for('food'))


@app.route('/delete_food_item/<int:item_id>')
@login_required
def delete_food_item(item_id):
    try:
        food_memory = FoodMemory.query.filter_by(
            id=item_id, user_id=current_user.id).first()
        if food_memory:
            db.session.delete(food_memory)
            db.session.commit()
            flash('Food item deleted successfully!')
        else:
            flash('Food item not found.')
    except Exception as e:
        flash('Error deleting food item.')

    return redirect(url_for('food'))


# API endpoints for WhatsApp-style chat functionality
@app.route('/api/typing_status', methods=['POST'])
@login_required
def typing_status():
    data = request.get_json()
    typing = data.get('typing', False)

    # In a real app, you'd store typing status in cache/database
    # For demo purposes, we'll just return success
    return jsonify({'success': True, 'typing': typing})


@app.route('/api/mark_read', methods=['POST'])
@login_required
def mark_messages_read():
    data = request.get_json()
    message_ids = data.get('message_ids', [])

    if message_ids:
        # Mark messages as read where current user is receiver
        Message.query.filter(Message.id.in_(message_ids),
                             Message.receiver_id == current_user.id).update(
                                 {'is_read': True}, synchronize_session=False)

        db.session.commit()
    else:
        # Mark all unread messages from other user as read
        other_user = User.query.filter(User.id != current_user.id).first()
        if other_user:
            Message.query.filter_by(sender_id=other_user.id,
                                    receiver_id=current_user.id,
                                    is_read=False).update({'is_read': True})
            db.session.commit()

    return jsonify({'success': True})


@app.route('/api/presence', methods=['GET'])
@login_required
def get_presence():
    # Get the other user
    other_user_id = 2 if current_user.id == 1 else 1
    other_user = User.query.get(other_user_id)

    if not other_user:
        return jsonify({'online': False, 'last_seen': None})

    # In a real app, you'd track actual presence
    # For demo, simulate online status
    import random
    is_online = random.choice([True, False])

    return jsonify({
        'online':
        is_online,
        'last_seen':
        other_user.last_seen.isoformat() if other_user.last_seen else None,
        'typing':
        False  # Could track typing status here
    })


@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
