from app.model.post import Post
from app.model.user import User
from app.schema.post import PostInfoSchema

# Sorting
# - Ascending : 1, descending : -1
# - datetime인 경우 가까운 날짜, 최신부터 오더링할 경우 -1, 가장 오래된 것 부터는 1
pipeline = [
    {"$project": {"title": 1,
                  "content": 1,
                  "likes_count": {"$size": "$like"}}},
    {"$sort": {"likes_count": -1}},
    {"$limit": 10}
]

recent_pipeline = [
    {"$project": {"title": 1,
                  "author": 1,
                  "content": 1,
                  "create_time": 1}},
    {"$sort": {"create_time": -1}},
    {"$limit": 10}
]

# post 내 reference field에 내가 있는지 확인해야 함.
my_like_posts_pipeline = [
    {""}
]


class DashboardService:

    def __init__(self):
        self.result_posts = []
        pass

    def get_likes_top10(self) -> bool:
        """
        모든 포스트에서 좋아요가 많은 10개 오더링
        :return:
        """
        ret = Post.objects().aggregate(*pipeline)
        if ret is None:
            print(f"Can't get data : {ret}")
            return False

        self.result_posts = list(ret)

        # 좀 더 Graceful하게 변경하고 싶음..
        # Mongo bson의 objectId 필드가 jsonify할 경우 바로 파싱이 안됨.
        for item in self.result_posts:
            item["_id"] = str(item["_id"])

        return True

    def get_recent_top10(self) -> bool:
        """
        가장 최근에 생성된 포스트 10개
        """
        agg = Post.objects().aggregate(*recent_pipeline)
        if agg is None:
            return False

        self.result_posts = list(agg)
        print(self.result_posts)
        for item in self.result_posts:
            item["_id"] = str(item["_id"])

        return True

    def get_my_posts(self, user_id) -> bool:
        agg = Post.objects(author__user_id=user_id)
        if agg is None:
            return False

        for item in agg:
            serialized_data = PostInfoSchema().dump(item)
            self.result_posts.append(serialized_data)

        return True

    def get_my_comments(self, user_id) -> bool:
        return True

    def get_my_like_posts(self, user_id) -> bool:
        """
        내가 좋아요 누른 포스트의 값을 가지고 옴, ListField within referenceField 체크 방법
        :param user_id: 좋아요를 누른 유저
        :return:
        """
        user_to_check = User.objects(user_id=user_id).first()
        print(user_to_check)
        # 최악의 경우는 user_id model의 _id를 찾아서 넣어주어야하나?
        # 너무 별론데, 다른 방법은 없나, StackOverflow는 쪼개야 한다고 하는데

        agg = Post.objects(like__contains=user_to_check)
        for item in agg:
            serialized_data = PostInfoSchema().dump(item)
            self.result_posts.append(serialized_data)

        return True
