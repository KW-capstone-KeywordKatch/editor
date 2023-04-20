"""
api version 1
"""

from flask import Blueprint
from kk_editor import db
from kk_editor.models import Article
from core.crawler.main import start_crawl
from core.analyzer.analyzer import fetch_articles

bp = Blueprint('api_v1', __name__, url_prefix='/v1')

@bp.route('/collect')
def collect():
    count, spend_time = start_crawl(db, Article)
    return f"{count}개 저장 완료.  걸린 시간: {spend_time}"

@bp.route('/analyze')
def analyze():
    """
    DB에서 기사를 로드하여 분석한 뒤 그 결과를 DB에 저장
    """   
    return fetch_articles(db, Article)

