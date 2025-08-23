import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 1024
    height: 768
    color: "#ffffff"

    Column {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Label {
            text: qsTr("Übersicht")
            font.pointSize: 18
        }

        Rectangle {
            width: parent.width
            height: 200
            color: "#e0f7fa"
            Text {
                anchors.centerIn: parent
                text: qsTr("Termine und Aufgaben werden hier angezeigt.")
            }
        }

        Rectangle {
            width: parent.width
            height: 40
            color: "#eeeeee"
            Label {
                anchors.centerIn: parent
                text: qsTr("Status: Bereit")
                font.pointSize: 14
            }
        }
    }
}
