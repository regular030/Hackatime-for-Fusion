import os
import time
import requests
import adsk.core, adsk.fusion, adsk.cam, traceback
from configparser import ConfigParser

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

                        # Track user commands
            self.command_started_handler = CommandEventHandler(self.on_command_started)
            app.commandStarting.add(self.command_started_handler)

            self.command_terminated_handler = CommandEventHandler(self.on_command_terminated)
            app.commandTerminated.add(self.command_terminated_handler)

            print("Tracking started.")  # Debugging
        except Exception as e:
            print(f"Error while starting tracking: {str(e)}")

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

            print("Event handlers removed successfully.")  # Debugging
        except Exception as e:
            print(f"Error while removing event handlers: {str(e)}")

    def on_file_opened(self, args):
        """Handle file opened event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"File Opened: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        file_name = args.document.name
        print(f"Project Name: {project_name}, File Name: {file_name}")  # Debugging
        self.send_heartbeat(project_name, file_name, "file_opened", extra_info={"action": "open"})

    def on_file_saved(self, args):
        """Handle file saved event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"File Saved: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        file_name = args.document.name
        print(f"Project Name: {project_name}, File Name: {file_name}")  # Debugging
        self.send_heartbeat(project_name, file_name, "file_saved", extra_info={"action": "save"})

    def on_document_activated(self, args):
        """Handle document activated event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"Document Activated: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        file_name = args.document.name
        print(f"Project Name: {project_name}, File Name: {file_name}")  # Debugging
        self.send_heartbeat(project_name, file_name, "document_activated", extra_info={"action": "activate"})

    def on_document_deactivated(self, args):
        """Handle document deactivated event."""
        if not self.is_tracking or not self.api_key:
            return
        print(f"Document Deactivated: {args.document.name}")  # Debugging
        project_name = self.get_project_name(args.document)
        file_name = args.document.name
        print(f"Project Name: {project_name}, File Name: {file_name}")  # Debugging
        self.send_heartbeat(project_name, file_name, "document_deactivated", extra_info={"action": "deactivate"})

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

    #Project data
    def send_heartbeat(self, project_name, entity_name, action_type, extra_info=None):
        """Send activity data to WakaTime."""
        print(f"Sending Heartbeat: Project - {project_name}, File - {entity_name}, Action - {action_type}")  # Debugging
        payload = {
            "time": time.time(),
            "entity": entity_name,
            "project": project_name,
            "type": "file",
            "category": action_type,
            "language": "Fusion 360",
        }

        if extra_info:
            payload.update(extra_info)

        headers = {
            "Authorization": f"Basic {self.api_key}"
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code != 201:
                print(f"Failed to send heartbeat: {response.text}")
            else:
                print(f"Heartbeat sent successfully: {response.status_code}")  # Debugging
        except requests.RequestException as e:
            print(f"Error sending heartbeat: {str(e)}")


# Fusion 360 event handling
class DocumentEventHandler(adsk.core.DocumentEventHandler):
    """Custom event handler for document events."""
    
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

        if not waka_manager.api_key:
            print("Failed to load API key.")
            return

        # Start tracking
        print(f"API Key Loaded: {waka_manager.api_key}")  # Debugging: Log the API key
        waka_manager.start_tracking()
    except Exception as e:
        if ui:
            ui.messageBox(f"Failed to start WakaTime Add-In:\n{str(e)}\n{traceback.format_exc()}")

def stop(context):
    global waka_manager
    try:
        # Stop tracking only if the manager is initialized
        if waka_manager:
            waka_manager.stop_tracking()
            waka_manager = None

        # Notify the user that tracking has stopped
        ui.messageBox("WakaTime Add-In has stopped.")
        print("WakaTime Add-In has stopped.")  # Debugging
    except Exception as e:
        if ui:
            ui.messageBox(f"Failed to stop WakaTime Add-In:\n{str(e)}\n{traceback.format_exc()}")
