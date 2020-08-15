#!/usr/bin/python

import os
from json import (loads as JSON)
from os import remove
from os.path import isfile

'''
The purpose of this file is to convert the list of `charges` provided by the stripe server as a 
JSON file into a CSV (spreadsheet or excel document) which contains easy information for the refund.
'''

# Configure input and output
data_directory = 'data'
script_dir = os.path.join(os.path.dirname(__file__), data_directory)
input_file_name = os.path.join(script_dir, 'charges.json')
output_file_name = os.path.join(script_dir, 'refunds.csv')

# Check to ensure that the input file exists
if not isfile(input_file_name):
  exit()

# Read the entire input file into memory
with open(input_file_name) as input_file:
  input_file_data = input_file.read()

# Convert the raw input into JSON
input_file_JSON = JSON(input_file_data)

# Output total refunds
print("Total entries: " + str(len(input_file_JSON)))

# Create output file object in writing mode
output_file = open(output_file_name, 'w+')

# 
for charge in input_file_JSON:
  
  # Only refund as much as they are still owed, this deals with previous partial refunds
  total_refund = charge['amount'] - charge['amount_refunded']
  email = charge['receipt_email']
  charge_id = charge['id']

  # Construct write line for the charge
  delimiter = "\t"
  columns = (str(total_refund), email, charge_id)
  line = delimiter.join(columns) + "\n"
  
  # Write line to file
  output_file.write(line)

# Close output file
output_file.close()
