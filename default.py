import sys
import os
import subprocess
import xbmc
import xbmcaddon
import xbmcgui
import shutil

'''

This software is provided "as is" and has absolutely NO WARRANTY.
Please use at your own risk!

This is an eraly dev release: 
the following features are known NOT to work at times
and may overwrite your files!
- running the script MIGHT NOT work correctly - I could not test it in linux and strawberry perl is causing problems in my windows machine, but the script SHOULD be loaded correctly
- editing configuration WILL NOT save correctly and might overwrite sorttv.conf with a blank file
- import configuration MIGHT NOT save correctly and might overwrite sorttv.conf with a blank file

stable release TODO:
- fix edit/import config file
- fill credits.txt
- change the back.png

whishlist TODO:
- find better solution for editing config file (without ControlList)
- scheduling
- add ability to run/configure script through smb share
- add ability to install perl and related perl extensions (Windows only)
- skinning

'''

__scriptid__   = "script.sorttv"
__settings__   = xbmcaddon.Addon(id=__scriptid__)
__language__   = __settings__.getLocalizedString
__version__    = __settings__.getAddonInfo('version')
__cwd__        = __settings__.getAddonInfo('path')
__scriptname__ = "SortTV"
__author__     = "check CREDITS.txt for a full list"

#get actioncodes from keymap.xml
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7

