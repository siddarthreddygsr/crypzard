import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTextEdit
from PyQt5 import QtWidgets

class UfwGui(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the GUI
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("UFW GUI")
        self.setGeometry(100, 100, 600, 400)

        # Create a label to display firewall status
        self.status_label = QLabel("Firewall Status: ", self)
        self.status_label.setGeometry(20, 20, 200, 30)

        # Create buttons for various actions
        self.enable_button = QPushButton("Enable Firewall", self)
        self.enable_button.setGeometry(20, 60, 150, 30)
        self.enable_button.clicked.connect(self.enable_firewall)

        self.disable_button = QPushButton("Disable Firewall", self)
        self.disable_button.setGeometry(200, 60, 150, 30)
        self.disable_button.clicked.connect(self.disable_firewall)

        self.reset_button = QPushButton("Reset Firewall", self)
        self.reset_button.setGeometry(380, 60, 150, 30)
        self.reset_button.clicked.connect(self.reset_firewall)

        self.list_rules_button = QPushButton("List Rules", self)
        self.list_rules_button.setGeometry(20, 100, 150, 30)
        self.list_rules_button.clicked.connect(self.list_rules)

        self.add_rule_button = QPushButton("Add Rule", self)
        self.add_rule_button.setGeometry(200, 100, 150, 30)
        self.add_rule_button.clicked.connect(self.add_rule)

        self.delete_rule_button = QPushButton("Delete Rule", self)
        self.delete_rule_button.setGeometry(380, 100, 150, 30)
        self.delete_rule_button.clicked.connect(self.delete_rule)

        # Create a QTextEdit widget to display rule listing and adding
        self.rules_text_edit = QTextEdit(self)
        self.rules_text_edit.setGeometry(20, 150, 550, 200)

    def reset_firewall(self):
        subprocess.run(["sudo","ufw","--force","reset"])

        self.update_status_label()
        

    def enable_firewall(self):
        # Run the 'ufw enable' command as a subprocess with sudo
        subprocess.run(["sudo", "ufw", "enable"])

        # Update the status label to display the new firewall status
        self.update_status_label()

    def disable_firewall(self):
        # Run the 'ufw disable' command as a subprocess with sudo
        subprocess.run(["sudo", "ufw", "disable"])

        # Update the status label to display the new firewall status
        self.update_status_label()

    def list_rules(self):
        # Run the 'ufw status' command to list firewall rules
        rules_output = subprocess.getoutput("sudo ufw status")
        self.rules_text_edit.setPlainText(rules_output)

    def add_rule(self):
        # Open a dialog to input a new rule
        new_rule, ok = QtWidgets.QInputDialog.getText(
            self, "Add Rule", "Enter a new firewall rule (e.g., allow 80/tcp):"
        )
        new_rule = new_rule.split()
        precommand = ['sudo','ufw']
        precommand.extend(new_rule)
        print(precommand)
        if ok:
            # Run the 'ufw allow' or 'ufw deny' command with the new rule
            subprocess.run(precommand)

            # Update the displayed rules
            self.list_rules()

    def delete_rule(self):
        # Open a dialog to input the rule to be deleted
        rule_to_delete, ok = QtWidgets.QInputDialog.getText(
            self, "Delete Rule", "Enter the firewall rule to delete:"
        )

        if ok:
            # Run the 'ufw delete' command to delete the specified rule
            subprocess.run(["sudo", "ufw", "delete", rule_to_delete])

            # Update the displayed rules
            self.list_rules()

    def update_status_label(self):
        # Retrieve the current firewall status using 'ufw status' command
        status = subprocess.getoutput("sudo ufw status")

        # Update the status label text to reflect the current status
        self.status_label.setText(f"Firewall Status: {status}")

def main():
    # Create a PyQt5 application
    app = QApplication(sys.argv)

    # Create an instance of the UfwGui class
    ufw_app = UfwGui()

    # Show the GUI
    ufw_app.show()

    # Run the application's event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
