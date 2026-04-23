import datetime
import pandas as pd
import empyrical as ep
from flask import request

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required, params_required
from utils.queries import SurfingQuery
from utils.helper import replace_nan, select_periods
from utils.ratios import draw_down_underwater, yearly_return
from surfing.util.calculator import Calculator
from surfing.data.api.derived import DerivedDataApi
from extensions.es.es_searcher import IndexSearcher
from extensions.es.es_conn import ElasticSearchConnector
from extensions.es.es_models import IndexSearchDoc


class IndexSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = IndexSearcher(conn, key_word, IndexSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.order_book_id, i.desc_name, i.index_id] for i in results]

        if not results:
            results = []

        return results


class IndexPointQueryAPI(ApiViewHandler):

    @params_required(*['index_id', 'columns'])
    @login_required
    def post(self):
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')

        df = SurfingQuery.get_index_point(
            self.input.index_id,
            start_date,
            end_date,
            self.input.columns,
        )
        df = df[['datetime'] + self.input.columns]
        return replace_nan(df.to_dict(orient='list'))


class IndexPointAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
        )
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        if len(df) < 1:
            return {}

        period = select_periods()
        if period:
            df['temp_datetime'] = df.index
            temp_df = df.copy()
            df = df.resample(period).last()
            df = df.append(temp_df.iloc[0])
            df = df.sort_index()
            df = df.drop_duplicates()
            df = df.dropna(subset=['close'])
            df = df.reset_index()
            df = df.rename(columns={
                'temp_datetime': 'datetime',
                'datetime': 'drop_datetime',
            })
            df = df.set_index('datetime')
            arr = df['close']
        else:
            arr = df['close']

        data = {
            'point': arr.values,
            'dates': arr.index,
        }

        return replace_nan(data)


class IndexPeriodRetAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
            ('close',),
        )

        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        period = select_periods()
        if period:
            df = df.resample(period).last().fillna(method='ffill')

        if len(df) < 1:
            return {}

        data = Calculator.get_recent_ret(df.index, df['close']).__dict__
        return replace_nan(data)


class IndexPeriodRatiosAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
            ('close',),
        )
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')

        period = select_periods()
        if period:
            arr = df['close'].resample(period).last().fillna(method='ffill')
        else:
            arr = df['close']

        if len(arr) < 1:
            return {}

        data = Calculator.get_stat_result(arr.index, arr.values).__dict__
        return replace_nan(data)


class IndexMonthlyRetAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
            ('close',),
        )

        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        period = select_periods()
        if period:
            df = df.resample(period).last().fillna(method='ffill')

        if len(df) < 1:
            return {}

        df['ret'] = df['close'] / df['close'].shift(1) - 1
        returns = df['ret']

        ret = ep.aggregate_returns(returns, 'monthly')
        ret = pd.DataFrame(ret)
        ret.index = ['{}-{}'.format(index[0], index[1]) for index in ret.index]

        data = {
            'ret': ret['ret'].to_list(),
            'month': ret.index,
            'yearly': yearly_return(returns),
        }
        return replace_nan(data)


class IndexDrawDownWaterAPI(ApiViewHandler):

    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = SurfingQuery.get_index_point(
            index_id,
            start_date,
            end_date,
        )
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        period = select_periods()
        if period:
            arr = df['close'].resample(period).apply(lambda x: x[-1] if len(x) > 0 else None).fillna(method='ffill')
        else:
            arr = df['close']

        dff = draw_down_underwater(arr)

        data = {
            'values': dff.values,
            'dates': dff.index,
        }

        return replace_nan(data)


class IndexPEAPI(ApiViewHandler):
    """指数历史PE"""
    @login_required
    def get(self, index_id):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        df = DerivedDataApi().get_index_valuation_develop_columns_by_id(index_id, ['pe_ttm', 'datetime'])
        df = df.sort_values('datetime')

        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            df = df[df['datetime'] >= start_date]

        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            df = df[df['datetime'] <= end_date]

        data = {
            'values': df.pe_ttm,
            'dates': df.datetime,
        }
        return replace_nan(data)
