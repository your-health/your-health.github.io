###############################################################################
# Contact Related Routines
###############################################################################
@anvil.server.callable(require_user=True)
def get_user_contacts_iter():
  """Get the contacts row iter associated with the current user."""
  print(datetime.now(), '(server) in get_user_contacts()')

  current_user = anvil.users.get_user()
  contacts = app_tables.user_contacts.search(tables.order_by("created", ascending=False),
                                             user=current_user)
  return contacts


@anvil.server.callable(require_user=True)
def add_user_contact(contact_dict):
  """Add a contact for current user based on contact_dict."""
  print(datetime.now(), '(server) in add_user_contact()')

  safe_row_add('user_contacts', contact_dict)


@anvil.server.callable
def update_user_contact(contact, contact_dict):
  """Update a contact row based on contact_dict."""
  print(datetime.now(), '(server) in update_user_contact()')

  safe_row_update('user_contacts', contact, contact_dict)


@anvil.server.callable
def delete_user_contact(contact):
  """Delete contact."""
  print(datetime.now(), '(server) in delete_user_contact()')

  safe_row_delete('user_contacts', contact)