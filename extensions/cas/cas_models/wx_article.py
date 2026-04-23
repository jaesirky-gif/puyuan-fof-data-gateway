
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class WxArticleCas(Model):
    __table_name__ = 'wx_article_cas'
    __keyspace__ = 'fof'

    article_id = columns.Integer(primary_key=True)
    content = columns.Text()

    def to_dict(self):
        return {
            'article_id': self.article_id,
            'content': self.content,
        }

