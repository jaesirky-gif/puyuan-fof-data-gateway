import pandas as pd
from flask import request
from copy import deepcopy
from bases.viewhandler import ApiViewHandler
from utils.helper import replace_nan
from utils.serializer import DataFrameDictSerializer
from utils.decorators import login_required, params_required
from utils.queries import SurfingQuery
from utils.caches import get_all_funds
from extensions.es.es_searcher import FundSearcher, FOFFundSearcher
from extensions.es.es_conn import ElasticSearchConnector
from extensions.es.es_models import FundSearchDoc, FOFFundSearchDoc

from surfing.data.wrapper.mysql import ViewDatabaseConnector
from surfing.data.view.view_models import FundDailyCollection


class FOFPriFundSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = FOFFundSearcher(conn, key_word, FOFFundSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.fof_id, i.fof_name] for i in results]

        if not results:
            results = []

        return results


class FundSearcherAPI(ApiViewHandler):

    @login_required
    def get(self, key_word):
        page = int(request.args.get('page', 0))
        page_size = int(request.args.get('page_size', 5))
        offset = page * page_size

        conn = ElasticSearchConnector().get_conn()
        searcher = FundSearcher(conn, key_word, FundSearchDoc)
        results, count = searcher.get_usually_query_result(key_word, offset, page_size)
        results = [[i.order_book_id, i.desc_name, i.fund_id] for i in results]

        if not results:
            results = []

        return results


class FundListAPI(ApiViewHandler):

    @login_required
    def get(self):
        columns = request.args.get('columns')
        columns = columns.split(',') if columns else None

        with ViewDatabaseConnector().managed_session() as mn_session:
            if columns:
                n_c = deepcopy(columns)
                n_c.remove('fund_name')
                n_c.remove('fund_id')
                n_c.remove('order_book_id')
                n_c = set(n_c)
                query = mn_session.query(
                    FundDailyCollection.fund_id,
                    FundDailyCollection.full_name,
                    FundDailyCollection.order_book_id,
                ).add_columns(*n_c)
            else:
                query = mn_session.query(
                    FundDailyCollection.fund_id,
                    FundDailyCollection.full_name,
                    FundDailyCollection.order_book_id,
                    FundDailyCollection.wind_class_I,
                )

            df = pd.read_sql(query.statement, query.session.bind)
            df = df.rename(columns={
                'full_name': 'fund_name'
            })
            if columns:
                df = df[columns]
            data = df.to_dict(orient='list')
        return replace_nan(data)


class FundPointQueryAPI(ApiViewHandler):

    @params_required(*['fund_ids', 'columns'])
    @login_required
    def post(self):
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        df = SurfingQuery.get_fund_price(
            self.input.fund_ids,
            start_date,
            end_date,
            self.input.columns,
        )
        return replace_nan(df.to_dict(orient='list'))


class FundScreenAPI(ApiViewHandler):

    def eq(self, df, column_values):
        for i in column_values:
            if not self.view_columns.get(i):
                continue
            df = df[df[i] == column_values.get(i)]
        return df

    def gte(self, df, column_values):
        for i in column_values:
            if not self.view_columns.get(i):
                continue
            df = df[df[i] >= column_values.get(i)]
        return df

    def lte(self, df, column_values):
        for i in column_values:
            if not self.view_columns.get(i):
                continue
            df = df[df[i] <= column_values.get(i)]
        return df

    def lt(self, df, column_values):
        for i in column_values:
            if not self.view_columns.get(i):
                continue
            df = df[df[i] < column_values.get(i)]
        return df

    def gt(self, df, column_values):
        for i in column_values:
            if not self.view_columns.get(i):
                continue
            df = df[df[i] > column_values.get(i)]
        return df

    def contains(self, df, column_values):
        for i in column_values:
            if not self.view_columns.get(i):
                continue
            df = df[df[i].str.contains(column_values.get(i))]
        return df

    @login_required
    def post(self):
        df = get_all_funds()
        self.view_columns = {i: 1 for i in df.columns}
        if request.json.get('eq'):
            df = self.eq(df, request.json.get('eq'))
        if request.json.get('gt'):
            df = self.gt(df, request.json.get('gt'))
        if request.json.get('lt'):
            df = self.lt(df, request.json.get('lt'))
        if request.json.get('gte'):
            df = self.gte(df, request.json.get('gte'))
        if request.json.get('lte'):
            df = self.lte(df, request.json.get('lte'))
        if request.json.get('contains'):
            df = self.contains(df, request.json.get('contains'))
        if request.json.get('fund_ids'):
            df = df[df['fund_id'].isin(request.json.get('fund_ids'))]
        if request.json.get('ordering'):
            ascending = False if request.json.get('ordering').startswith('-') else True
            ordering = request.json.get('ordering')
            ordering = ordering[1:] if ordering.startswith('-') else ordering
            df = df.sort_values(ordering, ascending=ascending)

        page = request.json.get('page', 1)
        page_size = request.json.get('page_size', 10)

        serializer = DataFrameDictSerializer()
        serializer.set_pagination(page, page_size)
        data = serializer.to_representation(df)
        return replace_nan(data)

