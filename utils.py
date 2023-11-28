import pandas as pd

BASE_URL = 'https://blockchain.info/rawaddr/'


def retrieve_transactions(address):
    """Requests address info to the API"""
    full_url = BASE_URL + address

    content = pd.read_json(full_url)
    return content['txs']


def process_data(transactions, address):
    """Processes the data retrieved from APIs to retrieve only useful parameters"""
    data = list()
    for transaction in transactions:  # Extraction of useful data from the original dataframe
        record = dict()
        amount = transaction['result']
        record['IsReceived'] = amount > 0
        record['Amount'] = amount
        record['Balance'] = transaction['balance']

        # Checking if the selected address is a sender or a receiver
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

    return pd.DataFrame(data)  # Final DataFrame processed


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

