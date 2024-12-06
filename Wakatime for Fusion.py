import os
import time
import requests
import adsk.core, adsk.fusion, adsk.cam, traceback
from configparser import ConfigParser
import platform

app = adsk.core.Application.get()
ui = app.userInterface

class WakaTimeManager:
    def __init__(self):
        # Load API key from the config file
        self.api_key = self.load_api_key()
        self.api_url = "https://waka.hackclub.com/api/heartbeats"  # Custom API URL from your .wakatime.cfg
        self.is_tracking = False
        self.document_opened_handler = None
        self.document_saved_handler = None
        self.document_activated_handler = None
        self.document_deactivated_handler = None
        self.command_created_handler = None  # Track command created event handler

    def load_api_key(self):
        """Load the API key from the .wakatime.cfg file."""
        config_file = os.path.expanduser("~/.wakatime.cfg")  # Path to the .wakatime.cfg file

        if not os.path.exists(config_file):
            print(f"Config file not found: {config_file}")
            return None
       
        config = ConfigParser()
        config.read(config_file)

        if 'settings' in config and 'api_key' in config['settings']:
            return config['settings']['api_key']
        else:
            print("API key not found in the configuration file.")
            return None

    def start_tracking(self):
        """Begin tracking Fusion 360 activity."""
        if not self.api_key:
            print("No API key provided. Tracking cannot start.")
            return

        self.is_tracking = True

        # Check if there's an active document
        if app.activeDocument is None:
            print("No active document open.")
            return

        try:
            # Create and add event handlers to the application object (not the document)
            self.document_opened_handler = DocumentEventHandler(self.on_file_opened)
            app.documentOpened.add(self.document_opened_handler)

            self.document_saved_handler = DocumentEventHandler(self.on_file_saved)
            app.documentSaved.add(self.document_saved_handler)

            self.document_activated_handler = DocumentEventHandler(self.on_document_activated)
            app.documentActivated.add(self.document_activated_handler)

            self.document_deactivated_handler = DocumentEventHandler(self.on_document_deactivated)
            app.documentDeactivated.add(self.document_deactivated_handler)

            # Correctly add the commandCreated event handler to `ui.commandCreated`
            self.command_created_handler = CommandEventHandler(self.on_command_created)
            ui.commandCreated.add(self.command_created_handler)  # Correct usage with the `ui` object

            print("Tracking started.")  # Debugging

            # Send test heartbeat
            self.send_test_heartbeat()

        except Exception as e:
            print(f"Error while starting tracking: {str(e)}")

    def send_test_heartbeat(self):
        """Send a test heartbeat with project and file information."""
        os_info = platform.system()
        language = "Fusion 360"
        editor = "Fusion 360"
        active_document = app.activeDocument
        
        #find current file and project
        if active_document is None:
            print("No active document found.")
            return
        file_name = active_document.name
        project_name = self.get_project_name(active_document)

        payload = {
            "time": time.time(),
            "entity": file_name,
            "project": project_name,
            "type": "file",
            "category": "test_start",
            "language": language,
            "Editor": editor,
            "os": os_info
        }

        headers = {
            "Authorization": f"Basic {self.api_key}"
        }

        print(f"Preparing to send test heartbeat: {payload}")

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code != 201:
                print(f"Failed to send test heartbeat: {response.text}")
            else:
                print(f"Test heartbeat sent successfully: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending test heartbeat: {str(e)}")

    def stop_tracking(self):
        """Stop tracking Fusion 360 activity."""
        self.is_tracking = False
        print("Tracking stopped.")  # Debugging

        # Remove event handlers when stopping
        try:
            if self.document_opened_handler:
                app.documentOpened.remove(self.document_opened_handler)
                self.document_opened_handler = None

            if self.document_saved_handler:
                app.documentSaved.remove(self.document_saved_handler)
                self.document_saved_handler = None

            if self.document_activated_handler:
                app.documentActivated.remove(self.document_activated_handler)
                self.document_activated_handler = None

            if self.document_deactivated_handler:
                app.documentDeactivated.remove(self.document_deactivated_handler)
                self.document_deactivated_handler = None

            # Remove the commandCreated event handler correctly
            if self.command_created_handler:
                ui.commandCreated.remove(self.command_created_handler)
                self.command_created_handler = None

            print("Event handlers removed successfully.")  # Debugging
        except Exception as e:
            print(f"Error while removing event handlers: {str(e)}")

    def on_file_opened(self, args):
        """Handle file opened event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"File Opened: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        entity_name = args.document.name  # Changed to entity_name for consistency
        print(f"Project Name: {project_name}, Entity Name: {entity_name}")  # Debugging
        self.send_heartbeat(project_name, entity_name, "file_opened", extra_info={"action": "open"})

    def on_file_saved(self, args):
        """Handle file saved event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"File Saved: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        entity_name = args.document.name  # Changed to entity_name for consistency
        print(f"Project Name: {project_name}, Entity Name: {entity_name}")  # Debugging
        self.send_heartbeat(project_name, entity_name, "file_saved", extra_info={"action": "save"})

    def on_document_activated(self, args):
        """Handle document activated event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"Document Activated: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        entity_name = args.document.name  # Changed to entity_name for consistency
        print(f"Project Name: {project_name}, Entity Name: {entity_name}")  # Debugging
        self.send_heartbeat(project_name, entity_name, "document_activated", extra_info={"action": "activate"})

    def on_document_deactivated(self, args):
        """Handle document deactivated event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"Document Deactivated: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        entity_name = args.document.name  # Changed to entity_name for consistency
        print(f"Project Name: {project_name}, Entity Name: {entity_name}")  # Debugging
        self.send_heartbeat(project_name, entity_name, "document_deactivated", extra_info={"action": "deactivate"})

    def on_command_created(self, args):
        """Handle command created event."""
        if not self.is_tracking or not self.api_key:
            return

        try:
            # Log the available attributes in args to help debug
            print(f"Event Args: {dir(args)}")

            # Check if 'commandDefinition' exists
            if hasattr(args, 'commandDefinition'):
                command_definition = args.commandDefinition
                print(f"Command Created: {command_definition.name}")  # Log command name

                project_name = "Fusion 360"  # Get the project name
                entity_name = command_definition.name  # Changed to entity_name for consistency

                # Add extra info such as the action type
                extra_info = {"action": "create"}
                self.send_heartbeat(project_name, entity_name, "command_created", extra_info=extra_info)
            else:
                print("No 'commandDefinition' attribute in ApplicationCommandEventArgs.")
                print(f"Other available attributes in event args: {vars(args)}")
        except Exception as e:
            print(f"Error in on_command_created: {str(e)}")

    def get_project_name(self, document):
        """Get the project name from the document."""
        try:
            # Use the dataFile property to access project-related details
            if document.dataFile and document.dataFile.parentProject:
                project_name = document.dataFile.parentProject.name
            else:
                project_name = "Unknown Project"
        except Exception as e:
            print(f"Error getting project name: {e}")
            project_name = "Unknown Project"
        return project_name

    def send_heartbeat(self, project_name, entity_name, action_type, extra_info=None):
        """Send activity data to WakaTime."""
        os_info = platform.system()
        language = "Fusion 360"
        editor = "Fusion 360"
        active_document = app.activeDocument
        
        #find current file and project
        if active_document is None:
            print("No active document found.")
            return
        file_name = active_document.name
        project_name = self.get_project_name(active_document)
        
        # Debugging print statement with more detailed info
        print(f"Preparing to send heartbeat: {{'time': {time.time()}, 'entity': '{file_name}', 'project': '{project_name}', 'type': 'file', 'category': '{action_type}', 'language': '{language}', 'Editor': '{editor}', 'os': '{os_info}'}}")

        # Construct the payload with more detailed information
        payload = {
            "time": time.time(),
            "entity": file_name,
            "project": project_name,
            "type": "file",
            "category": action_type,
            "Language": language,
            "Editor": editor,
            "OperatingSystem": os_info
        }

        if extra_info:
            payload.update(extra_info)  # Update with additional details like action

        headers = {
            "Authorization": f"Basic {self.api_key}"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code != 201:
                print(f"Failed to send heartbeat: {response.text}")
            else:
                print(f"Heartbeat sent successfully: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending heartbeat: {str(e)}")


class DocumentEventHandler(adsk.core.DocumentEventHandler):
    """Custom event handler for document events."""

    def __init__(self, handler_function):
        super().__init__()
        self.handler_function = handler_function

    def notify(self, args):
        """Notify the event handler."""
        self.handler_function(args)


class CommandEventHandler(adsk.core.ApplicationCommandEventHandler):
    """Custom event handler for command created events."""

    def __init__(self, handler_function):
        super().__init__()
        self.handler_function = handler_function

    def notify(self, args):
        """Notify the event handler."""
        self.handler_function(args)

waka_manager = None

def run(context):
    global waka_manager
    try:
        # Initialize WakaTime manager
        waka_manager = WakaTimeManager()
        waka_manager.start_tracking()  # Start tracking Fusion 360 activity

    except Exception as e:
        print(f"Error: {str(e)}")
        if waka_manager:
            waka_manager.stop_tracking()  # Ensure we stop tracking on error
