###############################################################################
# Immunization Related Routines
###############################################################################
@anvil.server.callable(require_user=True)
def get_user_immunizations_items():
  """
  Get user_immunizations rows associated with the current user
  as a list of dictionaries with the format:
           {'user_immunizations_row': row,
            'name':                   row['name'],
            'notes':                  row['notes'],
            }
  """
  print(datetime.now(), '(server) in get_user_immunizations_items()')

  rows = app_tables.user_immunizations.search(tables.order_by("created", ascending=False),
                                              user=anvil.users.get_user())

  data_dict = [{'user_immunizations_row': row,
                'name': row['name'],
                'notes': row['notes']}
               for row in rows]

  return data_dict


@anvil.server.callable(require_user=True)
def add_user_immunizations(immunization_dict):
  """
  Add a new row to the user_immunizations table for the current user
  based on contents of immunization_dict.
  """
  print(datetime.now(), '(server) in add_user_immunizations()')

  new_row =  safe_row_add('user_immunizations', immunization_dict)

  data_dict = [{'user_immunizations_row': row,
                'name': row['name'],
                'notes': row['notes']}
               for row in rows]

  return data_dict

@anvil.server.callable(require_user=True)
def update_user_immunizations(immunization, immunization_dict):
  """Update a immunization with immunization_dict."""
  print(datetime.now(), '(server) in update_user_immunizations()')

  safe_row_update('user_immunizations', immunization, immunization_dict)


@anvil.server.callable(require_user=True)
def delete_user_immunizations(immunization):
  "Delete immunization from the user_immunizations table."
  print(datetime.now(), '(server) in delete_user_immunizations()')

  safe_row_delete('user_immunizations', immunization)

