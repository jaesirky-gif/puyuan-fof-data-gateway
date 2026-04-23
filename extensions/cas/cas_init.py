from extensions.cas.cas_models.example import CasExample
from extensions.cas.cas_models.production import ProductionInfoCas
from extensions.cas.cas_models.wx_article import WxArticleCas

from cassandra.cqlengine.management import sync_table, drop_table, create_keyspace_simple, create_keyspace_network_topology


def sync_cas_table():
    sync_table(CasExample)
    sync_table(ProductionInfoCas)
    sync_table(WxArticleCas)


def drop_cas_table():
    drop_table(CasExample)
    drop_table(ProductionInfoCas)
    drop_table(WxArticleCas)


if __name__ == '__main__':
    from apps import create_app

    from bases.globals import cas
    create_app().app_context().push()
    cas.get_conn()
    cas.get_session()
    create_keyspace_simple('fof', 1)
    create_keyspace_network_topology('fof', {'cn_northwest_1a': 1})
    sync_cas_table()
    #
    # # CasExample.create(
    # #     user_id=1,
    # #     time_stamp='1',
    # # )
    a = CasExample.get(user_id=1)
    print(a.to_dict())
    # create_keyspace_simple('fof', 1)
    # create_keyspace_network_topology('fof', {'cn_northwest_1a': 1})
    # drop_cas_table()
