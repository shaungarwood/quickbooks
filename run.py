from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
import toml

from IPython import embed

config = toml.load("config.toml")

auth_client = AuthClient(
        client_id=config['keys']['client_id'],
        client_secret=config['keys']['client_secret'],
        environment='sandbox',
        redirect_uri='http://localhost:5000/app/callback',
    )
url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
print(url)
input()

#client = QuickBooks(
#        auth_client=auth_client,
#        refresh_token='REFRESH_TOKEN',
#        company_id='COMPANY_ID',
#    )
