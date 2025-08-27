from flask import Blueprint

main_bp = Blueprint('main', __name__)

from flask import render_template

@main_bp.route('/')
def index():
    return render_template('index.html')
