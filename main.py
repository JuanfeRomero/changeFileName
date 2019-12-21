import os
import wx
import sys

class WrongFormatError(Exception):
    """The String input is not a correct extension format"""
    pass


class EmptyEntryError(Exception):
    """The entry was empty"""
    pass


def check_format_error(new_extension, specific_extension, new_name_checker):
    if new_name_checker.IsEnabled() and (new_extension == '' or not new_extension.startswith('.')):
        return True
    if not specific_extension == '' and not specific_extension.startswith('.'):
        print('noooo')
        return True
    else:
        return False


def replace_name(file_path, new_name, specific_extension, exclude_folder, only_folder):
    counter = 0
    file_path = file_path + '//'
    if new_name:
        if specific_extension:
            for filename in os.listdir(file_path):
                filename = filename.lower()
                filename_w_path, extension = os.path.splitext((file_path + filename))
                if specific_extension == extension:
                    dst = new_name + (str(counter)) + extension
                    src = file_path + filename
                    dst = file_path + dst
                    counter += 1
                    os.rename(src, dst)
        elif not specific_extension:
            if exclude_folder:
                for filename in os.listdir(file_path):
                    filename_w_path, extension = os.path.splitext((file_path + filename))
                    dst = new_name + (str(counter)) + extension
                    src = file_path + filename
                    if os.path.isdir(src):
                        continue
                    dst = file_path + dst
                    counter += 1
                    os.rename(src, dst)
            elif only_folder:
                for filename in os.listdir(file_path):
                    filename_w_path, extension = os.path.splitext((file_path + filename))
                    dst = new_name + (str(counter)) + extension
                    src = file_path + filename
                    if not os.path.isdir(src):
                        continue
                    dst = file_path + dst
                    counter += 1
                    os.rename(src, dst)


