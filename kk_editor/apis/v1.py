"""
api version 1
"""

from flask import Blueprint
from kk_editor import db
from kk_editor.models import Article
from core.crawler.main import start_crawl
# from core.analyzer.analyzer import fetch_articles
from apscheduler.schedulers.background import BackgroundScheduler

bp = Blueprint('api_v1', __name__, url_prefix='/v1')

# @bp.route('/analyze')
# def analyze():
#     """
#     DB에서 기사를 로드하여 분석한 뒤 그 결과를 DB에 저장
#     """
#     return fetch_articles(db, Article)


# 마지막으로 크롤링 완료한 시각 전역변수로 가지고 있음
last_crawl = None
@bp.route('/collect')
def collect():
    global last_crawl
    count, spend_time, last_crawl = start_crawl(db, Article, last_crawl)
    return f"{count}개 저장 완료.  걸린 시간: {spend_time}   완료 시각: {last_crawl}"



scheduler = BackgroundScheduler()
scheduler.add_job(func=collect, trigger='cron', hours='*', minute='0')
scheduler.start()