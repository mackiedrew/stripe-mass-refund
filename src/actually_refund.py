#!/usr/bin/python

import stripe
from os import remove
from os.path import isfile
from functools import reduce

'''
Alright, primetime, this will actually give people money, so be sure about the files you give to it.
'''

# Add your stripe API key here! You will also need to add it to the actually_refund script
stripe.api_key = '!!!ADD API KEY!!!'

# Configure input and output
data_directory = 'data/'
refund_list_file_name = data_directory + 'refunds.csv'
refund_log_file_name = data_directory + 'refunds.log'

# Read the entire input file into memory
with open(refund_list_file_name) as input_file:
    input_file_raw = in_file.readlines()
# Remove whitespace from the ends of each line
stripped = [line.strip() for line in input_file_raw]
# Split each line into a subarray broken up by tabs
split = [line.split('\t') for line in stripped]
# Convert each subarray into a dictionary for easy reference
refunds = [{"email": line[0], "amount": int(line[1]), "id": line[2]} for line in split]

# Immutable sum of the entire refund.
refund_list = list(map(lambda line: line['amount'], refunds))
total_refund = reduce(lambda x, y: x + y, refund_list)

# Output details about the entire refund
print("Total Number of Refunds: " + str(len(refunds)) + '\n')
print("Total Refunds in USD: $" + str(total_refund / 100) + '\n')

def super_print(log_file, output_string):
  '''Print to log and to the console.'''
  print(output_string)
  log_file.write(output_string)

# Create output file object in writing mode
log_file = open(refund_log_file_name, 'w')

# Process each refund, one by one, may take a long time.
for refund in refunds:
  
  # Generate details for refund that's about to occur
  email = "Processing refund for: " + refund['email'] + '\n'
  amount = "For the amount of: $" + str(refund['amount'] / 100) + ' USD\n'
  charge_id = "Using the charge ID of: " + refund['id'] + '\n'
  output_string = email + amount + charge_id

  # Output pre-request string
  super_print(log_file, output_string)

  # Try to refund, if it fails a message will be printed indicating that.
  try:
    # Actual refund
    response = stripe.Refund.create(
      charge=refund['id'],
      amount=refund['amount'],
      reason="requested_by_customer",
    )
    response = "PROCESSED PROPERLY! \n"
  except:
    response = "***********FAILED TO PROCESS*********** \n"

    # Output post-request string
    super_print(log_file, output_string)

# Close output file
log_file.close()
