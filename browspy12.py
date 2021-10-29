from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		# Full Screen
		self.showMaximized()

		# Tabs 
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.setCentralWidget(self.tabs)

		# creating a status bar
		self.status = QStatusBar()
		self.setStatusBar(self.status)

		# creating a tool bar for navigation
		navtb = QToolBar("Navigation")
		self.addToolBar(navtb)

		# Back
		back_btn = QAction("←", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		# Forward
		next_btn = QAction("→", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		# Reload
		reload_btn = QAction("⟳", self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		# Home
		home_btn = QAction("🏠", self)
		home_btn.setStatusTip("Go home")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		# YouTube
		youtube_btn = QAction("📺", self)
		youtube_btn.setStatusTip("Go YouTube")
		youtube_btn.triggered.connect(self.navigate_youtube)
		navtb.addAction(youtube_btn)

		# Meet
		meet_btn = QAction("Meet", self)
		meet_btn.setStatusTip("Go Google Meet")
		meet_btn.triggered.connect(self.navigate_meet)
		navtb.addAction(meet_btn)        

		# adding a separator
		navtb.addSeparator()

		# URL Bar
		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlbar)

		# similarly adding stop action
		# stop_btn = QAction("Stop", self)
		# stop_btn.setStatusTip("Stop loading current page")
		# stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		# navtb.addAction(stop_btn)

		# creating first tab
		self.add_new_tab(QUrl('https://duckduckgo.com/'), 'Homepage')
		self.show()
		self.setWindowTitle("BrowsPy v1.1")

	# method for adding new tab
	def add_new_tab(self, qurl = None, label ="Blank"):
		if qurl is None:
			qurl = QUrl('https://duckduckgo.com/')
		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)
		browser.urlChanged.connect(lambda qurl, browser = browser:
								self.update_urlbar(qurl, browser))
		browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.tabs.setTabText(i, browser.page().title()))

	# when double clicked is pressed on tabs
	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()

	# when tab is changed
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.update_urlbar(qurl, self.tabs.currentWidget())
		self.update_title(self.tabs.currentWidget())

	# when tab is closed
	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)

	# method for updating the title
	def update_title(self, browser):
		if browser != self.tabs.currentWidget():
			return
		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle("% s" % title)

	# Home
	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com/"))

	# YouTube
	def navigate_youtube(self):
		self.tabs.currentWidget().setUrl(QUrl("https://youtube.com"))

	# Meet
	def navigate_meet(self):
		import meet

	# method for navigate to url
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)

	# method to update the url
	def update_urlbar(self, q, browser = None):
		if browser != self.tabs.currentWidget():
			return
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

app = QApplication(sys.argv)
app.setApplicationName("BrowsPy v1.2")
window = MainWindow()
app.exec_()