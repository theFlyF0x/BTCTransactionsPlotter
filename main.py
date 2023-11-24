import pandas as pd

BASE_URL = 'https://blockchain.info/rawaddr/'

address = 'bc1qw9uxxvkf6qk98ly5u0s4ehtl5cf8wjl0jy6cql'
full_url = BASE_URL + address

content = pd.read_json(full_url)
transactions = content['txs']

#out_trx = content['txs'][16]['out']
#transaction = [tr for tr in out_trx if tr['addr'] == address]
def get_senders(transaction):
    """Returns all the sender addresses in a transaction"""
    senders = list()
    for send in transaction['inputs']:
        senders.append(send['prev_out']['addr'])
    return senders

def get_recipients(transaction):
    """Returns all the recipient addresses in a transaction"""
    recipients = list()
    for recpt in transaction['out']:
        recipients.append(recpt['addr'])
    return recipients


data = list()
for transaction in transactions:
    record = dict()
    amount = transaction['result']
    record['IsReceived'] = amount>0
    record['Amount'] = amount
    record['Balance'] = transaction['balance']

    senders = []
    recipients = []
    if record['IsReceived']:
        senders = get_senders(transaction)
        recipients = address
    else:
        senders = address
        recipients = get_recipients(transaction)

    record['Senders'] = senders
    record['Recipients'] = recipients

    data.append(record)

table_of_transactions = pd.DataFrame(data)