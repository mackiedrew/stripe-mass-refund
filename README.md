# Stripe Mass Refund

Stripe does not have, by default, an easy way to refund a large number of people. This program is meant to:

1. Fetch customers from the database after a specified date.
2. Filter customers from this master list, only those which match the preferred refund 'criteria'.
3. Convert the customer list into a CSV containing the format: [CUSTOMER EMAIL] [AMOUNT TO REFUND] [CHARGE ID]
4. Actually process each refund from the CSV.

# History

I wrote this script for my old company, and it has since been scrubbed for sensitive data.
However, I have received persmission from the company to post the script.

# Usage

This script is a bit manual, but that is mostly intentional. You need to run each part independently which is a safe-guard against accidental refund.

1. Replace the API Key in the get\_customers.py file with one you desire.
2. Add filtering options to the filtering\_method of the get\_customers.py file
3. Run charge\_to\_list.py to convert to an easier to view CSV
4. Open the CSV and ensure all the the refunds are ones to perform, things can go very wrong.
5. If everything seems swell, and you are sure, replace the API KEY in the actually\_refund.py
6. Run actually\_refund.py

# Disclaimer

The API may change, the script may not work, check the scripts work before moving on because it could seriously mess up your bank account.

This has been tested on amounts larger than a million USD so I can't say forsure it works on more than that.