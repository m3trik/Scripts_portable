import os.path





#qt stylesheet reference
#http://doc.qt.io/qt-5/stylesheet-reference.html#qtabbar-widget




# ------------------------------------------------
#' MainWindow StyleSheet'
# ------------------------------------------------
class StyleSheet():
	'''
	COLOR_DARK     = #191919
	COLOR_MEDIUM   = #353535
	COLOR_MEDLIGHT = #5A5A5A
	COLOR_LIGHT    = #DDDDDD
	COLOR_ACCENT   = rgba(82,133,166,200)
	'''
	QMainWindow='''
		QMainWindow {
			background-color: transparent; 
			color: rgb(225, 225, 225);
		}'''

	QWidget='''
		QWidget::item:selected {
			background: rgba(82,133,166,200);
		}'''

	QPushButton='''
		QPushButton {
			border: 1px solid black;
			background-color: rgba(100,100,100,200);
		}

		QPushButton::checked {
			border: 1px solid black;
			background-color: rgba(82,133,166,200);
			color: black;
		}

		QPushButton::hover {   
			border: 1px solid black;
			background-color: rgba(82,133,166,200);
			color: white;
		}

		QPushButton::unchecked::hover {
			background-color: rgba(0,0,0,0);
			color: rgba(82,133,166,200);
		}

		QPushButton::checked::hover {
			background-color: rgba(0,0,0,0);
			color: rgba(82,133,166,200);
		}

		QPushButton::pressed {   
			border: 1px solid black;
			background-color: rgba(82,133,166,200);
			color: white;
		}

		QPushButton:flat {
			border: none; /* no border for a flat push button */
		}

		QPushButton:default {
			border-color: navy; /* make the default button prominent */
		}'''

	QAbstractButton='''
		QAbstractButton:hover {
			background: #353535;
		}

		QAbstractButton:pressed {
			background: #5A5A5A;
		}'''

	QComboBox='''
		QComboBox {
			background-color: rgba(100,100,100,200);
			color: white;
			selection-background-color: rgba(82,133,166,200);
			/*selection-color: black;*/
		}

		QComboBox:open {
			background-color: rgba(100,100,100,200);
			color: white;
			selection-background-color: rgba(82,133,166,200);
		}

		QComboBox::down-arrow {
			width: 3px;
			height: 3px;
			border: 1px solid #5A5A5A;
			border: 1px solid #5A5A5A;
			background: #353535;
		}

		QComboBox::drop-down {
			border: 1px solid #5A5A5A;
			background: #353535;
		}'''

	# QComboBox_cmb='''
	# 	QComboBox {
	# 		background: rgba(100,100,100,50);
	# 	}'''

	QSpinBox='''
		QSpinBox {

		}'''

	QDoubleSpinBox='''
		QDoubleSpinBox {

		}'''

	QAbstractSpinBox='''
		QScrollBar:left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow, QScrollBar::down-arrow {
			border: 1px solid #5A5A5A;
			width: 3px;
			height: 3px;
		}

		QAbstractSpinBox::up-arrow, QAbstractSpinBox::down-arrow {
			width: 3px;
			height: 3px;
			border: 1px solid #5A5A5A;
		}

		QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
			border: 1px solid #5A5A5A;
			background: #353535;
			subcontrol-origin: border;
		}'''

	QCheckBox='''
		QCheckBox, QRadioButton {
			border: none;
		}'''

	QRadioButton='''
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
		}'''

	QAbstractItemView='''
		QAbstractItemView {
			show-decoration-selected: 1;
			selection-background-color: rgba(82,133,166,200);
			selection-color: #DDDDDD;
			alternate-background-color: #353535;
		}'''

	QHeaderView='''
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
		}'''

	QTableView='''
		QTableView {
			gridline-color: #5A5A5A;
		}'''

	QTextEdit='''
		QTextEdit {

		}'''

	QAbstractSpinBox='''
		QAbstractSpinBox {
			padding-right: 0px;
		}'''

	QSlider='''
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
			background: rgba(82,133,166,200);
		}

		QSlider::sub-page:vertical, QSlider::add-page:horizontal {
			background: #353535;
		}'''

	QScrollBar='''
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
		}'''

	QGroupBox='''
		QGroupBox {
			margin-top: 4px;
			background-color: rgba(100,100,100,80);
			color: rgb(225, 225, 225);
			border: none;
		}

		QGroupBox::title {
			top: -7px;
			left: 7px;
		}'''

	QTabBar='''
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
		}'''

	QMenu='''
		QMenu::separator {
			background: #353535;
		}'''

	QLabel='''
		QLabel {
			border: none;
		}'''

	QToolTip='''
		QToolTip {
			background-color: rgba(225,225,225,225);
			color: black;
			border: 1px solid black;
		}'''

	QProgressBar='''
		QProgressBar {
			text-align: center;
		}

		QProgressBar::chunk {
			width: 1px;
			background-color: rgba(82,133,166,200);
		}'''



