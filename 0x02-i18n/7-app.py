#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Optional
import pytz
from pytz.exceptions import UnknownTimeZoneError

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
    """Return a user dictionary or None based on login_as parameter"""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """Executed before each request: set user in g"""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Determine best locale: URL -> User -> Header -> Default"""
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone() -> str:
    """Determine best timezone: URL -> User -> Default (UTC)"""
    try:
        # 1. Timezone from URL
        url_tz = request.args.get('timezone')
        if url_tz:
            return pytz.timezone(url_tz).zone

        # 2. Timezone from user
        if g.get('user'):
            user_tz = g.user.get('timezone')
            if user_tz:
                return pytz.timezone(user_tz).zone

    except UnknownTimeZoneError:
        pass

    # 3. Default to UTC
    return 'UTC'

@app.route('/')
def index():
    """Render home template"""
    return render_template('7-index.html')

if __name__ == '__main__':
    app.run()

