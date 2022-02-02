from .model import Link
from .schema import LinkSchema

BASE_ROUTE = 'link'


def register_routes(api, app, root='api'):
    """Routes registration."""
    from .controller import api as link_api

    api.add_namespace(link_api, path=f'/{root}/{BASE_ROUTE}')
