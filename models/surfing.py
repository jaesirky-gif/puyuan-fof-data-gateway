from surfing.data.view.basic_models import FundInfo as _FundInfo
from surfing.data.view.basic_models import IndexInfo as _IndexInfo
from surfing.data.view.basic_models import IndexPrice as _IndexPrice

from surfing.data.view.basic_models import FOFInfo as SurfingFOFInfo
from surfing.data.view.derived_models import FOFNavPublic as SurfingFOFNavPublic


from bases.dbwrapper import BaseModel, db


class FundInfo(_FundInfo, db.Model):
    __tablename__ = 'fund_info'
    __bind_key__ = 'basic'
    __table_args__ = {
        'extend_existing': True,
    }


class IndexInfo(_IndexInfo, BaseModel):
    __tablename__ = 'index_info'
    __bind_key__ = 'basic'
    __table_args__ = {
        'extend_existing': True,
    }


class IndexPrice(_IndexPrice, BaseModel):
    __tablename__ = 'index_price'
    __bind_key__ = 'basic'
    __table_args__ = {
        'extend_existing': True,
    }


class FOFInfo(SurfingFOFInfo, BaseModel):
    __tablename__ = 'fof_info'
    __bind_key__ = 'basic'
    __table_args__ = {'extend_existing': True}


class FOFNavPublic(SurfingFOFNavPublic, BaseModel):
    __tablename__ = 'fof_nav_public'
    __bind_key__ = 'derived'
    __table_args__ = {'extend_existing': True}

