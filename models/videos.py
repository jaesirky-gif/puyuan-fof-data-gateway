
from bases.dbwrapper import db, BaseModel
from bases.base_enmu import EnumBase


class VideoRoom(BaseModel):
    """双录视频房间"""
    __tablename__ = 'video_room'

    class VideoStatus(EnumBase):
        NOTHING = 0
        ROOM = 1
        COMPLETED = 2
        CONFIRMED = 3

    id = db.Column(db.String(127), primary_key=True)
    manager_id = db.Column(db.String(32))
    ins_name = db.Column(db.String(127))                                  # 机构ID
    fof_id = db.Column(db.String(32))
    investor_id = db.Column(db.String(32))                              # 投资者ID
    adviser_id = db.Column(db.Integer)                                  # 投顾ID
    status = db.Column(db.Integer, default=0)                           # 阶段
    video_url = db.Column(db.String(511))                               # 视频存储URL
    investor_url = db.Column(db.String(511))
    adviser_url = db.Column(db.String(511))

    @classmethod
    def get_video_info(cls, investor_id, manager_id, fof_id):
        self = cls.filter_by_query(
            investor_id=investor_id,
            manager_id=manager_id,
            fof_id=fof_id,
        ).first()

        if not self:
            return {'status': cls.VideoStatus.NOTHING}
        return {
            'status': self.status,
            'room_id': self.id,
            'video_url': self.video_url,
        }
