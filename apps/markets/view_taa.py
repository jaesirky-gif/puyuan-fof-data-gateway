
from surfing.data.api.research_tool import ResearchToolApi


from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan
from .validators import TaaValidation


class TaaAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = TaaValidation.get_valid_data(self.input)
        results = ResearchToolApi().asset_allocation_backtest(**data)

        ret = dict()
        ret['组合收益'] = results['组合收益'].reset_index().to_dict(orient='list')
        ret['各资产权重'] = results['各资产权重'].reset_index().to_dict(orient='list')
        ret['回测指标'] = results['回测指标'].reset_index().to_dict(orient='records')

        return replace_nan(ret)
