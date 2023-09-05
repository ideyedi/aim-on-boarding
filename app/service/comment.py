from app.model.comment import *
from app.schema.comment import *


class CommentService:
    def __init__(self):
        self.result = []

    @classmethod
    def write_comment(cls, comment_model: Comment) -> bool:
        """
        Post 작성 시 대댓글의 Rank를 부여하는 식으로 구현하면 좋을 듯
        """
        print(comment_model.content, comment_model.rank, comment_model.create_time)
        print(comment_model.involve, comment_model.parent)
        ret = comment_model.save()
        print(f"Query {ret}")
        if ret is None:
            return False

        return True

    def result(self):
        return self.result

    def get_all_comments_in_posts(self, post_id: str) -> bool:
        ret = Comment.objects(involve=post_id)
        if ret is None:
            return False
        # Graceful 하게 많은 model list를 재정렬하는 방법이 필요
        for item in ret:
            serialized_data = CommentInfoSchema().dump(item)
            self.result.append(serialized_data)

        return True
