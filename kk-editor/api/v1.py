"""
api version 1
"""

from flask import Blueprint

bp = Blueprint('api_v1', __name__, url_prefix='/v1')

@bp.route('/analyze')
def analyze():
    return __name__
