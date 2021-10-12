from datetime import datetime

from ._anvil_designer import AllergiesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Allergies(AllergiesTemplate):
  """
  Allow user's to view/edit all of their allergies.

  Notes
  ------
  1. self.repeating_panel is a client-side-cache of server-database rows.
      It allows for the consolidation of server calls to increase performance.
      It has the following structure:
          { 'user_allergies_row': <LiveObject: anvil.tables.Row>,
            'name':               <String>,
            'description':        <String>,
            'notes':              <String> }
  2. CRUD server routines:
          def add_user_allergies(allergy_dict):
          def get_user_allergies_items():
          def update_user_allergies(allergy, allergy_dict):
          def delete_user_allergies(allergy):
  3. In grid navigation, each header row counts as one (total of 3)
     and each card counts as 1, so a count of 13 is 10 cards.
  """

  def __init__(self, **properties):
    print(datetime.now(), f"in: {self.__class__.__name__}.__init__ {'*' * 40}")

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    ############################################################
    # Set event handlers
    ############################################################
    self.repeating_panel.set_event_handler('x-update-form', self.update_form)
    self.repeating_panel.set_event_handler('x-update-panel-item', self.update_panel_item)
    self.repeating_panel.set_event_handler('x-delete-panel-item', self.delete_panel_item)

    ############################################################
    # Update components
    ############################################################
    self.update_form()

    print(datetime.now(), f"out {self.__class__.__name__}.__init__")

  def update_form(self, **event_args):
    """Update form."""
    print(datetime.now(), f"in: {self.__class__.__name__}.update_form")

    self.update_panel_items()

  def update_panel_items(self, **event_args):
    """Update panel content from server."""
    print(datetime.now(), "in: {self.__class__.__name__}.update_panel_items")

    self.repeating_panel.items = anvil.server.call('get_user_allergies_items')

  def update_panel_item(self, item=None, **event_args):
    """
    Update an panel item's values to the server.
    """
    print(datetime.now(), "in: {self.__class__.__name__}.update_panel_item")

    # Pack dictionary with fields to update in the database
    allergy = item['user_allergies_row']
    allergy_dict = {'name': item['name'],
                    'description': item['description'],
                    'notes': item['notes']}

    anvil.server.call('update_user_allergies',
                      allergy,
                      allergy_dict)

  def delete_panel_item(self, item=None, **event_args):
    """
    Remove an item from client-side-cache and then remove it from the server.
    """
    print(datetime.now(), "in: {self.__class__.__name__}.delete_panel_item")

    # Find the client-side-cache index of the item to delete
    try:
      index = self.repeating_panel.items.index(item)
    except ValueError as e:
      print(datetime.now(), "Warning: Requst to delete non-existing row from self.repeating_panel.items",
            item, dict(item))
      return

    # Remove the item from the client-side-cache
    del self.repeating_panel.items[index]

    # Delete the item on the server
    anvil.server.call('delete_user_allergies', item['user_allergies_row'])

  def add_new_button_click(self, **event_args):
    """Add new item row based on header's textbox fields"""
    print(datetime.now(), "in: {self.__class__.__name__}.add_new_button_click")

    allergy_dict = {'name': self.new_name_textbox.text,
                    'description': self.new_description_textbox.text,
                    'notes': self.new_notes_textbox.text}
    self.new_name_textbox.text = ''
    self.new_description_textbox.text = ''
    self.new_notes_textbox.text = ''

    my_notification = Notification(f'New allergy adding to your database.', timeout=1.5)
    my_notification.show()

    new_row = anvil.server.call('add_user_allergies', allergy_dict)
    self.repeating_panel.items.insert(0, new_row)

    # setting repeating panel display to itself will refresh it
    self.repeating_panel.items = self.repeating_panel.items

  def form_show(self, **event_args):
    self.new_name_textbox.focus()
