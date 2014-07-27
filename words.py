#!/usr/bin/env python

import sys, os, string, oauth2client, gspread, pygtk, gtk, glib, pango, math, random, gobject
pygtk.require('2.0')

from oauth2client.client import flow_from_clientsecrets

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

spreadsheet_file_name = "NEW words"
password_file_name = "pass.txt"
pause_between_word_changes_seconds = 10
max_one_line_string_length = 30
iterations_before_reload = 12
text_font = "Serif Bold 80"
background_color = '#000000'
word_color = '#88FF88'
translation_color = '#8888FF'

screen_width = gtk.gdk.screen_width()
automatic = -1

with open (__location__ + "/" + password_file_name, "r") as passfile:
    pass_strings = passfile.readlines()

username = pass_strings[0].strip()
password = pass_strings[1].strip()

class GsThemeWindow(gtk.Window):
    __gtype_name__ = 'GsThemeWindow'
    
    def reauthenticate_and_reload(self):
        self.gc = gspread.client.login(username, password)
        self.worksheet = self.gc.open(spreadsheet_file_name).sheet1
        self.all_values = self.worksheet.get_all_values()
        return self.all_values

    def random_word_and_translation(self):
        self.reload_counter = (self.reload_counter + 1) % iterations_before_reload
        if self.reload_counter == 0:
            try:
                self.all_values = self.worksheet.get_all_values()
            except:
                self.all_values = self.reauthenticate_and_reload()
        arow = random.choice(self.all_values)
        if arow and len(arow) >= 2:
            return arow
        return []
        
    def __init__(self):
        super(GsThemeWindow, self).__init__()
        self.connect("destroy", gtk.main_quit)

        self.reload_counter = 0
        self.reauthenticate_and_reload()

        self.fullscreen()

        self.label_word = gtk.Label("word")
        fontdesc = pango.FontDescription(text_font)
        self.label_word.modify_font(fontdesc)
        self.label_word.set_line_wrap(True)
        self.label_word.set_size_request(screen_width, automatic)
        self.label_word.set_justify(gtk.JUSTIFY_CENTER)
        self.label_word.set_alignment(0.5, 0.5)
        color = gtk.gdk.color_parse(word_color)
        self.label_word.modify_fg(gtk.STATE_NORMAL, color)
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_size_request(screen_width, automatic)
        self.vbox.add(self.label_word)
        self.add(self.vbox)

        self.label_translation = gtk.Label("translation")
        fontdesc = pango.FontDescription(text_font)
        self.label_translation.modify_font(fontdesc)
        self.label_translation.set_line_wrap(True)
        self.label_translation.set_size_request(screen_width, automatic)
        self.label_translation.set_justify(gtk.JUSTIFY_CENTER)
        self.label_translation.set_alignment(0.5, 0.5)
        color = gtk.gdk.color_parse(translation_color)
        self.label_translation.modify_fg(gtk.STATE_NORMAL, color)
        self.vbox.add(self.label_translation)
        
        self.set_position(gtk.WIN_POS_CENTER)
        color = gtk.gdk.color_parse(background_color)
        self.modify_bg(gtk.STATE_NORMAL, color)
        color = gtk.gdk.color_parse(word_color)
        self.modify_fg(gtk.STATE_NORMAL, color)

        self.update_text()

        self.connect("button_press_event", gtk.main_quit)   
        self.connect("key_press_event", self.key_press_event)

        glib.timeout_add_seconds(pause_between_word_changes_seconds, self.on_timer)
        
        self.fullscreen()
        self.show_all()
        
    def update_text(self):
        random_values = self.random_word_and_translation()
        if random_values and len(random_values) >= 2:
            word = random_values[0].strip()
            if len(word) > max_one_line_string_length:
                self.label_word.set_size_request(screen_width, automatic)
            else:
                self.label_word.set_size_request(automatic, automatic)
            self.label_word.set_text(word)

            translation = random_values[1].strip()
            if len(translation) > max_one_line_string_length:
                self.label_translation.set_size_request(screen_width, automatic)
            else:
                self.label_translation.set_size_request(automatic, automatic)
            self.label_translation.set_text(translation)
        
    def on_timer(self):
        self.update_text()
        return True
 
    def key_press_event(self, widget, event):
       if event.keyval == gtk.gdk.keyval_from_name('Left') or event.keyval == gtk.gdk.keyval_from_name('Right') or event.keyval == gtk.keysyms.space:
           self.update_text()
       else:
           gtk.main_quit()
       return True
        
    def do_realize(self):
        ident = os.environ.get('XSCREENSAVER_WINDOW')
        if not ident is None:
            self.window = gtk.gdk.window_foreign_new(int(ident, 16))
            self.window.set_events(gtk.gdk.EXPOSURE_MASK |
                                   gtk.gdk.STRUCTURE_MASK)
            x, y, w, h, depth = self.window.get_geometry()
            self.size_allocate(gtk.gdk.Rectangle(x, y, w, h))
            self.set_default_size(w, h)
            self.set_decorated(False)
        else:
            self.window = gtk.gdk.Window(
                self.get_parent_window(),
                width=self.allocation.width,
                height=self.allocation.height,
                window_type=gtk.gdk.WINDOW_TOPLEVEL,
                wclass=gtk.gdk.INPUT_OUTPUT,
                event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK)
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.set_flags(self.flags() | gtk.REALIZED)
        
GsThemeWindow()
gtk.main()
