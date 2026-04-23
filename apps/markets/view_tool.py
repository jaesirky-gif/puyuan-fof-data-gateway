
from surfing.data.api.research_tool import ResearchToolApi

from bases.viewhandler import ApiViewHandler
from utils.decorators import login_required
from utils.helper import replace_nan

from .validators import AssetInfoValidation, PriceRatioValidation


class AssetInfoAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = AssetInfoValidation.get_valid_data(self.input)
        return ResearchToolApi().get_asset_info_by_key_words(**data)


class PriceRatioAPI(ApiViewHandler):

    @login_required
    def post(self):
        data = PriceRatioValidation.get_valid_data(self.input)
        return replace_nan(ResearchToolApi().super_price_ratio(**data))

