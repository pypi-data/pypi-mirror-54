# Comagic dataapi v2 wrapper

# Installation

Install using `pip`...

    pip install comagic-wrapper

#Documentation
https://www.comagic.ru/support/api/data-api/
-

# Usage

```python
from comagic import Comagic
client = Comagic("<login>", "<password>") # init retail api

or

client = Comagic(token="<token>")

```
# Customers
```python
# doc - https://www.comagic.ru/support/api/data-api/Partners/#get_customer_user
customers = client.customer_users.get(limit=1000, offset=0, field=[], filter={}, sort=[])
```

# Sites
```python
# list of sites
# doc - https://www.comagic.ru/support/api/data-api/site/get_sites/
sites = client.sites.get(user_id='<user_id> if needed')

# create site
# doc - https://www.comagic.ru/support/api/data-api/site/create_sites/
data = {
   "domain_name": "string",
   "default_phone_number": "number",
   "default_scenario_id": "number",
   "user_id": "number",
   "industry_id": "number",
   "target_call_min_duration": "number",
   "track_subdomains_enabled": "boolean",
   "cookie_lifetime": "number",
   "campaign_lifetime": "number",
   "sales_enabled": "boolean",
   "second_communication_period": "number",
   "services_enabled": "boolean",
   "replacement_dynamical_block_enabled" : "boolean",
   "widget_link" : {
     "enabled": "boolean",
     "text": "string",
     "url": "string"
   },
   "show_visitor_id": {
     "enabled": "boolean",
     "element_id_value": "string",
     "message": "string",
     "length_visitor_id": "number"
   }
}
site = client.sites.create(user_id='<user_id> if needed', **data)

# delete
# doc - https://www.comagic.ru/support/api/data-api/site/delete_sites/
deleted  = client.sites.delete(user_id='<user_id> if needed', id = '<site_id>')

# update site
# doc - https://www.comagic.ru/support/api/data-api/site/update_sites/
update_site = client.sites.update(user_id='<user_id> if needed', **data)
```

# Site blocks
```python
# get site_block
# doc - https://www.comagic.ru/support/api/data-api/site/get_site_blocks/
site_blocks = client.site_blocks.get(user_id='<user_id> if needed', fields = [])

# create site block
# doc - https://www.comagic.ru/support/api/data-api/site/create_site_blocks/
site_block = client.site_blocks.create(site_id="number", name= "string", user_id='<user_id> if needed')

# update site block
# doc - https://www.comagic.ru/support/api/data-api/site/update_site_blocks/
updated_site_block = client.site_blocks.update(id='<number>', name= "string", user_id='<user_id> if needed')

# delete site block
# doc - https://www.comagic.ru/support/api/data-api/site/delete_site_blocks/
deleted = client.site_blocks.delete(user_id='<user_id> if needed', id= '<id>')
```
# Account
```python
# get account
# doc - https://www.comagic.ru/support/api/data-api/Account/
account = client.account.get()
```

# Virtual Numbers
```python
# get virtual numbers
# doc - https://www.comagic.ru/support/api/data-api/vn/get_virtual_numbers/
numbers = client.virtual_numbers.get(user_id='<user_id> if needed', limit=10, offset=0, fields=[], sort=[])

# get available virtual numbers
# doc - https://www.comagic.ru/support/api/data-api/vn/get_available_virtual_numbers/
available_virtual_numbers = client.available_virtual_numbers.get(user_id='<user_id> if needed', limit=10, offset=0
, fields=[], sort=[])

# enable virtual number
# doc - https://www.comagic.ru/support/api/data-api/vn/enable_virtual_numbers/
enable = client.virtual_numbers.enable(user_id='<user_id> if needed', virtual_phone_number='number')

# disable virtual number
# doc - https://www.comagic.ru/support/api/data-api/vn/disable_virtual_numbers/
disable = client.virtual_numbers.disable(user_id='<user_id> if needed', virtual_phone_number='number')
```

# Tags
```python
# doc - https://www.comagic.ru/support/api/data-api/Tags/

# create tag
tag = client.tags.create(user_id='<user_id> if needed', name='<tag_name>')

# update tag
updated_tag = client.tags.update(user_id='<user_id> if needed', name='<tag_name>', id='<tag_id>')

# delete tag
deleted_tag = client.tags.delete(user_id='<user_id> if needed', id='<tag_id>')

# get tags
tag_list = client.tags.get(user_id='<user_id> if needed', limit=10, offset=0, fields=[], sort=[])

# set sales tag
sale_tag = client.tag_sales.set(
    user_id='<user_id> if needed',
    communication_id='<id>',
    communication_type='<type>',
    date_time='2019-08-09',
    transaction_value=123,
    comment='<comment>'
)

# set communication tag
communication_tag = client.tag_communications.set(
    user_id='<user_id> if needed',
    communication_id='<id>',
    communication_type='<type>',
    tag_id='<tag_id>'
)

# unset communication tag
unset_tag = client.tag_communications.unset(
    user_id='<user_id> if needed',
    communication_id='<id>',
    communication_type='<type>',
    tag_id='<tag_id>'
)
```
# Campaigns
```python
# Doc - https://www.comagic.ru/support/api/data-api/Campaigns/

# get campaigns
campaigns = client.campaigns.get(user_id='<user_id> if needed', limit=10, offset=0, fields=[], sort=[])

# delete campaign
deleted = client.campaigns.get(user_id='<user_id> if needed', id='<campaign_id>')

# get campaign available phone numbers
av_campaign_numbers = client.campaign_available_phone_numbers.get(user_id='<user_id> if needed', limit=10, offset=0
, fields=[], sort=[])

# get campaign available redirection phone numbers
redirect_campaign_numbers = client.campaign_available_redirection_phone_numbers.get(
    user_id='<user_id> if needed',
    limit=10, offset=0, fields=[], sort=[])

# create campaign
campaign = client.campaigns.create('<campaign params>') # create kwargs params like in doc

# update campaign
campaign = client.campaigns.update('<campaign params>') # create kwargs params like in doc

# get campaign weight parameter
campaign_weight = client.campaign_parameter_weights.get(user_id='<user_id> if needed', limit=10, offset=0, fields=[], sort=[])

# update campaign weight parameter
update_weight_params = client.campaign_parameter_weights.update('<weight params>')
``` 
# Reports
```python
# Doc - https://www.comagic.ru/support/api/data-api/Reports/

# communications report
communications_report = client.communications_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# call report
calls_report = client.call_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# CDR call report
call_legs_report = client.call_legs_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# goals report
goals_report = client.goals_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# chat report
chat_report = client.chat_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# get chat messages
messages = client.chat_messages_report.get(
    user_id='<user_id> if needed',
    chat_id = '<chat_id>',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# offline messages report
offline_messages_report = client.offline_messages_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# session report
visitor_sessions_report = client.visitor_sessions_report.get(
    user_id='<user_id> if needed',
    date_from='2019-19-10',
    date_to='2019-19-10',
    limit=10000,
    offset=0,
    sort=[],
    fields=[],
)

# financial_call_legs_report
financial_call_legs_report = client.financial_call_legs_report.get(
     user_id='<user_id> if needed',
     date_from='2019-19-10',
     date_to='2019-19-10',
     limit=10000,
     offset=0,
     sort=[],
     fields=[],
 )
```
# TODO
* more examples
* support full methods
* tests



