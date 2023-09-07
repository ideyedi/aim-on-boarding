from app.model.post import *
from app.model.user import *
from app.model.comment import *
from app.schema.post import *
from app.schema.comment import *

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

comment_pipeline = [
    {"$group": {"_id": "$involve", "count": {"$sum": 1}}},
    {"$project": {"post_id": "$_id",
                  "count": 1}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

connect_by_pipeline = [
    {
        "$graphLookup": {
            "from": "comment",
            "startWith": "$_id",
            "connectFromField": "parent",
            "connectToField": "_id",
            "as": "hierarchy_comments"
        }
    }
]


class DashboardService:

    def __init__(self):
        self.result_posts = []
        pass

    def get_likes_top10(self):
        """
        모든 포스트에서 좋아요가 많은 10개 오더링
        :return:
        """
        ret = Post.objects().aggregate(*pipeline)
        if ret is None:
            print(f"Can't get data : {ret}")
            return False

        #self.result_posts = list(ret)
        return list(ret)

    def get_recent_top10(self) -> bool:
        """
        가장 최근에 생성된 포스트 10개
        """
        agg = Post.objects().aggregate(*recent_pipeline)
        if agg is None:
            return False

        self.result_posts = list(agg)

        for item in self.result_posts:
            item["_id"] = str(item["_id"])

        return True

    def get_comments_top10(self) -> bool:
        agg = Comment.objects().aggregate(*comment_pipeline)

        list_post_id = list(agg)
        #
        print(list_post_id)

        for item in list_post_id:
            ret = Post.objects(id=item["post_id"]).first()
            data = PostInfoSchema().dump(ret)
            self.result_posts.append(data)

        print(self.result_posts)
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
        agg = Comment.objects(author=user_id)
        if agg is None:
            return False

        for item in agg:
            data = CommentInfoSchema().dump(item)
            self.result_posts.append(data)

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

    @classmethod
    def get_comment_tree(cls):
        agg = Comment.objects().aggregate(*connect_by_pipeline)
        if agg is None:
            return False

        print(agg)
        for item in agg:
            print(item)

        return list(agg)