#!/usr/bin/env python3
"""
Basic Flask app with Babel setup
"""
from flask import Flask, render_template
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


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders the index page
    Returns:
        str: HTML content of the index page
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
