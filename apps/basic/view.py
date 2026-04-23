import pandas as pd
from bases.viewhandler import ApiViewHandler
from utils.helper import replace_nan
from utils.decorators import login_required


class TradeDatesAPI(ApiViewHandler):

    def get(self):
        from surfing.data.view.basic_models import TradingDayList
        from surfing.data.wrapper.mysql import BasicDatabaseConnector

        with BasicDatabaseConnector().managed_session() as mn_session:
            query = mn_session.query(
                TradingDayList
            )
            df = pd.read_sql(query.statement, query.session.bind)
            df = df[['datetime']]

        return replace_nan(df.to_dict(orient='list'))