# background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde);
# min-width: 80px;











#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# testWidget.setObjectName("myWidget")
# testWidget.setStyleSheet("#myWidget {background-color:red;}") 


# background-color: #ABABAB; /* sets background of the menu */
# border: 1px solid black;

# /* sets background of menu item. set this to something non-transparent
# if you want menu color and menu item color to be different */
# background-color: transparent;

# QMenu::item:selected { /* when user selects item using mouse or keyboard */
#     background-color: #654321;
# For a more advanced customization, use a style sheet as follows:

# QMenu {
#     background-color: white;
#     margin: 2px; /* some spacing around the menu */

# QMenu::item {
#     padding: 2px 25px 2px 20px;
#     border: 1px solid transparent; /* reserve space for selection border */

# QMenu::item:selected {
#     border-color: darkblue;
#     background: rgba(100, 100, 100, 150);
# }

# QMenu::icon:checked { /* appearance of a 'checked' icon */
#     background: gray;
#     border: 1px inset gray;
#     position: absolute;
#     top: 1px;
#     right: 1px;
#     bottom: 1px;
#     left: 1px;

# QPushButton {
# 	background:rgba(127,127,127,2);
# 	background-color: red;
# 	color: white;
# 	border-width: 2px;
# 	border-radius: 10px;
# 	border-color: beige;
# 	border-style: outset;
# 	font: bold 14px;
# 	min-width: 10em;
# 	padding: 5px;

# QPushButton:hover {   
# 	border: 1px solid black;
# 	border-radius: 5px;   
# 	background-color:#66c0ff;

# QPushButton:pressed {
# 	background-color: rgb(224, 0, 0);
# 	border-style: inset;

# QPushButton:enabled {
# 	color: red

# QComboBox {
# 	image: url(:/none);}

# QComboBox::drop-down {
# 	border-width: 0px; 
# 	color: transparent

# QComboBox::down-arrow {
# 	border: 0px solid transparent; 
# 	border-width: 0px; left: 0px; top: 0px; width: 0px; height: 0px; 
# 	background-color: transparent; 
# 	color: transparent; 
# 	image: url(:/none);

# QTreeWidget {
# 	border:none;
# } 

# QTreeWidget::item {
# 	height: 20px;

# QTreeView {
#   alternate-background-color: rgba(35,35,35,255);
#   background: rgba(45,45,45,255);
# }

# QMenu {
# 	background-color: white; /* background-color: #ABABAB; sets background of the menu */
# 	margin: 2px; /* some spacing around the menu */
# 	border: 1px solid black;
# }

# QMenu::item {
# 	/* sets background of menu item. set this to something non-transparent
# 	if you want menu color and menu item color to be different */
# 	background-color: transparent;
# 	padding: 2px 25px 2px 20px;
# 	border: 1px solid transparent; /* reserve space for selection border */
# }

# QMenu::item:selected { 
# 	/* when user selects item using mouse or keyboard */
# 	background-color: #654321;
# 	border-color: darkblue;
# 	background: rgba(100, 100, 100, 150);
# }

# QMenu::icon:checked { /* appearance of a 'checked' icon */
# 	background: gray;
# 	border: 1px inset gray;
# 	position: absolute;
# 	top: 1px;
# 	right: 1px;
# 	bottom: 1px;
# 	left: 1px;
# }




'''


List of Pseudo-States:
:active				This state is set when the widget resides in an active window.
:adjoins-item		This state is set when the ::branch of a QTreeView is adjacent to an item.
:alternate			This state is set for every alternate row whe painting the row of a QAbstractItemView when QAbstractItemView::alternatingRowColors() is set to true.
:bottom				The item is positioned at the bottom. For example, a QTabBar that has its tabs positioned at the bottom.
:checked			The item is checked. For example, the checked state of QAbstractButton.
:closable			The items can be closed. For example, the QDockWidget has the QDockWidget::DockWidgetClosable feature turned on.
:closed				The item is in the closed state. For example, an non-expanded item in a QTreeView
:default			The item is the default. For example, a default QPushButton or a default action in a QMenu.
:disabled			The item is disabled.
:editable			The QComboBox is editable.
:edit-focus			The item has edit focus (See QStyle::State_HasEditFocus). This state is available only for Qt Extended applications.
:enabled			The item is enabled.
:exclusive			The item is part of an exclusive item group. For example, a menu item in a exclusive QActionGroup.
:first				The item is the first (in a list). For example, the first tab in a QTabBar.
:flat				The item is flat. For example, a flat QPushButton.
:floatable			The items can be floated. For example, the QDockWidget has the QDockWidget::DockWidgetFloatable feature turned on.
:focus				The item has input focus.
:has-children		The item has children. For example, an item in a QTreeView that has child items.
:has-siblings		The item has siblings. For example, an item in a QTreeView that siblings.
:horizontal			The item has horizontal orientation
:hover				The mouse is hovering over the item.
:indeterminate		The item has indeterminate state. For example, a QCheckBox or QRadioButton is partially checked.
:last				The item is the last (in a list). For example, the last tab in a QTabBar.
:left				The item is positioned at the left. For example, a QTabBar that has its tabs positioned at the left.
:maximized			The item is maximized. For example, a maximized QMdiSubWindow.
:middle				The item is in the middle (in a list). For example, a tab that is not in the beginning or the end in a QTabBar.
:minimized			The item is minimized. For example, a minimized QMdiSubWindow.
:movable			The item can be moved around. For example, the QDockWidget has the QDockWidget::DockWidgetMovable feature turned on.
:no-frame			The item has no frame. For example, a frameless QSpinBox or QLineEdit.
:non-exclusive		The item is part of a non-exclusive item group. For example, a menu item in a non-exclusive QActionGroup.
:off				For items that can be toggled, this applies to items in the "off" state.
:on					For items that can be toggled, this applies to widgets in the "on" state.
:only-one			The item is the only one (in a list). For example, a lone tab in a QTabBar.
:open				The item is in the open state. For example, an expanded item in a QTreeView, or a QComboBox or QPushButton with an open menu.
:next-selected		The next item (in a list) is selected. For example, the selected tab of a QTabBar is next to this item.
:pressed			The item is being pressed using the mouse.
:previous-selected	The previous item (in a list) is selected. For example, a tab in a QTabBar that is next to the selected tab.
:read-only			The item is marked read only or non-editable. For example, a read only QLineEdit or a non-editable QComboBox.
:right				The item is positioned at the right. For example, a QTabBar that has its tabs positioned at the right.
:selected			The item is selected. For example, the selected tab in a QTabBar or the selected item in a QMenu.
:top				The item is positioned at the top. For example, a QTabBar that has its tabs positioned at the top.
:unchecked			The item is unchecked.
:vertical			The item has vertical orientation.
:window				The widget is a window (i.e top level widget)


List of Sub-Controls:
::add-line			The button to add a line of a QScrollBar.
::add-page			The region between the handle (slider) and the add-line of a QScrollBar.
::branch			The branch indicator of a QTreeView.
::chunk				The progress chunk of a QProgressBar.
::close-button		The close button of a QDockWidget or tabs of QTabBar
::corner			The corner between two scrollbars in a QAbstractScrollArea
::down-arrow		The down arrow of a QComboBox, QHeaderView (sort indicator), QScrollBar or QSpinBox.
::down-button		The down button of a QScrollBar or a QSpinBox.
::drop-down			The drop-down button of a QComboBox.
::float-button		The float button of a QDockWidget
::groove			The groove of a QSlider.
::indicator			The indicator of a QAbstractItemView, a QCheckBox, a QRadioButton, a checkable QMenu item or a checkable QGroupBox.
::handle			The handle (slider) of a QScrollBar, a QSplitter, or a QSlider.
::icon				The icon of a QAbstractItemView or a QMenu.
::item				An item of a QAbstractItemView, a QMenuBar, a QMenu, or a QStatusBar.
::left-arrow		The left arrow of a QScrollBar.
::left-corner		The left corner of a QTabWidget. For example, this control can be used to control position the left corner widget in a QTabWidget.
::menu-arrow		The arrow of a QToolButton with a menu.
::menu-button		The menu button of a QToolButton.
::menu-indicator 	The menu indicator of a QPushButton.
::right-arrow		The right arrow of a QMenu or a QScrollBar.
::pane				The pane (frame) of a QTabWidget.
::right-corner		The right corner of a QTabWidget. For example, this control can be used to control the position the right corner widget in a QTabWidget.
::scroller			The scroller of a QMenu or QTabBar.
::section			The section of a QHeaderView.
::separator			The separator of a QMenu or in a QMainWindow.
::sub-line			The button to subtract a line of a QScrollBar.
::sub-page			The region between the handle (slider) and the sub-line of a QScrollBar.
::tab				The tab of a QTabBar or QToolBox.
::tab-bar			The tab bar of a QTabWidget. This subcontrol exists only to control the position of the QTabBar inside the QTabWidget. To style the tabs using the ::tab subcontrol.
::tear				The tear indicator of a QTabBar.
::tearoff			The tear-off indicator of a QMenu.
::text				The text of a QAbstractItemView.
::title				The title of a QGroupBox or a QDockWidget.
::up-arrow			The up arrow of a QHeaderView (sort indicator), QScrollBar or a QSpinBox.
::up-button			The up button of a QSpinBox.

List of Colors (Qt namespace (ie. Qt::red)):
white
black
red
darkRed
green
darkGreen
blue
darkBlue
cyan
darkCyan
magenta
darkMagenta
yellow
darkYellow
gray
darkGray
lightGray
color0 (zero pixel value) (transparent, i.e. background)
color1 (non-zero pixel value) (opaque, i.e. foreground)


'''