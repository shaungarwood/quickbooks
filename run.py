from intuitlib.client import AuthClient
from quickbooks import QuickBooks
import toml

config = toml.load("config.toml")

auth_client = AuthClient(
        client_id=config['keys']['client_id'],
        client_secret=config['keys']['client_secret'],
        environment='sandbox',
        redirect_uri='http://localhost:8000/callback',
    )

client = QuickBooks(
        auth_client=auth_client,
        refresh_token='REFRESH_TOKEN',
        company_id='COMPANY_ID',
    )
