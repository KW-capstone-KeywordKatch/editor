"""
api version 1
"""

from flask import Blueprint
from core.crawler.main import start_crawl
from kk_editor import db
from kk_editor.models import Article

bp = Blueprint('api_v1', __name__, url_prefix='/v1')

@bp.route('/analyze')
def analyze():
    return __name__

@bp.route('/collect')
def collect():
    count, spend_time = start_crawl(db, Article)
    return f"{count}개 저장 완료.  걸린 시간: {spend_time}"
