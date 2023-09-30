import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: window
    width: 400
    height: 580
    visible: true
    title: qsTr("Login Page")

    Drawer {
        id: navDrawer
        width: 200 // Set the width of the navigation drawer
        height: parent.height
        edge: Qt.LeftEdge

        Rectangle {
            width: navDrawer.width
            height: parent.height
            // color: "lightgray"

            // Add your navigation items here
            ListView {
                anchors.fill: parent
                model: ListModel {
                    ListElement { text: "Home" }
                    ListElement { text: "Profile" }
                    ListElement { text: "Settings" }
                }

                delegate: Item {
                    width: parent.width
                    height: 50
                    Text {
                        text: model.text
                        anchors.centerIn: parent
                    }

                    // Handle item clicks here
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            // Handle the click action (e.g., switch pages)
                            console.log("Clicked on", model.text);
                            navDrawer.close(); // Close the drawer after clicking an item
                        }
                    }
                }
            }
        }
    }

    // Add a button to open/close the navigation drawer
    Button {
        text: "☰"
        onClicked: {
            if (navDrawer.status === Drawer.Closed) {
                navDrawer.open();
            } else {
                navDrawer.close();
            }
        }
    }
}
