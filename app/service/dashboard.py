from app.model.post import Post

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
        self.result_posts = list(agg)
        print(self.result_posts)
        for item in self.result_posts:
            item["_id"] = str(item["_id"])

        return True
