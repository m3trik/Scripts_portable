import os.path



# ------------------------------------------------
#' MainWindow StyleSheet'
# ------------------------------------------------




css='''




QMainWindow {
	background-color: rgba(127,127,127,2); 
	color: rgb(225, 225, 225);
	};

QGroupBox {
	background-color: rgba(100,100,100,80);
	color: rgb(225, 225, 225);
	border: 3px solid black;
	};

QCheckBox::indicator:checked {
	background-color: rgb(140,000,140);
	color: rgb(0, 0, 0);
	};

QToolTip {
	background-color:rgb(225,225,225);
	color:rgb(0,140,0);
	border: 1px solid black;
	};




'''









#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------