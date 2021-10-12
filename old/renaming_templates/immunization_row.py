from datetime import datetime

from ._anvil_designer import ImmunizationsRowTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ImmunizationsRow(ImmunizationsRowTemplate):
  """
  View/Edit a single row of Immunizations.repeating_panel.items.

  Notes
  ------
  1. See Immunizations for details of format of self.items

        self.item is in the format:
            { 'user_immunizations_row': <LiveObject: anvil.tables.Row>,
              'name':               <String>,
              'notes':              <String> }

  2. repeating_panel event handlers
      self.repeating_panel.set_event_handler('x-update-form', self.update_form)
      self.repeating_panel.set_event_handler('x-update-panel-item', self.update_panel_item)
      self.repeating_panel.set_event_handler('x-delete-panel-item', self.delete_panel_item)
  3. The item dict will initialized only have the members in note 1.
     If an item is reset by a call to the server, it will be reinitialized.
  4. To avoid having edited but unsaved data lost on sorting/refreshing of other rows,
     item uses the unsaved_edits and other keys to retain state.
    """

  def __init__(self, **properties):
    print(datetime.now(), f"in: {self.__class__.__name__}.__init__ {'*' * 40}")

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    ############################################################
    # Set attributes
    ############################################################

    ############################################################
    # Update components
    ############################################################
    self.set_panel_visibility()

    print(datetime.now(), f"out {self.__class__.__name__}.__init__ ")

  def set_panel_visibility(self):
    """Set visibility for row panels and buttons."""
    print(datetime.now(), f"in: {self.__class__.__name__}.set_panel_visibility")

    # Determine which rows are visible by checking if there are unsaved edits
    if 'unsaved_edits' in self.item and self.item['unsaved_edits'] is True:
      # Edit mode
      view_visable = False
      edit_visable = True
    else:
      # View mode
      view_visable = True
      edit_visable = False

    self.name_view_row_panel.visible = view_visable
    self.note_view_row_panel.visible = view_visable

    self.name_edit_row_panel.visible = edit_visable
    self.note_edit_row_panel.visible = edit_visable

    # Show only the buttons that are valid for the mode
    self.edit_button.visible = view_visable
    self.delete_button.visible = view_visable
    self.save_button.visible = edit_visable
    self.undo_button.visible = edit_visable

  def edit_button_click(self, **event_args):
    """
    The edit_button_click handler will do the following:
      1. Hide the view panels
      2. Show the edit panels
      3. Set the components to their last cached value or self.item value
    """
    print(datetime.now(), f"in: {self.__class__.__name__}.edit_button_click")

    self.item['unsaved_edits'] = True
    self.set_panel_visibility()

    # Initialize edit components with view data
    # edit components use databinding for temporary persistence
    self.name_edit_textbox.text = self.item['name']
    self.notes_edit_textbox.text = self.item['notes']

  def save_button_click(self, **event_args):
    """
    The save_button_click handler will do the following:
      1. Hide the edit panels
      2. Shows the view panels
      3. Save values to database if changed (by passing to parent.panel)
      4. Show placeholder information about database change in one of the textboxes.
    """
    print(datetime.now(), f"in: {self.__class__.__name__}.save_button_click")

    self.item['unsaved_edits'] = False
    self.set_panel_visibility()

    # Find the saved values from item
    old_name = self.item['name']
    old_notes = self.item['notes']

    # Find the proposed values from edit components
    new_name = self.name_edit_textbox.text
    new_notes = self.notes_edit_textbox.text

    # If data did not change then no database updating required
    if (new_name == old_name) and (new_notes == old_notes):
      print(f"Input data did not change, no database calls required")
      return

    # Update item with new user input
    self.item['name'] = new_name
    self.item['notes'] = new_notes
    self.refresh_data_bindings()

    self.parent.raise_event('x-update-panel-item', item=self.item)

  def delete_button_click(self, **event_args):
    """Delete panel item."""
    print(datetime.now(), f"in: {self.__class__.__name__}.delete_button_click")

    reply = confirm(f"Are you sure you want to delete this immunization?")
    if reply:
      self.delete_button.enabled = False
      self.parent.raise_event('x-delete-panel-item', item=self.item)
      self.remove_from_parent()

  def undo_button_click(self, **event_args):
    """Cancel edit to panel item.  Shows the view panels and hides the edit panels."""
    print(datetime.now(), f"in: {self.__class__.__name__}.undo_button_click")

    self.item['unsaved_edits'] = False
    self.set_panel_visibility()
