###############################################################################
# Allergy Related Routines
###############################################################################
@anvil.server.callable(require_user=True)
def get_user_allergies_items():
  """
  Get user_allergies rows associated with the current user
  as a list of dictionaries with the format:
           {'user_allergies_row': row,
            'name':               row['name'],
            'description':        row['description'],
            'notes':              row['notes'],
            }
  """
  print(datetime.now(), '(server) in get_user_allergies_items()')

  rows = app_tables.user_allergies.search(tables.order_by("created", ascending=False),
                                          user=anvil.users.get_user())

  data_dict = [{'user_allergies_row': row,
                'name': row['name'],
                'description': row['description'],
                'notes': row['notes']}
               for row in rows]

  return data_dict


@anvil.server.callable(require_user=True)
def add_user_allergies(allergy_dict):
  """
  Add a new row to the user_allergies table for the current user
  based on contents of allergy_dict.

  Returns a single dictionary in the same format as get_user_allergies_items.
  """
  print(datetime.now(), '(server) in add_user_allergies()')

  new_row = safe_row_add('user_allergies', allergy_dict)

  data_dict = {'user_allergies_row': new_row,
               'name': new_row['name'],
               'description': new_row['description'],
               'notes': new_row['notes']}

  return data_dict


@anvil.server.callable(require_user=True)
def update_user_allergies(allergy, allergy_dict):
  """Update a allergy with allergy_dict."""
  print(datetime.now(), '(server) in update_user_allergies()')

  safe_row_update('user_allergies', allergy, allergy_dict)


@anvil.server.callable(require_user=True)
def delete_user_allergies(allergy):
  "Delete allergy from the user_allergies table."
  print(datetime.now(), '(server) in delete_user_allergies()')

  safe_row_delete('user_allergies', allergy)
