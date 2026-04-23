from apps.auth import blu as auth_blu
from apps.index import blu as index_blu
from apps.fof import blu as fof_blu
from apps.fund import blu as fund_blu
from apps.sms import blu as sms_blu
from apps.basic import blu as basic_blu
from apps.tx_video import blu as tx_video_blu
from apps.haifeng import blu as hf_blu
from apps.markets import blu as market_blu
from apps.portfolio import blu as portfolio_blu
from apps.management import blu as management_blu

routers = [
    auth_blu,
    index_blu,
    fof_blu,
    fund_blu,
    sms_blu,
    basic_blu,
    tx_video_blu,
    hf_blu,
    market_blu,
    portfolio_blu,
    management_blu,
]
