from flask import g, request
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status

from app.schema.post import *
from core.user import check_access_token
from app.error import ApiErrorSchema, ApiError
from app.service.post import PostService


class PostView(FlaskView):

    @doc(summary="Post feature health-check")
    @route("monitor", methods=["GET"])
    def post_monit(self):
        return ("Post health-Check",
                status.HTTP_200_OK)

    @doc(summary="Post feature", description="포스트 작성")
    @route("", methods=["POST"])
    @check_access_token
    @use_kwargs(PostCreateSchema, location="json_or_form", apply=False)
    def create_post(self, **kwargs):
        user_id = kwargs["user_id"]

        kwargs = PostCreateSchema().load(request.get_json())
        if kwargs is False:
            raise ApiError("Failed to create post",
                           status.HTTP_400_BAD_REQUEST)

        post_model = Post()
        post_model.title = kwargs["title"]
        post_model.content = kwargs["content"]
        post_model.hashtag = kwargs["hashtag"]

        print(post_model.__repr__())
        post_service = PostService(post_model)
        ret = post_service.creat_post(kwargs["board_title"], user_id)

        return "TEMP"
