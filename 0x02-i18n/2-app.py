#!/usr/bin/env python3
"""
Flask app with Babel setup and locale selector
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """
    Config class for Flask app settings
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determines best match for supported languages
    Returns:
        str: Best language match based on request
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders the index page
    Returns:
        str: HTML content of the index page
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
