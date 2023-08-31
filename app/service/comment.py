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
        print(self.result)
        ret = Comment.objects(involve=post_id)

        # MongoDB '_id'를 알고 있으면 바로 단번에 조회가 가능하네
        # Front에서 알수있도록 이걸 제공해야하나?
        for item in ret:
            serialized_data = CommentInfoSchema().dump(item)
            self.result.append(serialized_data)
            print(serialized_data)

        return True
