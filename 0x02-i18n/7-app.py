#!/usr/bin/env python3
"""
Flask app with user login simulation, prioritized locale, and timezone handling
"""

from flask import Flask, g, render_template, request
from flask_babel import Babel
import pytz
from pytz.exceptions import UnknownTimeZoneError

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration class for the Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Determine the best match for supported languages in this order:
    1. Locale from URL parameters.
    2. Locale from user settings.
    3. Locale from request headers.
    4. Default locale.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user["locale"]

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """
    Determine the best time zone in this order:
    1. Timezone from URL parameters.
    2. Timezone from user settings.
    3. Default to UTC.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass

    if g.user and g.user.get("timezone"):
        try:
            return pytz.timezone(g.user["timezone"]).zone
        except UnknownTimeZoneError:
            pass

    return Config.BABEL_DEFAULT_TIMEZONE


def get_user():
    """
    Retrieve a user dictionary based on the `login_as` URL parameter.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Execute before all requests to set the logged-in user in `g.user`.
    """
    g.user = get_user()


@app.route('/')
def index():
    """
    Basic route for the application.
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
