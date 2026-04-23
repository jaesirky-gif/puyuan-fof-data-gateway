from flask import request
from bases.viewhandler import ApiViewHandler
from bases.globals import db
from models import FOFNavPublic, FOFInfo
from utils.helper import replace_nan
from utils.decorators import login_required


class FOFPublicInfoAPI(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        obj = FOFInfo.filter_by_query(
            fof_id=fof_id,
            manager_id='1',
        ).first()
        if not obj:
            return {}
        return obj.to_dict()


class FOFPublicNavAPI(ApiViewHandler):

    @login_required
    def get(self, fof_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = db.session.query(
            FOFNavPublic.datetime,
            FOFNavPublic.ret,
            FOFNavPublic.nav,
            FOFNavPublic.acc_net_value,
            FOFNavPublic.adjusted_nav,
        )
        if start_date:
            query = query.filter(
                FOFNavPublic.datetime >= start_date,
            )
        if end_date:
            query = query.filter(
                FOFNavPublic.datetime <= end_date,
            )

        results = query.filter(
            FOFNavPublic.fof_id == fof_id,
        ).order_by(
            FOFNavPublic.datetime.asc()
        ).all()

        data = [list(i) for i in results]
        return replace_nan(data)


class FOFPublicListAPI(ApiViewHandler):

    @login_required
    def get(self):
        results = db.session.query(
            FOFNavPublic.datetime,
            FOFNavPublic.ret,
            FOFNavPublic.nav,
            FOFNavPublic.acc_net_value,
            FOFNavPublic.adjusted_nav,
        ).filter(
            FOFNavPublic.fof_id == fof_id,
        ).order_by(
            FOFNavPublic.datetime.asc()
        ).all()

        data = [list(i) for i in results]
        return replace_nan(data)

