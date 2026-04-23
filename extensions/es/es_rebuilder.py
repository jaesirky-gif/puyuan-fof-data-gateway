import pandas as pd
from extensions.es.es_builder import FOFFundSearchBuilder, FOFManagementSearchBuilder, PriFOFManagementSearchBuilder
from extensions.es.es_models import FOFFundSearchDoc, FOFManagementSearchDoc, PriFOFFundSearchDoc
from bases.globals import settings, db
from models import ManagementFund, Management, FOFInfo
from apps import create_app
create_app().app_context().push()


def fof_fund_search_rebuilder():
    builder = FOFFundSearchBuilder(label='es_test', doc_model=FOFFundSearchDoc)
    builder.init_rebuild_index()

    query = db.session.query(ManagementFund)
    df = pd.read_sql(query.statement, query.session.bind)
    for index in df.index:
        param = builder.build_doc_param(
            df.loc[index, 'fund_no'],
            df.loc[index, 'fund_name'],
        )
        builder.add_bulk_data(df.loc[index, 'fund_no'], param)
    builder.done_rebuild_index()


def pri_fof_fund_search_rebuilder():
    builder = PriFOFManagementSearchBuilder(label='es_test', doc_model=PriFOFFundSearchDoc)
    builder.init_rebuild_index()

    results = db.session.query(
        FOFInfo.fof_id,
        FOFInfo.manager_id,
        FOFInfo.fof_name,
        FOFInfo.is_fof,
        FOFInfo.asset_type,
    ).filter(
        FOFInfo.asset_type.in_(['production', 'hedge']),
        FOFInfo.is_deleted == False,
    ).all()
    print(len(results))
    for i in results:
        param = builder.build_doc_param(
            i[1],
            i[3],
            i[4],
            i[0],
            i[2],
        )
        builder.add_bulk_data('{}_{}'.format(i[1], i[0]), param)
    builder.done_rebuild_index()


def fof_management_search_rebuilder():
    builder = FOFManagementSearchBuilder(label='es_test', doc_model=FOFManagementSearchDoc)
    builder.init_rebuild_index()

    query = db.session.query(
        Management.register_no,
        Management.manager_name,
    )
    df = pd.read_sql(query.statement, query.session.bind)
    for index in df.index:
        param = builder.build_doc_param(
            df.loc[index, 'register_no'],
            df.loc[index, 'manager_name'],
        )
        builder.add_bulk_data(df.loc[index, 'register_no'], param)
    builder.done_rebuild_index()


def re_build():
    pri_fof_fund_search_rebuilder()
    print('pri fof fund rebuilder done!')

    # fof_fund_search_rebuilder()
    # print('fof fund rebuilder done!')

    # fof_management_search_rebuilder()
    # print('fof management rebuilder done!')


if __name__ == '__main__':
    re_build()
