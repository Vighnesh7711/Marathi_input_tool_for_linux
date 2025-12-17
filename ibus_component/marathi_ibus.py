import sys
import os
import logging

# Setup debug logging to catch silent failures
logging.basicConfig(filename='/tmp/maza-marathi.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

logging.info("Starting Maza Marathi Engine...")

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# Add parent (for dev)
sys.path.append(os.path.join(current_dir, '..'))

try:
    import gi
    gi.require_version('IBus', '1.0')
    from gi.repository import IBus, GLib, GObject
    logging.info("IBus libraries imported successfully.")
except Exception as e:
    logging.error(f"Failed to import IBus/GI: {e}")
    sys.exit(1)

from src.im_controller import IMController

# Register the class as a GObject type explicitly
class MarathiEngine(IBus.Engine):
    __gtype_name__ = 'MarathiEngine'
    
    def __init__(self):
        super(MarathiEngine, self).__init__()
        logging.info("Initializing MarathiEngine instance...")
        try:
            self.controller = IMController()
            self.buffer = ""
            self.lookup_table = IBus.LookupTable.new(10, 0, True, True)
            logging.info("Controller loaded successfully.")
        except Exception as e:
            logging.error(f"Error in Engine init: {e}")

    def do_process_key_event(self, keyval, keycode, state):
        logging.debug(f"Key Event: val={keyval}, code={keycode}, state={state}")
        try:
            # Ignore key release events
            if state & IBus.ModifierType.RELEASE_MASK:
                return False
                
            # Ignore modifier keys (Ctrl, Alt) but allow Shift
            if state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK):
                return False

            # Handle Lookup Table Navigation if visible
            if self.lookup_table.get_number_of_candidates() > 0:
                if keyval == IBus.KEY_Page_Up:
                    self.lookup_table.page_up()
                    self.update_lookup_table(self.lookup_table, True)
                    return True
                elif keyval == IBus.KEY_Page_Down:
                    self.lookup_table.page_down()
                    self.update_lookup_table(self.lookup_table, True)
                    return True
                elif keyval == IBus.KEY_Up:
                    self.lookup_table.cursor_up()
                    self.update_lookup_table(self.lookup_table, True)
                    return True
                elif keyval == IBus.KEY_Down:
                    self.lookup_table.cursor_down()
                    self.update_lookup_table(self.lookup_table, True)
                    return True
                # Handle selection via numbers (1-5)
                elif IBus.KEY_1 <= keyval <= IBus.KEY_5:
                    pass 

            # Handle Backspace
            if keyval == IBus.KEY_BackSpace:
                if self.buffer:
                    self.buffer = self.buffer[:-1]
                    self.update()
                    return True
                return False

            # Handle Space / Enter (Commit)
            if keyval == IBus.KEY_space or keyval == IBus.KEY_Return:
                if self.buffer:
                    # Commit the selected suggestion
                    cursor_pos = self.lookup_table.get_cursor_pos()
                    candidate_text = ""
                    
                    if self.lookup_table.get_number_of_candidates() > 0:
                        candidate = self.lookup_table.get_candidate(cursor_pos)
                        candidate_text = candidate.get_text()
                    else:
                        # Fallback: Transliterate explicit if table empty (paranoia)
                        # Avoid commiting English buffer unless absolutely necessary
                        try:
                            fallback = self.controller.get_suggestions(self.buffer)
                            candidate_text = fallback[0] if fallback else self.buffer
                        except:
                            candidate_text = self.buffer
                    
                    # Train the dictionary (only if candidate differs from buffer to avoid learning english typos?)
                    # Actually we want to learn corrections.
                    self.controller.train(self.buffer, candidate_text)

                    # Commit
                    suffix = " " if keyval == IBus.KEY_space else ""
                    self.commit_text(IBus.Text.new_from_string(candidate_text + suffix))
                    
                    self.buffer = ""
                    self.lookup_table.clear()
                    self.hide_lookup_table()
                    self.hide_preedit_text()
                    return True
                return False

            # Handle Standard Characters (Ascii)
            if 32 < keyval < 127:
                char = chr(keyval)
                self.buffer += char
                self.update()
                return True

            return False
            
        except Exception as e:
            logging.error(f"Error processing key: {e}")
            return False # Fallback to default behavior

    def update(self):
        try:
            logging.debug(f"Update called. Buffer: '{self.buffer}'")
            
            if not self.buffer:
                self.hide_preedit_text()
                self.hide_lookup_table()
                return

            # Get suggestions
            suggestions = self.controller.get_suggestions(self.buffer)
            logging.debug(f"Suggestions: {suggestions}")
            
            # Update Preedit
            # ALWAYS show the first suggestion (Marathi) in preedit
            if suggestions:
                best_match = suggestions[0]
                logging.debug(f"Setting preedit to: '{best_match}'")
                
                # Create preedit text with underline
                preedit_text = IBus.Text.new_from_string(best_match)
                attrs = IBus.AttrList()
                attrs.append(IBus.Attribute.new(IBus.AttrType.UNDERLINE, IBus.AttrUnderline.SINGLE, 0, len(best_match)))
                preedit_text.set_attributes(attrs)
                
                # Cursor position 0 means start of preedit, True means visible
                self.update_preedit_text(preedit_text, 0, True)
            else:
                self.hide_preedit_text()

            # Update Lookup Table
            self.lookup_table.clear()
            if suggestions:
                for s in suggestions:
                    self.lookup_table.append_candidate(IBus.Text.new_from_string(s))
                
                self.update_lookup_table(self.lookup_table, True)
            else:
                self.hide_lookup_table()
                
        except Exception as e:
            logging.error(f"Error in update: {e}")


class IMApp:
    def __init__(self):
        self.bus = IBus.Bus()
        self.bus.request_name("org.freedesktop.IBus.MazaMarathi", 0)
        self.factory = IBus.Factory.new(self.bus.get_connection())
        # Correction: Use the python class directly, do not use from_name loop which requires GObject registration magic
        self.factory.add_engine("maza-marathi", MarathiEngine)

    def run(self):
        logging.info("Entering Main Loop")
        try:
            self.loop = GLib.MainLoop()
            self.loop.run()
        except Exception as e:
            logging.error(f"Error in Main Loop: {e}")

if __name__ == "__main__":
    try:
        IBus.init()
        app = IMApp()
        app.run()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")