def replace_format(file_path, old_extension, new_extension):
    file_path = file_path + '//'
    for filename in os.listdir(file_path):
        filename = filename.lower()
        dst = filename.replace(old_extension, new_extension)
        src = file_path + filename
        if os.path.isdir(src):
            continue
        dst = file_path + dst
        os.rename(src, dst)


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Name/Format Changer')
        # Add can take up to 5 arguments:
        # window(the widget), proportion, flag, border and userData(not used often)
        # assigning the panel to the frame so it has the right color
        panel = wx.Panel(self)

        # adding a bmp icon for the window
        bmp_folder = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, (16, 16))
        bmp_title = wx.ArtProvider.GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_OTHER, (16, 16))
        bmp_sheet = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16))

        # Create the necessary widgets and putting them in boxes
        # icon and title
        title_icon = wx.StaticBitmap(panel, wx.ID_ANY, bmp_title)
        title = wx.StaticText(panel, wx.ID_ANY, 'Name Changer')
        # Path text with directory selector
        folder_icon = wx.StaticBitmap(panel, wx.ID_ANY, bmp_folder)
        folder_text = wx.StaticText(panel, wx.ID_ANY, 'Select Folder to change')
        self.folder_selector = wx.DirPickerCtrl(panel, wx.ID_ANY, "Select")

        # New Name text and textbox with specific extension
        new_name_icon = wx.StaticBitmap(panel, wx.ID_ANY, bmp_sheet)
        new_name_text = wx.StaticText(panel, wx.ID_ANY, 'New Name')
        self.new_name_text_box = wx.TextCtrl(panel, wx.ID_ANY, '')
        specific_extension_text = wx.StaticText(panel, wx.ID_ANY, 'Change only this extension')
        self.specific_extension = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.exclude_folders_button = wx.CheckBox(panel, wx.ID_ANY)
        self.exclude_folders_button.SetLabelText('Exclude Folders')
        self.Bind(wx.EVT_CHECKBOX, self.except_folders_checked, self.exclude_folders_button)
        self.only_folders_button = wx.CheckBox(panel, wx.ID_ANY)
        self.Bind(wx.EVT_CHECKBOX, self.only_folders_checked, self.only_folders_button)
        self.only_folders_button.SetLabelText('Only Folders')

        # extensions and text boxes
        new_extension = wx.StaticText(panel, wx.ID_ANY, f'To :')
        self.new_extension_text_box = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.new_extension_text_box.Disable()
        old_extension = wx.StaticText(panel, wx.ID_ANY, f'convert')
        self.old_extension_text_box = wx.TextCtrl(panel, wx.ID_ANY, '')
        self.Bind(wx.EVT_TEXT, self.on_dot_start, self.old_extension_text_box)

        # execute and cancel buttons
        ok_btn = wx.Button(panel, wx.ID_ANY, 'Convert')
        cancel_btn = wx.Button(panel, wx.ID_ANY, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.on_ok, ok_btn)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_btn)

        # sizers
        top_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel)
        title_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel)
        folder_path_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel)
        new_name_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel, 'Change File Name')
        extensions_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel, 'Change Formats')
        buttons_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel)
        checkbox_sizer = wx.BoxSizer(wx.VERTICAL)

        title_sizer.Add(title_icon, 0, wx.ALL, 5)
        title_sizer.Add(title, 0, wx.ALL, 5)

        folder_path_sizer.Add(folder_icon, 0, wx.ALL, 5)
        folder_path_sizer.Add(folder_text, 0, wx.ALL, 5)
        folder_path_sizer.Add(self.folder_selector, 1, wx.ALL|wx.EXPAND, 5)

        new_name_sizer.Add(new_name_icon, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        new_name_sizer.Add(new_name_text, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        new_name_sizer.Add(self.new_name_text_box, 1, wx.ALL|wx.SHAPED|wx.ALIGN_CENTER_VERTICAL, 5)
        new_name_sizer.Add(specific_extension_text, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        new_name_sizer.Add(self.specific_extension, 1, wx.ALL|wx.SHAPED|wx.ALIGN_CENTER_VERTICAL, 5)
        checkbox_sizer.Add(self.exclude_folders_button, 0, wx.ALL, 5)
        checkbox_sizer.Add(self.only_folders_button, 0, wx.ALL, 5)
        new_name_sizer.Add(checkbox_sizer, 0, wx.ALL|wx.EXPAND, 5)

        extensions_sizer.Add(old_extension, 0, wx.ALL, 5)
        extensions_sizer.Add(self.old_extension_text_box, 1, wx.ALL, 5)
        extensions_sizer.Add(new_extension, 0, wx.ALL, 5)
        extensions_sizer.Add(self.new_extension_text_box, 1, wx.ALL, 5)

        buttons_sizer.Add(ok_btn, 0, wx.ALL, 5)
        buttons_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(folder_path_sizer, 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(new_name_sizer, 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(extensions_sizer, 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(wx.StaticLine(panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(buttons_sizer, 0, wx.ALL|wx.CENTER, 5)

        panel.SetSizer(top_sizer)
        top_sizer.Fit(self)
        self.Show()

    def on_ok(self, event):
        folder_selector = self.folder_selector.GetPath()
        new_name = self.new_name_text_box.GetValue()
        new_name_checker = self.new_extension_text_box
        new_extension = self.new_extension_text_box.GetValue()
        old_extension = self.old_extension_text_box.GetValue()
        specific_extension = self.specific_extension.GetValue()
        exclude_folder = self.exclude_folders_button.IsChecked()
        only_folder = self.only_folders_button.IsChecked()

        try:
            if not os.path.isdir(folder_selector):
                raise FileNotFoundError
            if new_name == '' and old_extension == '':
                raise EmptyEntryError
            else:
                replace_name(folder_selector, new_name, specific_extension, exclude_folder, only_folder)
                if check_format_error(new_extension, specific_extension, new_name_checker):
                    raise WrongFormatError
                replace_format(folder_selector, old_extension, new_extension)
        except FileNotFoundError:
            file_path_error = wx.MessageDialog(self, "Error, directory unknown", "Error!", wx.OK)
            file_path_error.ShowModal()
        except WrongFormatError:
            wrong_format_error = wx.MessageDialog(self, "Error, incorrect extension format", "Error!", wx.OK)
            wrong_format_error.ShowModal()
        except EmptyEntryError:
            empty_entry_error = wx.MessageDialog(self, "Error, enter a name or a correct extension to change")
            empty_entry_error.ShowModal()
        else:
            success_message = wx.MessageDialog(self, "Success!", "Finished", wx.OK)
            success_message.ShowModal()

    def on_cancel(self, event):
        sys.exit()

    def on_dot_start(self, event):
        self.new_extension_text_box.Disable()
        check_if_dot = self.old_extension_text_box.GetValue()
        if check_if_dot.startswith('.'):
            self.new_extension_text_box.Enable()
        if not check_if_dot.startswith('.'):
            self.new_extension_text_box.SetLabel('')

    def except_folders_checked(self, event):
        only_folder_checkbox = self.only_folders_button
        only_folder_checkbox.SetValue(False)
        specific_extension_text = self.specific_extension
        specific_extension_text.Enable()

    def only_folders_checked(self, event):
        except_folder_checkbox = self.exclude_folders_button
        except_folder_checkbox.SetValue(False)
        specific_extension_text = self.specific_extension
        specific_extension_text.SetLabel('')
        specific_extension_text.Disable()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
