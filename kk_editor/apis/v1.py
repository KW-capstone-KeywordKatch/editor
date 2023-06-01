"""
api version 1
"""

from flask import Blueprint

import kk_editor.apis.v0
from kk_editor import db
from kk_editor.models import Article
from core.crawler.main import start_crawl
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text

bp = Blueprint('api_v1', __name__, url_prefix='/v1')


# 마지막으로 크롤링 완료한 시각 전역변수로 가지고 있음
last_crawl = None
# 최근에 분석 완료한 기사의 id를 가지고 있음     ####서버 재시작 시 문제 발생 가능####
last_analyze = 0
@bp.route('/collect')
def collect():
    global last_crawl
    count, spend_time, last_crawl = start_crawl(db, Article, last_crawl)

    a = kk_editor.apis.v0.Analyze()
    from kk_editor import app
    with app.app_context():
        a.get()

    return f"{count}개 저장 완료.  걸린 시간: {spend_time}   완료 시각: {last_crawl}"

# 매일 00시 30분에 전날 기사 삭제
def delete_article():
    from kk_editor import app
    with app.app_context():
        count = Article.query.count()
        db.session.execute(text('TRUNCATE TABLE article'))
        db.session.commit()

        db.session.execute(text('TRUNCATE TABLE keywords'))
        db.session.commit()

    print("기사 초기화 완료")
    return count


scheduler = BackgroundScheduler()
scheduler.add_job(func=collect, trigger='cron', hour='*', minute='1')
scheduler.start()

delete_scheduler = BackgroundScheduler()
delete_scheduler.add_job(func=delete_article, trigger='cron', hour='19', minute='0')
delete_scheduler.start()