class RunSortTV(xbmcgui.Window):
    def __init__(self):
        screenx = self.getWidth()
        screeny = self.getHeight()
        offsetx = screenx / 20
        offsety = screeny / 20
        buttonwidth =  screenx / 5
        buttonheight = screeny / 20
        separator = buttonwidth / 5

        self.strActionInfo = xbmcgui.ControlLabel(offsetx, offsety, screenx-offsetx*2, buttonheight, '', 'font14', '0xFFFFFFFF')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel('Welcome to SortTV')

        self.strActionInfo = xbmcgui.ControlLabel(offsetx, offsety+buttonheight*2, screenx-offsetx*2, buttonheight, '', 'font13', '0xAAFFFFFF')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel('Select Run SortTV to run the script or Configure to set the options | Press ESC or Back on your remote to exit')

        self.button0 = xbmcgui.ControlButton(offsetx, offsety+buttonheight*4, buttonwidth, buttonheight, "Run SortTV")
        self.addControl(self.button0)
        self.setFocus(self.button0)

        self.button1 = xbmcgui.ControlButton(offsetx+buttonwidth+separator, offsety+buttonheight*4, buttonwidth, buttonheight, "Configure")
        self.addControl(self.button1)
    
	self.button2 = xbmcgui.ControlButton(offsetx+buttonwidth*2+separator*2, offsety+buttonheight*4, buttonwidth, buttonheight, "Import Configuration")
        self.addControl(self.button2)

        self.button3 = xbmcgui.ControlButton(screenx-buttonwidth-offsetx, offsety+buttonheight*4, buttonwidth, buttonheight, "About")
        self.addControl(self.button3)

        self.button0.controlRight(self.button1)
        self.button1.controlLeft(self.button0)
	self.button1.controlRight(self.button2)
        self.button2.controlLeft(self.button1)
        self.button2.controlRight(self.button3)
        self.button3.controlLeft(self.button2)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()

    def onControl(self, control):
        if control == self.button0:
            self.list = xbmcgui.ControlList(0, offsety+buttonheight*6, screenx, screeny-(offsety+buttonheight*6) )
            self.addControl(self.list)
            args = ['perl',xbmc.translatePath('special://home/addons/script.sorttv/sorttv.pl')]
            dmp = subprocess.Popen(args, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.list.addItem('### SortTV running: ###')
            while True:
                if dmp.poll() is not None:
                    break
                (stdout, stderr) = dmp.communicate()
                self.list.addItem("Script output: " + stdout)
                self.list.addItem("Error messages: " + stderr)
                time.sleep(5)
            self.list.addItem('### SortTV done! ###')
            xbmc.executebuiltin('XBMC.UpdateLibrary(video)')
        if control == self.button1:
            self.configure()
	if control == self.button2:
            self.importconfig()
        if control == self.button3:
            cname = 'special://home/addons/script.sorttv/CREDITS.txt'
            credits = open(cname, "r")
            xbmcgui.Dialog().ok("Credits", credits.read())

    def message(self, message):
        dialog = xbmcgui.Dialog()
        dialog.ok("SortTV", message)

    def configure(self):
        fname = 'special://home/addons/script.sorttv/sorttv.conf'
        if os.path.isfile(fname) == False:
            self.message('Configuration file not present. Please ensure the file sorttv.conf is in your addon directory.')
        else:
            popup = DoConfig()
            popup .doModal()
            del popup
    
    def importconfig(self):
	d = xbmcgui.Dialog()
        src = d.browse(1, 'Select folder', 'files', '.conf')
        dst = 'special://home/addons/script.sorttv'
        try:
            shutil.copy2(xbmc.translatePath(src), xbmc.translatePath(dst))
            self.message('Configuration imported!')
        except:
            self.message('Unexpected error importing configuration.')

class DoConfig(xbmcgui.Window):
    def __init__(self):
        screenx = self.getWidth()
        screeny = self.getHeight()
        offsetx = screenx / 20
        offsety = screeny / 20
        buttonwidth =  screenx / 5
        buttonheight = screeny / 20
        separator = buttonwidth / 5
        
        self.strActionInfo = xbmcgui.ControlLabel(offsetx, offsety, screenx-offsetx*2, buttonheight, '', 'font14', '0xFFBBFFBB')
        self.addControl(self.strActionInfo)
        self.strActionInfo.setLabel('Push BACK to go back (and save), DOWN/UP to scroll, ENTER to modify')
        fname = 'special://home/addons/script.sorttv/sorttv.conf'
        f = open(fname, "r")
        ls = f.read().split("\n")
        f.close()
        self.list = xbmcgui.ControlList(0, offsety+buttonheight*2, screenx-offsetx*2, screeny-offsety+buttonheight*2, buttonFocusTexture=xbmc.translatePath('special://home/addons/script.sorttv/img/back.png') )
        self.addControl(self.list)
        for line in ls:
            self.list.addItem(line)
        self.setFocus(self.list)
#        self.textbox = xbmcgui.ControlTextBox(100, 250, 300, 300, textColor='0xFFFFFFFF')
#        self.addControl(self.textbox)
#        for line in ls:
#            self.textbox.setText('test')
#        self.setFocus(self.textbox)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.goodbye()

    def goodbye(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno("Save", "Do you want to save the configuration?"):
#            indexes = range(self.list.size())
#            config = ""
#            for i in indexes:
#                config = "\n".join(self.list.getListItem(i).getLabel())
            config = "\n".join([self.list.getListItem(i).getLabel() for i in xrange(self.list.size())])
            fname = xbmc.translatePath('special://home/addons/script.sorttv/sorttv.conf')
            w = open(fname, 'r+')
            w.write(config)
            w.close()
            self.close()
        else:
            self.close()

    def onControl(self, control):
        if control == self.list:
            item = self.list.getSelectedItem().getLabel()
            keyboard = xbmc.Keyboard(item)
            keyboard.doModal()
            if keyboard.isConfirmed():
                self.list.getSelectedItem().setLabel(keyboard.getText())
#        if control == self.textbox:
#            self.textbox.scroll(0)
#            item = self.textbox.getSelectedItem().getLabel()
#            keyboard = xbmc.Keyboard(item)
#            keyboard.doModal()
#            if keyboard.isConfirmed():
#                self.textbox.getSelectedItem().setLabel(keyboard.getText())

    def message(self, message):
        dialog = xbmcgui.Dialog()
        dialog.ok("SortTV", message)


sorttvdisplay = RunSortTV()
sorttvdisplay .doModal()
del sorttvdisplay