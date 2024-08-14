# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QLabel, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 712)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setSizeIncrement(QSize(1, 1))
        self.actionAuthenticate = QAction(MainWindow)
        self.actionAuthenticate.setObjectName(u"actionAuthenticate")
        self.actionUpdate_DB_Spot = QAction(MainWindow)
        self.actionUpdate_DB_Spot.setObjectName(u"actionUpdate_DB_Spot")
        self.actionRefresh_Lists = QAction(MainWindow)
        self.actionRefresh_Lists.setObjectName(u"actionRefresh_Lists")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.selectButton = QPushButton(self.centralwidget)
        self.selectButton.setObjectName(u"selectButton")

        self.gridLayout_2.addWidget(self.selectButton, 2, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setStyleSheet(u"")
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setFrameShape(QFrame.NoFrame)

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.applyTagsButton = QPushButton(self.centralwidget)
        self.applyTagsButton.setObjectName(u"applyTagsButton")

        self.gridLayout_2.addWidget(self.applyTagsButton, 2, 1, 1, 1)

        self.randomButton = QPushButton(self.centralwidget)
        self.randomButton.setObjectName(u"randomButton")

        self.gridLayout_2.addWidget(self.randomButton, 3, 0, 1, 1)

        self.modifyTagsButton = QPushButton(self.centralwidget)
        self.modifyTagsButton.setObjectName(u"modifyTagsButton")

        self.gridLayout_2.addWidget(self.modifyTagsButton, 3, 1, 1, 1)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")

        self.gridLayout_2.addWidget(self.listWidget, 1, 0, 1, 1)

        self.gridListView = QListView(self.centralwidget)
        self.gridListView.setObjectName(u"gridListView")
        self.gridListView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.gridListView.setResizeMode(QListView.Adjust)
        self.gridListView.setViewMode(QListView.IconMode)

        self.gridLayout_2.addWidget(self.gridListView, 1, 1, 1, 1)

        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 28))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menuMenu.addAction(self.actionAuthenticate)
        self.menuMenu.addAction(self.actionUpdate_DB_Spot)
        self.menuMenu.addAction(self.actionRefresh_Lists)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Spotifier", None))
        self.actionAuthenticate.setText(QCoreApplication.translate("MainWindow", u"Authenticate", None))
        self.actionUpdate_DB_Spot.setText(QCoreApplication.translate("MainWindow", u"Update DB", None))
        self.actionRefresh_Lists.setText(QCoreApplication.translate("MainWindow", u"Refresh Lists", None))
        self.selectButton.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Now Playing: Nothing.", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Unlabelled Songs", None))
        self.applyTagsButton.setText(QCoreApplication.translate("MainWindow", u"Apply Tags", None))
        self.randomButton.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.modifyTagsButton.setText(QCoreApplication.translate("MainWindow", u"Add/Remove Tags", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi

