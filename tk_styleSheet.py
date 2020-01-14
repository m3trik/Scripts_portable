import os.path






# ------------------------------------------------
#' MainWindow StyleSheet'
# ------------------------------------------------
class StyleSheet():
	'''
	
	'''
	COLOR_DARK 		= 'rgb(0,0,0)'
	COLOR_MEDIUM 	= 'rgb(100,100,100)'
	COLOR_MEDLIGHT 	= 'rgb(125,125,125)'
	COLOR_LIGHT 	= 'rgb(225,225,225)'
	COLOR_ACCENT 	= 'rgba(82,133,166,225)'
	COLOR_TEXT1		= 'white'
	COLOR_TEXT2		= 'black'


	QWidget='''
		QWidget::item:selected {
			background: '''+COLOR_ACCENT+''';
		}

		QWidget#mainWindow {
			background: transparent;
		}'''

	QPushButton='''
		QPushButton {
			border-style: outset;
			border-radius: 1px;
			border: 1px solid black;
			padding: 0px;
			background-color: '''+COLOR_MEDIUM+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton::checked {
			border: 1px solid black;
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT2+''';
		}

		QPushButton::hover {   
			border: 1px solid black;
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton::unchecked::hover {
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton::checked::hover {
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT2+''';
		}

		QPushButton::pressed {   
			border: 1px solid black;
			background-color: '''+COLOR_MEDLIGHT+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton:flat {
			border: none; /* no border for a flat push button */
		}

		QPushButton:default {
			border-color: navy; /* make the default button prominent */
		}'''

	submenu='''
		QPushButton {
			border-style: outset;
			border-radius: 1px;
			border: 1px solid black;
			padding: 0px;
			background-color: rgb(50,50,50);
			color: grey;
		}

		QPushButton::checked {
			border: 1px solid black;
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT2+''';
		}

		QPushButton::hover {   
			border: 1px solid black;
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton::unchecked::hover {
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton::checked::hover {
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT2+''';
		}

		QPushButton::pressed {   
			border: 1px solid black;
			background-color: '''+COLOR_MEDLIGHT+''';
			color: '''+COLOR_TEXT1+''';
		}

		QPushButton:flat {
			border: none; /* no border for a flat push button */
		}

		QPushButton:default {
			border-color: navy; /* make the default button prominent */
		}'''

	QAbstractButton='''
		QAbstractButton:hover {
			background: '''+COLOR_MEDIUM+''';
		}

		QAbstractButton:pressed {
			background: '''+COLOR_MEDLIGHT+''';
		}'''

	QComboBox='''
		QComboBox {
			background: '''+COLOR_MEDIUM+''';
			color: '''+COLOR_TEXT1+''';
			border: 1px solid black;
			padding: 1px 18px 1px 3px;
			/* border-radius: 1px; */
			/* min-width: 0em; */
		}

		QComboBox::hover {
			background: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
			border: 1px solid black;
		}

		QComboBox::open {
			background: '''+COLOR_MEDIUM+''';
			color: '''+COLOR_TEXT1+''';
			border: 1px solid black;
			selection-background-color: '''+COLOR_ACCENT+''';
			selection-color: '''+COLOR_TEXT2+''';
		}

		QComboBox:on { /* shift the text when the popup opens */
			padding-top: 3px;
			padding-left: 4px;
		}

		QComboBox::down-arrow {
			width: 0px;
			height: 0px;
			border: transparent;
			background: '''+COLOR_MEDIUM+''';
		}

		QComboBox::drop-down {
			border: transparent;
			background: '''+COLOR_MEDIUM+''';
			subcontrol-origin: padding;
			subcontrol-position: top right;
			width: 0px;

			border-left-width: 1px;
			border-left-color: '''+COLOR_TEXT2+''';
			border-left-style: solid; /* just a single line */
			border-top-right-radius: 1px; /* same radius as the QComboBox */
			border-bottom-right-radius: 1px;
		}'''

	QSpinBox='''
		QSpinBox {
		background: '''+COLOR_MEDIUM+''';
		color: '''+COLOR_TEXT1+''';
		border: 1px solid black;
		}

		QSpinBox::hover {
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
			border: 1px solid black;
		}'''

	QDoubleSpinBox='''
		QDoubleSpinBox {
		background: '''+COLOR_MEDIUM+''';
		color: '''+COLOR_TEXT1+''';
		border: 1px solid black;
		}

		QDoubleSpinBox::hover {
			background-color: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
			border: 1px solid black;
		}'''

	QAbstractSpinBox='''
		QScrollBar:left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow, QScrollBar::down-arrow {
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			width: 3px;
			height: 3px;
		}

		QAbstractSpinBox::up-arrow, QAbstractSpinBox::down-arrow {
			width: 3px;
			height: 3px;
			border: 1px solid '''+COLOR_MEDLIGHT+''';
		}

		QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			background: '''+COLOR_MEDIUM+''';
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
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			background: none;
		}

		QRadioButton::indicator:unchecked:hover, QCheckBox::indicator:unchecked:hover {
			border: 1px solid '''+COLOR_MEDIUM+''';
		}

		QRadioButton::indicator::checked, QCheckBox::indicator::checked {
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			background: '''+COLOR_MEDLIGHT+''';
		}

		QRadioButton::indicator:checked:hover, QCheckBox::indicator:checked:hover {
			border: 1px solid '''+COLOR_MEDIUM+''';
			background: '''+COLOR_MEDIUM+''';
		}'''

	QAbstractItemView='''
		QAbstractItemView {
			show-decoration-selected: 1;
			selection-background-color: '''+COLOR_ACCENT+''';
			selection-color: '''+COLOR_MEDIUM+''';
			alternate-background-color: '''+COLOR_MEDIUM+''';
		}'''

	QHeaderView='''
		QHeaderView {
			border: 1px solid '''+COLOR_MEDLIGHT+''';
		}

		QHeaderView::section {
			background: '''+COLOR_DARK+''';
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			padding: 1px;
		}

		QHeaderView::section:selected, QHeaderView::section::checked {
			background: '''+COLOR_MEDIUM+''';
		}'''

	QTableView='''
		QTableView {
			gridline-color: '''+COLOR_MEDLIGHT+''';
		}'''

	QLineEdit='''
		QLineEdit {
			border: 1px solid black;
			border-radius: 10px;
			padding: 0 8px;
			background: '''+COLOR_MEDIUM+''';
			color: '''+COLOR_TEXT1+''';
			selection-background-color: '''+COLOR_ACCENT+''';
			selection-color: '''+COLOR_TEXT1+''';
		}

		QLineEdit::disabled {
			color: '''+COLOR_MEDIUM+''';
		}

		QLineEdit::enabled {
			color: '''+COLOR_TEXT1+''';
		}

		QLineEdit:read-only {
			background: '''+COLOR_MEDIUM+''';
		}'''

	QTextEdit='''
		QTextEdit {
			background-color: '''+COLOR_MEDIUM+''';
			color: '''+COLOR_TEXT1+''';
			selection-background-color: '''+COLOR_ACCENT+''';
			selection-color: '''+COLOR_TEXT1+''';
			background-attachment: fixed; /* fixed, scroll */
		}'''

	QListView='''
		QListView {
			background-color: '''+COLOR_MEDIUM+''';
			color: '''+COLOR_TEXT1+''';
			alternate-background-color: '''+COLOR_MEDIUM+''';
			background-attachment: fixed; /* fixed, scroll */
		}

		QListView::item:alternate {
			background: '''+COLOR_MEDIUM+''';
		}

		QListView::item:selected {
			border: 1px solid '''+COLOR_ACCENT+''';
		}

		QListView::item:selected:!active {
			background: '''+COLOR_MEDIUM+''';
			color: grey;
		}

		QListView::item:selected:active {
			background: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT2+''';
		}

		QListView::item:hover {
			background: '''+COLOR_ACCENT+''';
			color: '''+COLOR_TEXT1+''';
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
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			background: '''+COLOR_MEDIUM+''';
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
			background: '''+COLOR_ACCENT+''';
		}

		QSlider::sub-page:vertical, QSlider::add-page:horizontal {
			background: '''+COLOR_MEDIUM+''';
		}'''

	QScrollBar='''
		QScrollBar {
			border: 1px solid '''+COLOR_MEDLIGHT+''';
			background: '''+COLOR_DARK+''';
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
			background: '''+COLOR_MEDIUM+''';
			border: 1px solid '''+COLOR_MEDLIGHT+''';
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
			background:'''+COLOR_MEDIUM+''';
			border: 1px solid '''+COLOR_MEDLIGHT+''';
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
			margin-top: 4px; /* leave space at the top for the title */
			background-color: rgbs(127,127,127,2);
			color: '''+COLOR_TEXT2+''';
			border: 1px '''+COLOR_MEDLIGHT+''';
			border-radius: 5px;
		}

		QGroupBox::title {
			top: -7px;
			left: 7px;

    		subcontrol-position: top left; /* position at the top center */
			background-color: transparent;
			color: '''+COLOR_MEDLIGHT+''';
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
			background: '''+COLOR_MEDIUM+''';
		}'''

	QMenu='''
		QMenu::separator {
			background: '''+COLOR_MEDIUM+''';
		}'''

	QLabel='''
		QLabel {
			border: none;
		}'''

	QToolTip='''
		QToolTip {
			background-color: transparent;
			color: '''+COLOR_TEXT1+''';
			border: 0px solid transparent;
		}'''

	QProgressBar='''
		QProgressBar {
			border: 0px solid black;
			border-radius: 5px;
			text-align: center;
		}

		QProgressBar::chunk {
			width: 1px;
			margin: 0px;
			background-color: '''+COLOR_ACCENT+''';
		}'''









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


'''
#qt styleSheet reference
http://doc.qt.io/qt-5/stylesheet-reference.html#qtabbar-widget

# commenting:
	/* multi-line */

# setting property:
	qApp.setStyleSheet("QLineEdit#name[prop=true] {background-color:transparent;}") #does't effect the lineEdit with objectName 'name' if that buttons property 'styleSheet' is false (c++ lowercase). 
	self.setProperty('prop', True) #set the widget property.

# gradient:
	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #E0E0E0, stop: 1 #FFFFFF);

# multiple widgets:
	QComboBox:!editable, QComboBox::drop-down:editable { ... }



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

# min-width: 80px;

# QComboBox:editable {
# 	background: '''+COLOR_MEDIUM+''';
# }

# QComboBox:!editable, QComboBox::drop-down:editable {
# 	background: '''+COLOR_MEDIUM+''';
# }

# /* QComboBox gets the "on" state when the popup is open */
# QComboBox:!editable:on, QComboBox::drop-down:editable:on {
# 	background: '''+COLOR_MEDIUM+''';
# }
		
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




