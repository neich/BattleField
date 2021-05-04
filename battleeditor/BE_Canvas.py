import wx
import Battles.Utils.Geometry as Geometry
import BE_Dialogs.BE_BackgroundHelperDlg



""" Canvas:

    Due the aim of this project is not to create a full and flexible CAD system, there are some restrictions on canvas, related too to the Battles simulation viewport system
    The main fact is that the viewport (and window, in factor 1:1) is squared, ever. This avoids the main drawbacks of designing a flexible viewport system (aspects, resizes, ...)
    The second fact is that the window/viewport have 1000x1000 as base size. Note that the main window is resized to set the canvas at this size
    Then, if user changes the viewport size, a simple screen to user coordinates (and viceversa) has been implemented, considering that the origin is ever at the same
    place (top-right corner), so no pan action is available. Therefore, the coordinates mapping just scales the given point by factor between current viewport size
    and base viewport size (1000)

    Clearly, as a big TODO, more functionality should be added to this system
"""



class BE_Canvas(wx.Panel):

    """ Panel used as canvas to draw the canvas objects


        Attributes:
            eventHandler: Reference to the event handler to draw the objects that are currently creating
            document: Reference to the document to draw the canvas objects
            windowsize: window size (from default settings). Fixed at 1000x1000
            viewportsize: viewport size (from default settings). Both are used to map the coordinates inside the fixes window size of (1000x1000)
            backgroundhelper: background image to help the drawing
    """

    def __init__(self, parent, pos, size, style, eventhandler, document):
        wx.Panel.__init__(self, parent, pos = pos, size = size, style = style)

        self.__eventHandler = eventhandler
        self.__document = document

        self.__windowSize = [1000,1000]
        self.__windowSize[0] = self.__document.GetDefaultSettings().game.windowSize
        self.__windowSize[1] = self.__document.GetDefaultSettings().game.windowSize

        # Set the viewport size. See at header for more info
        self.__viewportSize = [1000,1000]
        self.__viewportSize[0] = self.__document.GetDefaultSettings().game.viewportSize
        self.__viewportSize[1] = self.__document.GetDefaultSettings().game.viewportSize

        self.__backgroundHelperDialog = None            # Just used to keep a referece to the backgound helper dialog and configure its bindings
        self.__backgroundHelper = None

        # Allow to set the background helper image
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)



    def OnEraseBackground(self, evt):
            """
            Add a picture to the background
            """
            # yanked from ColourDB.py
            dc = evt.GetDC()

            if not dc:
                dc = wx.ClientDC(self)
                rect = self.GetUpdateRegion().GetBox()
                dc.SetClippingRect(rect)
            dc.Clear()

            if (self.__backgroundHelper):
                # Fit the background image to current mapping coordinates, but only for it, due we are changing the canvas internal mapping (its more easy), and this
                # should not affect the other drawing tools
                p = self.UserToScreenCoord(1, 1)
                dc.SetUserScale(p.x, p.x)

                bmp = wx.Bitmap(self.__backgroundHelper)
                dc.DrawBitmap(bmp, 0, 0)

                # Restore the original mapping coordinates
                dc.SetUserScale(1, 1)



    def OnPaint(self, event):

        w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        #dc.Clear()


        # Draw all canvas objects (already created)
        self.__document.Draw(dc, self)



        # Draw the action objects at last, to avoid be overdrawed by static items
        self.__eventHandler.DrawAction(dc)

        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))


    def SetUserViewSize(self, w, h):
        self.__viewportSize[0] = w
        self.__viewportSize[1] = h



    def ScreenToUserCoord(self, x, y):
        # See at header for more information

        scale = [float(self.__viewportSize[0]) / float(self.__windowSize[0]), float(self.__viewportSize[0]) / float(self.__windowSize[0])]
        return Geometry.Point2D(x * scale[0], y * scale[1])


    def UserToScreenCoord(self, x, y):
        # See at header for more information

        scale = [float(self.__windowSize[0]) / float(self.__viewportSize[0]), float(self.__windowSize[0]) / float(self.__viewportSize[0])]
        return Geometry.Point2D(x * scale[0], y * scale[1])


    def ScreenToUserValue(self, x):
        # WARNING: This function only should be used if window and viewport are squared. Otherwise, the window/viewport factor should be considered
        p = self.ScreenToUserCoord(x, x)
        return p.x

    def UserToScreenValue(self, x):
        # WARNING: This function only should be used if window and viewport are squared. Otherwise, the window/viewport factor should be considered
        p = self.UserToScreenCoord(x, x)
        return p.x


    def SetBackgroundHelper(self, parent):
        # Sets the background helper

        self.__backgroundHelperDialog = BE_Dialogs.BE_BackgroundHelperDlg.BE_BackgroundHelperDlg(parent)

        if (self.__backgroundHelper):
            self.__backgroundHelperDialog.checkActive.SetValue(True)
            self.__backgroundHelperDialog.textFilename.SetValue(self.__backgroundHelper)
        else:
            self.__backgroundHelperDialog.checkActive.SetValue(False)

        self.__backgroundHelperDialog.butFileDlg.Bind(wx.EVT_BUTTON, self.OnSelectBackgroundImage)


        if (self.__backgroundHelperDialog.ShowModal() == wx.ID_OK):

            if (self.__backgroundHelperDialog.checkActive.GetValue() == True):
                self.__backgroundHelper = self.__backgroundHelperDialog.textFilename.GetValue()
            else:
                self.__backgroundHelper = None

        self.__backgroundHelperDialog.Destroy()
        self.__backgroundHelperDialog = None


    def OnSelectBackgroundImage(self, event):

        if (not self.__backgroundHelperDialog):
            return

        dlg = wx.FileDialog(None, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

        if (dlg.ShowModal() == wx.ID_OK):
            self.__backgroundHelperDialog.textFilename.SetValue(dlg.GetPath())

        dlg.Destroy()
