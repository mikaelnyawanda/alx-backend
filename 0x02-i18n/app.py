#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
from typing import Optional
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

app = Flask(__name__)

# Configuration class
class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user() -> Optional[dict]:
    """Return user dict or None based on login_as URL param."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """Executed before each request."""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Get best match locale: URL > user > header > default"""
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """Get best timezone: URL > user > default"""
    try:
        tz = request.args.get('timezone')
        if tz:
            return pytz.timezone(tz).zone
        if g.get('user'):
            user_tz = g.user.get('timezone')
            if user_tz:
                return pytz.timezone(user_tz).zone
    except UnknownTimeZoneError:
        pass
    return 'UTC'

@app.route('/')
def index():
    """Render the home page with current time"""
    user_tz = get_timezone()
    current_time = datetime.now(pytz.timezone(user_tz))
    formatted_time = format_datetime(current_time)
    return render_template('index.html', current_time=formatted_time)

if __name__ == '__main__':
    app.run()

