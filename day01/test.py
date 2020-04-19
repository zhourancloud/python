#!/usr/bin/python
from datetime import datetime

query = dict()
query['company_id'] = 100
query['company_name'] = "100"
query['company_age'] = 10
query['comany_addr'] = {
    'company_addr1': "aaa_aaa",
    'company_addr2': "bbb_bbb"
}
print(query)

if isinstance(query.get('company_id'), int):
    print("company_id is int")

if isinstance(query.get('company_name'), str):
    print("company_name is str")

# query.setdefault('company_id', 10)
query.update({'company_id1': 10})

print(query)

if query.get('company_id'):
    print(query.get('company_id'))

if not query.get('company_idd'):
    print(query.get('company_idd', ''))

print(datetime.utcnow())

print(query.values())
print(query.keys())