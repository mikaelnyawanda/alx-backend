#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import Optional

app = Flask(__name__)

# Config class for app
class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},  # 'kg' is unsupported
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user() -> Optional[dict]:
    """Return user dict from mock DB using login_as parameter."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """Run before all requests: get and set user in global context"""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Determine the best locale from URL, user settings, request headers"""
    # 1. Locale from URL parameter
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    # 2. Locale from user settings
    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    # 3. Locale from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Render the homepage"""
    return render_template('6-index.html')

if __name__ == '__main__':
    app.run()

