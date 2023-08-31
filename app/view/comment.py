from flask import g, request, jsonify
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status

from app.schema.comment import *
from app.service.comment import CommentService
from core.user import check_access_token
from app.error import ApiError


class CommentView(FlaskView):

    @doc(tags=["Comment"], summary="Comment feature", description="health-check monitor")
    @route("monitor", methods=["GET"])
    def dashboard_monit(self):
        return ("Comment health-check",
                status.HTTP_200_OK)

    @doc(tags=["Comment"], summary="Comment feature", description="write comment")
    @route("", methods=["POST"])
    @check_access_token
    @use_kwargs(CommentCreateSchema, location="json_or_form", apply=False, inherit=True)
    def post(self, **kwargs):
        comment_model = CommentCreateSchema().load(request.get_json())
        comment_model.author = kwargs["user_id"]

        comment_service = CommentService()
        ret = comment_service.write_comment(comment_model)
        print(ret)
        return ("Write comment",
                status.HTTP_200_OK)

    @doc(tags=["Comment"], summary="Comment feature", description="write comment")
    @route("", methods=["GET"])
    @use_kwargs({"post_id": fields.Str(required=True)}, location="query")
    def get_all(self, post_id, **kwargs):
        comment_service = CommentService()
        ret = comment_service.get_all_comments_in_posts(post_id)
        if not ret:
            raise ApiError("")

        # HTTP로 전달할 때 ReferenceField는 Object String으로 나오네?
        return jsonify(comment_service.result)
