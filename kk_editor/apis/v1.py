"""
api version 1
"""

from flask import Blueprint
from kk_editor import db
from kk_editor.models import Article
from core.crawler.main import start_crawl
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from core.analyzer import analyzer

bp = Blueprint('api_v1', __name__, url_prefix='/v1')


# 마지막으로 크롤링 완료한 시각 전역변수로 가지고 있음
last_crawl = None
@bp.route('/collect')
def collect():
    global last_crawl
    count, spend_time, last_crawl = start_crawl(db, Article, last_crawl)
    return f"{count}개 저장 완료.  걸린 시간: {spend_time}   완료 시각: {last_crawl}"

# 매일 00시 30분에 전날 기사 삭제
def delete_article():
    today = datetime.datetime.now()
    str_today = today.strftime("%Y%m%d")
    str_today = str_today[2:] + '000000'

    from kk_editor import app
    with app.app_context():
        count = Article.query.filter(Article.time <= str_today).delete()
        db.session.commit()

    print(f"기사 {count}개 삭제 완료")
    return count


scheduler = BackgroundScheduler()
scheduler.add_job(func=collect, trigger='cron', hour='*', minute='0')
scheduler.start()

delete_scheduler = BackgroundScheduler()
delete_scheduler.add_job(func=delete_article, trigger='cron', hour='0', minute=30)
delete_scheduler.start()