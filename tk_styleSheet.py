import os.path



# ------------------------------------------------
#' MainWindow StyleSheet'
# ------------------------------------------------

#qt stylesheet reference
#http://doc.qt.io/qt-5/stylesheet-reference.html#qtabbar-widget


# COLOR_DARK     = #191919
# COLOR_MEDIUM   = #353535
# COLOR_MEDLIGHT = #5A5A5A
# COLOR_LIGHT    = #DDDDDD
# COLOR_ACCENT   = #AAAAFF


css='''




QWidget::item:selected {
	background: #AAAAFF;
}

QCheckBox, QRadioButton {
	border: none;
}

QRadioButton::indicator, QCheckBox::indicator {
	width: 13px;
	height: 13px;
}

QRadioButton::indicator::unchecked, QCheckBox::indicator::unchecked {
	border: 1px solid #5A5A5A;
	background: none;
}

QRadioButton::indicator:unchecked:hover, QCheckBox::indicator:unchecked:hover {
	border: 1px solid #DDDDDD;
}

QRadioButton::indicator::checked, QCheckBox::indicator::checked {
	border: 1px solid #5A5A5A;
	background: #5A5A5A;
}

QRadioButton::indicator:checked:hover, QCheckBox::indicator:checked:hover {
	border: 1px solid #DDDDDD;
	background: #DDDDDD;
}

QGroupBox {
	margin-top: 6px;
}

QGroupBox::title {
	top: -7px;
	left: 7px;
}

QScrollBar {
	border: 1px solid #5A5A5A;
	background: #191919;
}

QScrollBar:horizontal {
	height: 15px;
	margin: 0px 0px 0px 32px;
}

QScrollBar:vertical {
	width: 15px;
	margin: 32px 0px 0px 0px;
}

QScrollBar::handle {
	background: #353535;
	border: 1px solid #5A5A5A;
}

QScrollBar::handle:horizontal {
	border-width: 0px 1px 0px 1px;
}

QScrollBar::handle:vertical {
	border-width: 1px 0px 1px 0px;
}

QScrollBar::handle:horizontal {
	min-width: 20px;
}

QScrollBar::handle:vertical {
	min-height: 20px;
}

QScrollBar::add-line, QScrollBar::sub-line {
	background:#353535;
	border: 1px solid #5A5A5A;
	subcontrol-origin: margin;
}

QScrollBar::add-line {
	position: absolute;
}

QScrollBar::add-line:horizontal {
	width: 15px;
	subcontrol-position: left;
	left: 15px;
}

QScrollBar::add-line:vertical {
	height: 15px;
	subcontrol-position: top;
	top: 15px;
}

QScrollBar::sub-line:horizontal {
	width: 15px;
	subcontrol-position: top left;
}

QScrollBar::sub-line:vertical {
	height: 15px;
	subcontrol-position: top;
}


QScrollBar::add-page, QScrollBar::sub-page {
	background: none;
}

QAbstractButton:hover {
	background: #353535;
}

QAbstractButton:pressed {
	background: #5A5A5A;
}

QAbstractItemView {
	show-decoration-selected: 1;
	selection-background-color: #AAAAFF;
	selection-color: #DDDDDD;
	alternate-background-color: #353535;
}

QHeaderView {
	border: 1px solid #5A5A5A;
}

QHeaderView::section {
	background: #191919;
	border: 1px solid #5A5A5A;
	padding: 1px;
}

QHeaderView::section:selected, QHeaderView::section::checked {
	background: #353535;
}

QTableView {
	gridline-color: #5A5A5A;
}

QTabBar {
	margin-left: 2px;
}

QTabBar::tab {
	border-radius: 0px;
	padding: 1px;
	margin: 1px;
}

QTabBar::tab:selected {
	background: #353535;
}

QAbstractSpinBox {
	padding-right: 0px;
}



QSlider {
	border: none;
}

QSlider::groove:horizontal {
	height: 5px;
	margin: 4px 0px 4px 0px;
}

QSlider::groove:vertical {
	width: 5px;
	margin: 0px 4px 0px 4px;
}

QSlider::handle {
	border: 1px solid #5A5A5A;
	background: #353535;
}

QSlider::handle:horizontal {
	width: 15px;
	margin: -4px 0px -4px 0px;
}

QSlider::handle:vertical {
	height: 15px;
	margin: 0px -4px 0px -4px;
}

QSlider::add-page:vertical, QSlider::sub-page:horizontal {
	background: #AAAAFF;
}

QSlider::sub-page:vertical, QSlider::add-page:horizontal {
	background: #353535;
}

QLabel {
	border: none;
}

QProgressBar {
	text-align: center;
}

QProgressBar::chunk {
	width: 1px;
	background-color: #AAAAFF;
}

QMenu::separator {
	background: #353535;
}


QMainWindow {
	background-color: rgba(127,127,127,2); 
	color: rgb(225, 225, 225);
}

QToolTip {
	background-color: rgb(225,225,225);
	color: rgb(0,140,0);
	border: 1px solid black;
}

QPushButton::hover {   
	border: 1px solid black;
	border-radius: 5px;
	background-color: #AAAAFF;
	color: black;
}

QPushButton::pressed {   
	border: 1px solid black;
	border-radius: 5px;
	background-color: #AAAAFF;
	color: black;
}

QPushButton::checked {
	background-color: #AAAAFF;
	color: black;
}

QComboBox {
	background-color: rgba(100, 100, 100, 225);
	color: white;
	selection-background-color: #AAAAFF;
	selection-color: black;
}


QCheckBox::indicator:checked {
	background-color: #AAAAFF;
	color: black;
}



'''

# QPushButton {
#	border: 2px solid #8f8f91;
#	border-radius: 6px;
#	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
#                                       stop: 0 #f6f7fa, stop: 1 #dadbde);
#     min-width: 80px;
# }

# QPushButton:flat {
#	border: none; /* no border for a flat push button */
# }

# QPushButton:default {
#	border-color: navy; /* make the default button prominent */
# }

# QComboBox::down-arrow {
# 	border: 1px solid #5A5A5A;
# 	background: #353535;
# }

# QComboBox::drop-down {
# 	border: 1px solid #5A5A5A;
# 	background: #353535;
# }

# QComboBox::down-arrow {
# 	width: 3px;
# 	height: 3px;
# 	border: 1px solid #5A5A5A;
# }

# QScrollBar:left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow, QScrollBar::down-arrow {
# 	border: 1px solid #5A5A5A;
# 	width: 3px;
# 	height: 3px;
# }

# QAbstractSpinBox::up-arrow, QAbstractSpinBox::down-arrow {
# 	width: 3px;
# 	height: 3px;
# 	border: 1px solid #5A5A5A;
# }

# QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
# 	border: 1px solid #5A5A5A;
# 	background: #353535;
# 	subcontrol-origin: border;
# }

# QGroupBox {
# 	background-color: rgba(100,100,100,80);
# 	color: rgb(225, 225, 225);
# 	border: 3px solid black;
# 	};









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------