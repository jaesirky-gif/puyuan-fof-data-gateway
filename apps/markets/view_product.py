
from flask import g

from surfing.data.api.portfolio import PortfolioDataApi
from surfing.util.calculator import Calculator

from bases.exceptions import LogicError
from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .libs import get_title_and_items
from .validators import ProductRetValidation, ProductRecentValidation, ProductCorrValidation, ProductRollingValidation


class SelfProductRetAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProductRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        data_dic = PortfolioDataApi().get_product_price_part(
            data['begin_date'], data['end_date'], data['time_para'], data['product_list'],
            manager_id=g.token.get('manager_id'),
        )
        if data_dic is None:
            return
        df = PortfolioDataApi().calculate_product_price(
            data_dic, data['begin_date'], data['end_date'], data['time_para'], data['price_type'], data['benchmark_id']
        )
        if df is None:
            return

        stats = Calculator.get_product_stats(df['_input_asset_nav'], df['_input_asset_info'])
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': replace_nan([row.to_dict() for _, row in stats.iterrows()])
        }


class SelfProductRecentAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProductRecentValidation.get_valid_data(self.input)
        data_dic = PortfolioDataApi().product_recent_rate_data(data['product_list'], manager_id=g.token.get('manager_id'))
        df = PortfolioDataApi().calc_product_recent_rate(data_dic, **data)
        return get_title_and_items(df)


class SelfProductCorrAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = ProductCorrValidation.get_valid_data(self.input)

        data_dic = PortfolioDataApi().get_product_price_part(
            data['begin_date'], data['end_date'], data['time_para'], data['product_list'],
            manager_id=g.token.get('manager_id'),
        )
        if data_dic is None:
            return
        df = PortfolioDataApi().calculate_product_price(
            data_dic, data['begin_date'], data['end_date'], data['time_para'], data['price_type'], data['benchmark_id']
        )
        if df is None:
            return

        df = Calculator.get_asset_corr(df['data'], data['period'])
        return get_title_and_items(df)


class SelfProductRollingCorrAPI(ApiViewHandler):

    @login_required
    def post(self):
        params = ProductRollingValidation.get_valid_data(self.input)
        data = ProductRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        data_dic = PortfolioDataApi().get_product_price_part(
            data['begin_date'], data['end_date'], data['time_para'], data['product_list'],
            manager_id=g.token.get('manager_id'),
        )
        if data_dic is None:
            return
        df = PortfolioDataApi().calculate_product_price(
            data_dic, data['begin_date'], data['end_date'], data['time_para'], data['price_type'], data['benchmark_id']
        )
        if df is None:
            return

        df = Calculator.get_product_rolling_corr(df['_input_asset_nav'], **params)
        return {
            'rets': replace_nan(df['data'].reset_index().to_dict('list')),
            'stats': {key: get_title_and_items(value) for key, value in df['details'].items()}
        }


class SelfProductRollingBetaAPI(ApiViewHandler):

    @login_required
    def post(self):
        params = ProductRollingValidation.get_valid_data(self.input)
        data = ProductRetValidation.get_valid_data(self.input)
        if not data['time_para'] and (not data['begin_date'] or not data['end_date']):
            raise LogicError('缺少参数')

        data_dic = PortfolioDataApi().get_product_price_part(
            data['begin_date'], data['end_date'], data['time_para'], data['product_list'],
            manager_id=g.token.get('manager_id'),
        )
        if data_dic is None:
            return
        df = PortfolioDataApi().calculate_product_price(
            data_dic, data['begin_date'], data['end_date'], data['time_para'], data['price_type'], data['benchmark_id']
        )
        if df is None:
            return

        df = Calculator.get_product_rolling_beta(df['_input_asset_nav'], **params)
        return replace_nan(df.reset_index().to_dict('list'))

