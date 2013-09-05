"""
http://sourceforge.net/apps/mediawiki/pyhook/index.php?title=PyHook_Tutorial
http://www.kbdedit.com/manual/low_level_vk_list.html
"""
import Case00_commonJobs

import pythoncom, pyHook
import win32gui
import win32api, win32con
from win32clipboard import *

import time
import re

def OnKeyboardEvent(event):
    if (event.KeyID == 118 or event.KeyID == 119 or event.KeyID == 120 or event.KeyID == 121 or event.KeyID == 122 or event.KeyID == 123):
        pasteFlag = 0
##        print('MessageName:',event.MessageName)
##        print('Message:',event.Message)
##        print('Time:',event.Time)
##        print('Window:',event.Window)
##        print('WindowName:',event.WindowName)
##        print('Ascii:', event.Ascii, chr(event.Ascii))
##        print('Key:', event.Key)
##        print('KeyID:', event.KeyID)
##        print('ScanCode:', event.ScanCode)
##        print('Extended:', event.Extended)
##        print('Injected:', event.Injected)
##        print('Alt', event.Alt)
##        print('Transition', event.Transition)
##        print('---')
    # return True to pass the event to other handlers

##    hwnd = win32gui.GetForegroundWindow()
##    print(win32gui.GetWindowText(hwnd))
        if event.KeyID == 118 or event.KeyID == 119 or event.KeyID == 120 or event.KeyID == 121 or event.KeyID == 122:  #F7 ... F11
    ##        win32api.keybd_event(0x46, 0, ) # F
    ##        win32api.keybd_event(0x52, 0, ) # R
    ##        win32api.keybd_event(0x0D, 0, ) # R

            win32api.keybd_event(win32con.VK_CONTROL,0x9d,0 , 0);
            win32api.keybd_event(win32api.VkKeyScan('C'),0x9e,0 , 0);
            win32api.keybd_event(win32api.VkKeyScan('C'),0x9e, win32con.KEYEVENTF_KEYUP,0);
            win32api.keybd_event(win32con.VK_CONTROL,0x9d,win32con.KEYEVENTF_KEYUP,0);
    #----------------------------
            time.sleep(0.01)
            OpenClipboard()
            value = GetClipboardData()
            #========
            if event.KeyID == 118: #F7 key end with _000
                foundKey = Case00_commonJobs.findCorrespondentKey(dataDict, value, labelLoweredStandardedDict)
                outputstring=re.sub('_000\d','_0000',foundKey)
                pasteFlag = 1
            elif event.KeyID == 119: #F8 keep the key
                foundKey = Case00_commonJobs.findCorrespondentKey(dataDict, value, labelLoweredStandardedDict)
                outputstring = foundKey
                pasteFlag = 1
            elif event.KeyID == 121: #F10 keep the key
                foundKey = Case00_commonJobs.findCorrespondentKey(dataDict, value, labelLoweredStandardedDict)
                foundKey = re.sub('_000\d','_0000',foundKey)
                outputstring = '<posui:showLabel key="'+foundKey+'" />'
                pasteFlag = 1
            elif event.KeyID == 122: #F11 header value with tooltip ; input value MUST start with > character
                if re.search(r'^>', value):
                    value = value.lstrip(">")
                    foundKey = Case00_commonJobs.findCorrespondentKey(dataDict, value, labelLoweredStandardedDict)
                    toolTip = re.sub('_000\d','_0000',foundKey)
                    outputstring = ' onmouseover="tooltipOn(\'<posui:showLabel key="'+toolTip+'" />\');" onmouseout="tooltipOff();"><posui:showLabel key="'+foundKey+'" />'
                    pasteFlag = 1
                else:
                    outputstring = value
                    pasteFlag = 0
                
                
            #========
            SetClipboardData(CF_UNICODETEXT, outputstring)
            CloseClipboard()
    #----------------------------
            if pasteFlag == 1:
                win32api.keybd_event(win32con.VK_CONTROL,0x9d,0 , 0);
                win32api.keybd_event(win32api.VkKeyScan('V'),0x9e,0 , 0);
                win32api.keybd_event(win32api.VkKeyScan('V'),0x9e, win32con.KEYEVENTF_KEYUP,0);
                win32api.keybd_event(win32con.VK_CONTROL,0x9d,win32con.KEYEVENTF_KEYUP,0);

        elif event.KeyID == 123:  #F12
            hm.UnhookKeyboard()
    
    return True

##filename = r'C:\Documents and Settings\SoftVnn Member\My Documents\Dropbox\backUp\130401_MultiLanguageChanging\Tools\label_ko.properties'
filename = r'label_ko.properties'

dataDict = Case00_commonJobs.addDataToDict(filename, 1)
labelLoweredStandardedDict = Case00_commonJobs.addDataToDict(filename,1,1)

    
# create a hook manager
hm = pyHook.HookManager()
##hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()

