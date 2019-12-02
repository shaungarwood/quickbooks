import datetime
import csv

import toml

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
from quickbooks.objects import *

from IPython import embed

def newer_than_cutoff(date):
    cutoff = datetime.datetime(2019, 10, 15, 0, 0)
    txndate = datetime.datetime.strptime(date, '%Y-%m-%d')
    return txndate > cutoff

def write_csv(filename, fieldnames, data):
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for line in data:
            csv_writer.writerow(line)

config = toml.load("config.toml")

auth_client = AuthClient(
        client_id=config['keys']['client_id'],
        client_secret=config['keys']['client_secret'],
        environment='production',
        redirect_uri='http://localhost:5000/app/callback',
    )
url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
print(url)
print("\n\nplease click link and authorize quickbooks, then [enter]\n\n")
input() # waiting for user to click link and authorize quickbooks

config = toml.load("config.toml")
if "codes" not in config:
    print("something didn't get loaded properly")
    exit()

auth_client.get_bearer_token(
        config['codes']['code'],
        realm_id=config['codes']['realmId']
    )

client = QuickBooks(
        auth_client=auth_client,
        refresh_token=auth_client.refresh_token,
        company_id= config['keys']['company_id']
    )

ap_name = "Accounts Payable (A/P)"
ap = Account.filter(Name=ap_name, qb=client)
if len(ap) == 0:
    print(f"could not find {ap_name} account")
    exit()
elif len(ap) > 1:
    print(f"found more than one account: {ap}")
    exit()

ap = ap[0].to_dict()
ap['Entries'] = []

# everything = []
# for x in [Bill, BillPayment, Invoice, Deposit]:
#     txns = x.all(max_results=1000, qb=client)
#     for txn in txns:
#         everything.append(txn)

# sandbox 2: Bill, BillPayment, Invoice, Deposit
# prod: Payment, Deposit, Invoice

all_bills = Bill.all(max_results=1000, qb=client)
to_del = []
for bill in all_bills:
    txndate = bill.TxnDate

    if newer_than_cutoff(txndate):
        print(txndate)
        continue

    to_del.append({
        'account': bill.APAccountRef.name,
        'vendor': bill.VendorRef.name,
        'balance': bill.Balance,
        'total': bill.TotalAmt,
        'txn date': bill.TxnDate
        })
    # bill.delete()

if to_del:
    write_csv("bills.csv", ['account', 'vendor', 'balance', 'total', 'txn date'], to_del)


embed()
