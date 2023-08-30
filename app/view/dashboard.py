"""
RFP
좋아요가 많은 글 10개 리스트 업
-> Post Doc 찔러서 좋아요 순으로 Ordering하면 됨

근래 생성된 포스트 10개 리스트 업
-> Post Doc 찔러서 create_time ordering
-> 전체 안가지고오고 원하는 카운트만 오더링할 수 있나 쿼리 단에서

댓글, comment 많은 글 리스트 업
-> Comment, Thread Doc에서 글 많은 순으로 Grouping

내가 쓴 포스트
내가 좋아요 한 포스트
내가 쓴 댓글
"""

from flask import g, request, jsonify
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status

from app.service.dashboard import DashboardService


class DashBoardView(FlaskView):

    @doc(tags=["DashBoard"], summary="DashBoard feature", description="health-check monitor")
    @route("monitor", methods=["GET"])
    def dashboard_monit(self):
        return ("DashBoard health-check",
                status.HTTP_200_OK)

    @doc(tags=["DashBoard"], summary="DashBoard feature", description="Posts Likes-Top10")
    @route("likes", methods=["GET"])
    def likes_top10(self):
        dash_service = DashboardService()
        dash_service.get_likes_top10()
        print(dash_service.result_posts)

        return jsonify(dash_service.result_posts)

    @doc(tags=["DashBoard"], summary="DashBoard feature", description="Posts Recent-Top10")
    @route("recent", methods=["GET"])
    def recent_top10(self):
        dash_service = DashboardService()
        dash_service.get_recent_top10()

        return jsonify(dash_service.result_posts)

    @doc(tags=["DashBoard"], summary="DashBoard feature", description="Posts Comments-Top10")
    @route("comments", methods=["GET"])
    def comments_top10(self):
        pass
