from flask import g, request
from flask_apispec import doc, use_kwargs, marshal_with
from flask_classful import FlaskView, route
from flask_api import status

from app.schema.post import *
from core.user import check_access_token
from app.error import ApiErrorSchema, ApiError
from app.service.post import PostService


class PostView(FlaskView):

    @doc(tags=["Post"], summary="Post feature health-check")
    @route("monitor", methods=["GET"])
    def healthcheck(self):
        return ("Post health-Check",
                status.HTTP_200_OK)

    @doc(tags=["Post"], summary="Post feature", description="포스트 작성")
    @route("", methods=["POST"])
    @check_access_token
    @use_kwargs(PostCreateSchema, location="json_or_form", apply=False)
    def create_post(self, **kwargs):
        user_id = kwargs["user_id"]

        kwargs = PostCreateSchema().load(request.get_json())
        if kwargs is False:
            raise ApiError("Failed to create post",
                           status.HTTP_400_BAD_REQUEST)

        # 요 시리얼라이즈 부분을 좀 나이스하게 바꿀순 없을까?
        # 결국 board 정보를 같은 form으로 전달받아서 요런 재작업을 해줘야하는데
        post_model = Post()
        post_model.title = kwargs["title"]
        post_model.content = kwargs["content"]
        post_model.hashtag = kwargs["hashtag"]

        print(post_model.__repr__())
        post_service = PostService(post_model)
        ret = post_service.creat_post(kwargs["board_title"], user_id)
        if not ret:
            raise ApiError("",
                           status_code=status.HTTP_409_CONFLICT)

        return ("Create Post",
                status.HTTP_200_OK)

    @doc(tags=["Post"], summary="Post feature", description="포스트 좋아요 추가")
    @route("/like", methods=["POST"])
    @check_access_token
    @use_kwargs({"post_id": fields.String(required=True)}, location="query")
    def like_post(self, post_id, **kwargs):
        post_service = PostService(Post())
        ret = post_service.add_like(post_id, kwargs["user_id"])
        if not ret:
            raise ApiError("",
                           status_code=status.HTTP_409_CONFLICT)

        return ("Like post",
                status.HTTP_200_OK)

    @doc(tags=["Post"], summary="Post feature", descripiton="포스트 삭제")
    @route("", methods=["DELETE"])
    @check_access_token
    @use_kwargs({"post_id": fields.String(required=True)}, location="query")
    def delete(self, post_id, **kwargs):
        post_service = PostService(Post())
        ret = post_service.delete_post(post_id, kwargs["user_id"])
        if not ret:
            raise ApiError("",
                           status_code=status.HTTP_400_BAD_REQUEST)

        return ("Delete post",
                status.HTTP_200_OK)

    @doc(tags=["Post"], summary="Post feature", description="포스트 수정")
    @route("", methods=["PUT"])
    @check_access_token
    @use_kwargs(PostInfoSchema, location="query")
    def put(self, *args, **kwargs):
        post_service = PostService(args[0][0])
        post_id = args[0][1]

        ret = post_service.modify_post(post_id, kwargs["user_id"])
        if not ret:
            raise ApiError("",
                           status_code=status.HTTP_400_BAD_REQUEST)

        return ("Modified post",
                status.HTTP_200_OK)
