# SmsEdge API Python
Pip package for interacting SMSEdge API functions.
You can browse our documentation for more details: https://developers.smsedge.io/v1/reference

## Installation
```commandline
pip install smsedge-api-python-SMSEdge
``` 

## Initialization
Import class the the package
```python
from smsedge_api_python import SmsEdgeApi
```

* Make an object from the class.
* Use the API Key from your account (https://app.smsedge.io/users/) to create a new SmsEdgeApi instance.
```python
api = SmsEdgeApi('') # api_key is required, For example: K_xGA286GbLxGf7zWM
```

* Then you can use the API.

## SMS

#### Send A single SMS
```python
# Params details:

# Required params:
# from, The sender of the SMS (11 characters max)
# to, SMS receiver phone number, in international format (f.e 12127678347 - US number)
# text, Text of SMS

# Optional params:
# name, Value for custom name variable in text provided
# email, Value for custom email variable in text provided
# country_id, ID of country. Recommended to specify this parameter if phone number provided in local format
# reference, Unique value per message, to prevent double submission
# shorten_url, If true will search for a URL (http:#example.com) in the message and will shorten it so it’ll be click trackable. Will short the first URL in the text
# list_id, Phone number of recipient can be added to list with this ID
# transactional, show Label for transactional messages
# preferred_route_id, Use this param if you want to send SMS via specific Route
# delay, If you want to delay sending, set this parameter (in seconds)

fields = {
    'from': 'SNDR_ID',
    'to': 12127678347,
    'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry',
    'name': 'John Doe',
    'email': 'johndoe@email.com',
    'country_id': 1,  # List of countries on get_countries() function.
    'reference': 'some_string',
    'shorten_url': True,  # By default false.
    'list_id': 1,
    'transactional': 1,
    'preferred_route_id': 1,  # List of routes on get_routes() function.
    'delay': 10  # Delay by seconds
}

sms = api.send_single_sms(fields)
print(sms)

Result:
{
  "success": true,
  "data": {
    "id": 19591,
    "created": "2018-02-14 17:35:40",
    "from": "smsapi",
    "to": 6598943560,
    "country_id": 192,
    "country_name": "Singapore",
    "verify_local": 1,
    "shorten_url": 1,
    "list_id": 2070,
    "parts": 1,
    "reference": null,
    "clicked": false,
    "text": "Dear John (john@test.com), please visit my page http:#page.com/",
    "status": "sent"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 17:35:40"
  },
  "api": {
    "version": "v1",
    "module": "sms",
    "function": "send-single"
  },
  "user": {
    "id": 64
  }
}
```
#### Bulk SMS Sending

```python
# Params details:

# Required params:
# list_id, Messages will be sent to all good numbers from list with this ID
# from, The sender of the SMS (11 characters max)

# text, Text of SMS -> Usage of custom variables in text: name, lname, email, custom1, custom2, custom3, custom4, custom5
# For example: Hello, {{{name}}} {{{lname}}}! Please visit my site: http:#smsedge.io/

# Optional params:
# shorten_url, If true will search for a URL (http:#example.com) in the message and will shorten it so it’ll be click trackable. Will short the first URL in the text
# preferred_route_id, Use this param if you want to send SMS via specific Route

fields = {
    'list_id': 1,
    'from': 'SNDR_ID',
    'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry',
    'preferred_route_id': 1  # List of routes on get_routes() function.
}

list_messages = api.send_list(fields)
print(list_messages)

Result:

{
  "success": true,
  "data": [
    "7 message(s) have been sent"
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 17:46:08"
  },
  "api": {
    "version": "v1",
    "module": "sms",
    "function": "send-list"
  },
  "user": {
    "id": 64
  }
}
```
#### Get SMS Information

```python
# Params details:

# Required params:
# ids, Comma-separated SMS ids

fields = {
    'ids': '1,4,27'
}

sms_info = api.get_sms_info(fields)
print(sms_info)

Result:

{
  "success": true,
  "data": [
    {
      "id": 18839,
      "created": "2018-02-11 10:14:30",
      "from": "smsapi",
      "to": 972535000000,
      "country_id": 104,
      "country_name": "Israel",
      "verify_local": 1,
      "shorten_url": 1,
      "list_id": null,
      "parts": 1,
      "reference": "some-external-id-1",
      "clicked": false,
      "cost": 0.006,
      "original_url": "http:#page.com/",
      "shortened_url": "http:#sho.rt/1ei4h",
      "text": "Please visit my page: http:#sho.rt/1ei4h",
      "status": "sent",
      "dlr_status": "DELIVERED"
    },
    {
      "id": 18875,
      "created": "2018-02-13 11:52:17",
      "from": "smsapi",
      "to": 972535000001,
      "country_id": 104,
      "country_name": "Israel",
      "verify_local": 1,
      "shorten_url": 1,
      "list_id": 2065,
      "parts": 1,
      "reference": "some-external-id-1",
      "clicked": false,
      "cost": 0.006,
      "original_url": "http:#page.com/",
      "shortened_url": "http:#sho.rt/1ei4h",
      "text": "Please visit my page: http:#sho.rt/1ei4h",
      "status": "waiting",
      "dlr_status": "QUEUED"
    }
  ],
  "errors": [
    "SMS with specified id [905] was not found"
  ],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 17:10:30"
  },
  "api": {
    "version": "v1",
    "module": "sms",
    "function": "get"
  },
  "user": {
    "id": 64
  }
}
```

## LISTS OF NUMBERS

#### Create A New List
```python
# Params details:

# Required params:
# name, Name of the new list

fields = {
    'name': 'My list Python'
}

created_list = api.create_list(fields)
print(created_list)

Result:

  "success": true,
  "data": {
    "id": 2071,
    "name": "Test List",
    "description": null,
    "status": "Finished",
    "created": "2018-02-14 15:39:39"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 15:39:39"
  },
  "api": {
    "version": "v1",
    "module": "lists",
    "function": "create"
  },
  "user": {
    "id": 64
  }
}
```

#### Delete A List

```python
# Params details:

# Required params:
# id, ID of list that wanted to be deleted

fields = {
    'id': 46502
}

delete_list = api.delete_list(fields)
print(delete_list)

Result:

{
  "success": true,
  "data": {
    "message": "List [2071] has been deleted successfully"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 15:43:00"
  },
  "api": {
    "version": "v1",
    "module": "lists",
    "function": "delete"
  },
  "user": {
    "id": 64
  }
}
```

#### Get List Information

```python
# Params details:

# Required params:
# id, ID of requested list

fields = {
    'id': 1
}

list_resource = api.get_list_info(fields)
print(list_resource)

Result:

{
  "success": true,
  "data": {
    "id": 2065,
    "name": "Test List",
    "description": null,
    "status": "Finished",
    "created": "2018-02-11 10:19:28",
    "counts": [
      {
        "country_id": "13",
        "country_name": "Australia",
        "numbers_total": "39",
        "numbers_good": "11",
        "numbers_bad": "3",
        "numbers_clickers": "0",
        "numbers_sent": "0",
        "numbers_hlr_progress": "0",
        "numbers_waiting": "0"
      },
      {
        "country_id": "226",
        "country_name": "United States",
        "numbers_total": "7",
        "numbers_good": "0",
        "numbers_bad": "0",
        "numbers_clickers": "0",
        "numbers_sent": "0",
        "numbers_hlr_progress": "0",
        "numbers_waiting": "0"
      }
    ]
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 15:40:59"
  },
  "api": {
    "version": "v1",
    "module": "lists",
    "function": "info"
  },
  "user": {
    "id": 64
  }
}
```

#### Get All Lists

```python
lists = api.get_all_lists()
print(lists)

Result:

{
  "success": true,
  "data": [
    {
      "id": 2070,
      "name": "Test List 1",
      "description": null,
      "status": "Finished",
      "created": "2018-02-12 14:49:37"
    },
    {
      "id": 2069,
      "name": "Test List 2",
      "description": null,
      "status": "Finished",
      "created": "2018-02-12 10:46:31"
    }
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 15:44:10"
  },
  "api": {
    "version": "v1",
    "module": "lists",
    "function": "getall"
  },
  "user": {
    "id": 64
  }
}
```

## PHONE NUMBERS

#### Add A Number To List

```python
# Params details:

# Required params:
# number, Phone number of recipient
# list_id, Number will be added to list with this ID

# Optional params:
# country_id, ID of country. Recommended to specify this parameter if phone number provided in local format
# name, Name of recipient
# email, E-mail of recipient

fields = {
    'number': '',
    'list_id': 1,
    'country_id': 1,
    'name': 'John Doe',
    'email': 'john_doe@email.com'
}

created_number = api.create_number(fields)
print(created_number)

Result:

{
  "success": true,
  "data": {
    "id": 31014558,
    "number": "61449980000",
    "number_normalized": "61449980000",
    "list_id": 2070,
    "country_id": 13,
    "country_name": "Australia",
    "created": "2018-02-14 15:53:00",
    "status": "good"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 15:53:00"
  },
  "api": {
    "version": "v1",
    "module": "numbers",
    "function": "create"
  },
  "user": {
    "id": 64
  }
}
```

#### Delete A Number

```python
# Params details:

# Required params:
# ids, Comma-separated IDs of numbers to be deleted

fields = {
    'ids': '1,32,27'
}

deleted_numbers = api.delete_numbers(fields)
print(deleted_numbers)

Result:

{
  "success": true,
  "data": {
    "message": "1 number(s) have been deleted successfully"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 16:11:07"
  },
  "api": {
    "version": "v1",
    "module": "numbers",
    "function": "delete"
  },
  "user": {
    "id": 64
  }
}
```

#### Get Numbers

```python
# Params details:

# Optional params:
# list_id, Numbers from list with this id will be return
# ids, Comma-separated IDs of numbers
# limit, Limit of numbers to be returned per request. Max: 1000
# offset, By specifying offset, you retrieve a subset of records starting with the offset value.

# At least one of parameters: List ID or IDs of numbers should be specified!.

fields = {
    'list_id': 1,
    'limit': 1000
}

numbers = api.get_numbers(fields)
print(numbers)

Result:

{
  "success": true,
  "data": [
    {
      "id": 31012550,
      "number": "9093190000",
      "number_normalized": "19093190000",
      "list_id": 2065,
      "country_id": 226,
      "country_name": "United States",
      "created": "2018-02-11 10:25:20",
      "created_via_api": true,
      "status": "bad"
    },
    {
      "id": 31012551,
      "number": "9093190000",
      "number_normalized": "19093190000",
      "list_id": 2065,
      "country_id": 226,
      "country_name": "United States",
      "created": "2018-02-11 10:25:26",
      "created_via_api": true,
      "status": "bad"
    }
  ],
  "errors": [],
  "pagination": {
    "limit": 2,
    "offset": 0,
    "total": 46
  },
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 15:59:35"
  },
  "api": {
    "version": "v1",
    "module": "numbers",
    "function": "get"
  },
  "user": {
    "id": 64
  }
}
```

#### Get Unsubscribers

```python
unsubscribers = api.get_unsubscribers()
print(unsubscribers)

Result:

{
  "success": true,
  "data": [
    {
      "number": 123456789012,
      "unsubscribed": "2018-04-10 14:33:27"
    },
    {
      "number": 123456789013,
      "unsubscribed": "2018-04-10 15:51:08"
    },
    {
      "number": 123456789014,
      "unsubscribed": "2018-04-15 10:36:39"
    }
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-04-15 11:37:24"
  },
  "api": {
    "version": "v1",
    "module": "numbers",
    "function": "unsubscribers"
  },
  "user": {
    "id": 278
  }
}
```

## ROUTES

#### Get All Routes

```python
routes = api.get_routes()
print(routes)

Result: 

{
  "success": true,
  "data": [
    {
      "id": "119",
      "name": "Route 121",
      "country_id": "13",
      "country_name": "Australia",
      "price": 0.033
    },
    {
      "id": "119",
      "name": "Route 121",
      "country_id": "226",
      "country_name": "United States",
      "price": 0.012
    }
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-03-20 12:16:59"
  },
  "api": {
    "version": "v1",
    "module": "routes",
    "function": "getall"
  },
  "user": {
    "id": 64
  }
}
```

## AUXILIARY TOOLS

#### Number Simple Verification

```python
# Params details:

# Required params:
# number, Phone number that should be verified

# Optional params:
# country_id, ID of country. Recommended to specify this parameter if phone number provided in local format

fields = {
    'number': '12127678347',
    'country_id': 1
}

simple_verify = api.number_simple_verify(fields)
print(simple_verify)

Result:

{
  "success": true,
  "data": {
    "normalized_number": "61411390000",
    "national_number": "411390000",
    "country_id": 13,
    "country_name": "Australia"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-12 14:04:49"
  },
  "api": {
    "version": "v1",
    "module": "verify",
    "function": "number-simple"
  },
  "user": {
    "id": 64
  }
}
```

#### Number HLR Verification

```python
# Params details:

# Required params:
# number, Phone number that should be verified

# Optional params:
# country_id, ID of country. Recommended to specify this parameter if phone number provided in local format


fields = {
    'number': '12127678347',
    'country_id': 1
}

hlr_verify = api.number_hlr_verify(fields)
print(hlr_verify)

Result: 

{
  "success": true,
  "data": {
    "normalized_number": "4799900000",
    "national_number": "99900000",
    "country_id": 160,
    "country_name": "Norway",
    "hlr": {
      "status": "bad",
      "operator": "",
      "raw_response": {
        "error": 0,
        "errorDescription": "No errors",
        "id": "470400000",
        "brand": "",
        "brand_name": "",
        "reference": "l4799900000",
        "msisdn": 4799900000,
        "network": "",
        "status": "failed",
        "details": {
          "imsi": "",
          "ported": 0
        }
      },
      "stage": "finished"
    }
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 13:32:13"
  },
  "api": {
    "version": "v1",
    "module": "verify",
    "function": "number-hlr"
  },
  "user": {
    "id": 64
  }
}
```

#### Text Analyzing

```python
# Params details:

# Required params:
# text, Text of SMS you want to verify before sending

fields = {
    'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry'
}

text = api.text_analyzing(fields)
print(text)

Result:

{
  "success": true,
  "data": {
    "text": "My SMS text can be verified using this function. Please visit http:#smsedge.io/",
    "encoding": "GSM_7BIT",
    "current_length": 80,
    "max_length": 160,
    "messages_number": 1,
    "url_detected": true,
    "urls": [
      "http:#smsedge.io/"
    ]
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 13:26:31"
  },
  "api": {
    "version": "v1",
    "module": "text",
    "function": "analyze"
  },
  "user": {
    "id": 64
  }
}
```

## REPORTS

#### Sending Process Report

```python
# Params details:

# Optional params:
# status, Filter result by SMS sending status. Available values: sent, waiting, failed
# date_from, Filter results by minimum date
# date_to, Filter results by maximum date
# limit, Limit of items to be returned per request. Max: 1000
# offset, By specifying offset, you retrieve a subset of records starting with the offset value.

fields = {
    'status': 'sent',
    'date_from': datetime.datetime(2018, 8, 11),
    'date_to': datetime.datetime(2018, 8, 19),
    'limit': 1000
}

process_report = api.get_sending_report(fields)
print(process_report)

Result:

{
  "success": true,
  "data": [
    {
      "id": 19581,
      "created": "2018-02-12 15:27:21",
      "from": "smsapi",
      "to": 6598800000,
      "country_id": 192,
      "country_name": "Singapore",
      "verify_local": 0,
      "shorten_url": 1,
      "list_id": 154,
      "parts": 1,
      "reference": null,
      "clicked": false,
      "cost": 0.0135,
      "original_url": "http:#page.com/",
      "shortened_url": "http:#sho.rt/1ei",
      "text": "Joe, visit http:#sho.rt/1ei",
      "status": "sent"
    },
    {
      "id": 19580,
      "created": "2018-02-12 15:29:21",
      "from": "smsapi",
      "to": 6598795001,
      "country_id": 192,
      "country_name": "Singapore",
      "verify_local": 0,
      "shorten_url": 1,
      "list_id": 154,
      "parts": 1,
      "reference": null,
      "clicked": false,
      "cost": 0.0135,
      "original_url": "http:#page.com/",
      "shortened_url": "http:#sho.rt/1ei",
      "text": "Ann, visit http:#sho.rt/1ei",
      "status": "waiting"
    }
  ],
  "errors": [],
  "pagination": {
    "limit": 2,
    "offset": 10,
    "total": 750
  },
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 13:14:55"
  },
  "api": {
    "version": "v1",
    "module": "reports",
    "function": "sending"
  },
  "user": {
    "id": 64
  }
}
```

#### Statistics

```python
# Params details:

# Required Params:
# country_id, ID of Country
# date_from, Filter results by minimum date
# date_to, Filter results by maximum date. Maximal period - 7 days

# Optional params:
# route_id, ID of Route

fields = {
    'country_id': 1,  # List of countries on getCountries() function.
    'date_from': datetime.datetime(2018, 8, 11),
    'date_to': datetime.datetime(2018, 8, 19),
    'route_id': 1  # List of routes on getRoutes() function.
}

statistics = api.get_sending_stats(fields)
print(statistics)

Result:

{
    "success": true,
    "data": {
        "clicks": 0,
        "sent": 5,
        "ctr": 0,
        "cost": 0.06
    },
    "errors": [],
    "response": {
        "code": 200,
        "description": "OK",
        "date": "2019-07-11 10:33:02"
    },
    "api": {
        "version": "v1",
        "module": "reports",
        "function": "stats"
    },
    "user": {
        "id": 1000
    }
}
```

## USER

#### User Details

```python
user = api.get_user_details()
print(user)

Result:

{
  "success": true,
  "data": {
    "id": 64,
    "username": "api-client",
    "email": "api-client@smsedge.io",
    "balance": "191.721",
    "registered": "2017-04-26 14:46:33",
    "optout_link": "https:#goo.gl/6KsQT7"
  },
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 13:06:36"
  },
  "api": {
    "version": "v1",
    "module": "user",
    "function": "details"
  },
  "user": {
    "id": 64**
  }
}
```

## REFERENCES

#### Getting All Available API Functions

```python
functions = api.get_functions()
print(functions)

Result:

{
  "success": true,
  "data": [
    {
      "module": "lists",
      "function": "create",
      "url": "/v1/lists/create/"
    },
    {
      "module": "numbers",
      "function": "create",
      "url": "/v1/numbers/create/"
    },
    {
      "module": "sms",
      "function": "send-single",
      "url": "/v1/sms/send-single/"
    }
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 13:04:25"
  },
  "api": {
    "version": "v1",
    "module": "references",
    "function": "functions"
  },
  "user": {
    "id": 9
  }
}
```

#### Getting All HTTP Response Status Codes

```python
http_statues = api.get_http_statuses()
print(http_statues)

Result:

{
  "success": true,
  "data": [
    {
      "code": 200,
      "description": "OK"
    },
    {
      "code": 401,
      "description": "Authentication Failure"
    },
    {
      "code": 404,
      "description": "Resource Not Found"
    }
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 13:00:42"
  },
  "api": {
    "version": "v1",
    "module": "references",
    "function": "statuses"
  },
  "user": {
    "id": 9
  }
}
```
#### Getting List Of Countries
```python
countries = api.get_countries()
print(countries)

Result:

{
  "success": true,
  "data": [
    {
      "id": 44,
      "code_iso_aplha_2": "CN",
      "code_iso_aplha_3": "CHN",
      "code_phone": 86,
      "name": "China"
    },
    {
      "id": 226,
      "code_iso_aplha_2": "US",
      "code_iso_aplha_3": "USA",
      "code_phone": 1,
      "name": "United States"
    }
  ],
  "errors": [],
  "response": {
    "code": 200,
    "description": "OK",
    "date": "2018-02-14 12:57:07"
  },
  "api": {
    "version": "v1",
    "module": "references",
    "function": "countries"
  },
  "user": {
    "id": 152
  }
}
```



