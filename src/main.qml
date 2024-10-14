import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    title: "Clock"

    Rectangle {
        anchors.fill: parent

        Image {
            anchors.fill: parent
            source: "./ui/background.png"
            fillMode: Image.PreserveAspectCrop
        }

        Rectangle {
            anchors.fill: parent
            color: "transparent"

            Text {
                text: "16:38:33"
                font.pixelSize: 24
                color: "white"
            }

        }

    }

}

