"""
중간 발표 시연을 위한 rest api
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from core.analyzer import analyzer
from kk_editor import db
from kk_editor.models import Article, Keywords
from sqlalchemy.exc import NoResultFound


api = Namespace('v0', description='prototype operations')


@api.route('/<string:keyword>')
@api.param('keyword', description='keyword')
class Recommend(Resource):
    @api.doc('기사 추천')
    def get(self, keyword):
        try:
            data = analyzer.recommend_by_keyword(keyword, Keywords, Article)
            response = {'code': 1,
                        'payload': data}
            return jsonify(response)
        # 해당 검색어에 대한 기사가 없음
        except NoResultFound as e:
            response = {'code': 0,
                        'payload': None}
            return jsonify(response)


@api.route('/analyze')
class Analyze(Resource):
    def get(self):
        analyzer.extract_keyword(db, Article)
        analyzer.collect_keyword(db, Keywords)
        return 'analyze'
