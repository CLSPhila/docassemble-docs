import json
import os
import re
import requests
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail

def get_house_json(guessed_address):
  guessed_address = guessed_address.upper()
  symbols = re.split("\\s+", guessed_address)
  guessed_address_wildcard = "%".join(symbols)

  url = f"https://phl.carto.com/api/v2/sql?q=SELECT * FROM opa_properties_public WHERE location LIKE '%{guessed_address_wildcard}%'"
  resp = requests.get(url)

  if (
    resp.status_code == 400 or
    resp.json()["total_rows"] == 0
  ):
    return None
  else:
    json_data = resp.json()
    return json_data


def get_home_guesses(guessed_address):
  ADDRESS_SEARCH_LENGTH_THRESHOLD = 6
  if len(guessed_address) < ADDRESS_SEARCH_LENGTH_THRESHOLD:
    return {}
  data = get_house_json(guessed_address)
  new_dictionary = {}
  try: 
    for row in data["rows"]:
      new_dictionary[row["location"]] = {}
      for key, val in row.items():
        new_dictionary[row["location"]][key] = val
    return new_dictionary
  except TypeError:
    return {}
    
condition_codes = [
  ("New Construction", "New Construction"),
  ("Rehab", "Rehab"),
  ("Above Average", "Above Average: A well-maintained home with newer features such as floors, windows,and doors.  Not a new build or complete/recent rehab."),
  ("Average", "Average: This is the condition of most homes in Philadelphia.  Use this if your home is in need of some minor maintenance, but is generally livable and well-maintained."),
  ("Below Average", "Below Average: Use this condition code if your home is in need of major repairs, or has serious defects (fallen-in ceilings, sagging porch, cracking walls).  This condition code is also usually the right one to use if a tree has fallen onto your home and caused minor to moderate damage."),
  ("Poor", "Poor: Use this if your property is in poor enough condition that it is in need of a complete rehabilitation.  This category often includes homes that are unsafe to live in (buckling walls, missing roof pieces, etc.)  Use this condition code if a tree has fallen onto your home and caused major damage."),
  ("Shell, Sealed, or Structurally Compromised", "Sealed/Structurally Compromised: Use this condition code of your property is a shell and needs to be demolished."),
]

def get_condition_code_and_desc(code):
  try:
      code = int(code)
      return condition_codes[code - 1] # To account for 0 index
  except:
      return ("Undetermined", "Undetermined")

async def send_email_to_city_dept(dept, attachments, isTest=True):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

  if dept is None:
    return None
  from_email = Email(email_address)
  to_email = To("tsouthard@clsphila.org")
  subject = "TEST: Tax Appeal"
  content = Content("text/plain", "This is a test. Please ignore if you got this by accident")
  mail = Mail(from_email, to_email, subject, content)
  response = sg.client.mail.send.post(request_body=mail.get())
  return response # What should indicate failure vs success? What should we do?
  # Message to user with a button to retry if failed?