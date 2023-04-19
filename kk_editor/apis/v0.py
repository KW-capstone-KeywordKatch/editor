"""
중간 발표 시연을 위한 rest api
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from core.analyzer import analyzer
from kk_editor import db
from kk_editor.models import Article


api = Namespace('v0', description='prototype operations')


@api.route('/<string:keyword>')
@api.param('keyword', description='keyword')
class Recommend(Resource):
    @api.doc('기사 추천')
    def get(self, keyword):
        analyzer.fetch_articles(db, Article)
        return f'recommend for {keyword}'

