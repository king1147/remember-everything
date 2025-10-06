from flask import Blueprint, render_template, current_app

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    return render_template('base.html', config=current_app.config)
