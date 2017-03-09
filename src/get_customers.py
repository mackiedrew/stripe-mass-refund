#!/usr/bin/python

import stripe
from json import (dump as write_json)
from os import remove
from os.path import isfile
from functools import reduce

'''
This file collects all of the stripe charges from now till the beginning of time, this can be time 
consuming but the limit of the API is 100 at a time. It will then be filtered to remove any
charges that don't fit a certain criteria.
'''

# Add your stripe API key here! You will also need to add it to the actually_refund script
stripe.api_key = '!!!ADD API KEY!!!'

# Configure input and output
output_file_name = 'data/charges.json'
fetch_limit = 100

# First response to setup fetch objects
charges = stripe.Charge.list(limit=fetch_limit)
more_charges_avaliable = charges['has_more']

# Colelct all entries in memory until the end of the list
while more_charges_avaliable:
  # Find how much data has been collected
  length = len(charges['data'])
  print("Fetched values: " + str(length + fetch_limit))
  # Determine the last entry we have gotten
  last_entry = charges['data'][length - 1]['id']
  # Make a request for new charges then add them to the list
  response = stripe.Charge.list(
    limit=fetch_limit,
    starting_after=last_entry,
    )
  # Concatinate dictionaries
  charges['data'] = charges['data'] + response['data']
  # Determine if there are more entries to get 
  more_charges_avaliable = response['has_more']


def filtering_method(charge):
  '''
  Method used to select for charges you want to refund. Some example filters are comented below,
  if a charge does not meet criteria, return false, if every test passes, return True.  
  '''
  # if charge['amount'] <= price_limit:
  #   return False
  # if charge['created'] <= only_times_after:
  #   return False
  # if "succeeded" not in charge['status']:
  #   return False
  # if charge['amount'] == charge['amount_refunded']:
  #   return False
  # if "Some words here" not in charge['description']:
  #   return False
  return True

# Filter charges based on the method defined above.
filtered_charges = list(filter(lambda charge: filtering_method(charge), charges["data"]))

# Add amounts, and refunded amounts to a large list for later summing
list_of_income = [entry['amount'] for entry in filtered_charges]
list_of_refund = [entry['amount_refunded'] for entry in filtered_charges]

# Sum the produced arrays to give totals (in USD cents)
total_income = reduce(lambda total, amount: total + amount, list_of_amount)
total_refund = reduce(lambda total, amount: total + amount, list_of_refund)

# Convert to strings and format
total_charges = len(filtered_charges)
income_USD = total_income / 100
refund_USD = total_refund / 100
new_total = total_income - total_refund

# Display information about the refund 
print("Total charges: " + str(total_charges))
print("Income money: $" + str(income_USD))
print("Refund money: $" + str(refund_USD))
print("Total money: $" + str(new_total))

# Remove file if it exists
if isfile(output_file_name):
  remove(output_file_name)

# Output JSON to file
with open(output_file_name, 'w') as output_file:
  write_json(filtered_charges, output_file, indent=4, sort_keys=True)
