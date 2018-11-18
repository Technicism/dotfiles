import gtk
import urllib
import terminatorlib.plugin as plugin
from terminatorlib.config import Config
import re

# Written by John Cooper http://choffee.co.uk
# Copyright 2010 John Cooper

# Copyright:
#
#     <Copyright (C) 2010 John Cooper>
#
# License:
#
#     This package is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation version 2.
#
#     This package is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this package; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# On Debian systems, the complete text of the GNU General
# Public License can be found in `/usr/share/common-licenses/GPL-2'.

# Modified by cgw 2011/11/06
# Modified by Technicism 2018/11/19
#   - Support config options to change the search engine.
#   - Embed the license for single file portability.

# See https://github.com/choffee/terminator-plugins for original source.

NAME = 'SearchPlugin'
AVAILABLE = [NAME]

_spaces = re.compile(" +")

config = Config()
base_uri = config.plugin_get(NAME, 'base_uri', 'https://www.google.com/search?q=%s')
label = config.plugin_get(NAME, 'label', 'Google Search')

class SearchPlugin(plugin.Plugin):
    capabilities = ['terminal_menu']

    def do_search(self, searchMenu):
        """Launch Google search for string"""
        if not self.searchstring:
            return
        uri = base_uri % urllib.quote(self.searchstring.encode("utf-8"))
        gtk.show_uri(None, uri, gtk.gdk.CURRENT_TIME)

    def callback(self, menuitems, menu, terminal):
        """Add our menu item to the menu"""
        self.terminal = terminal
        item = gtk.ImageMenuItem(gtk.STOCK_FIND)
        item.connect('activate', self.do_search)
        item.set_label(label)
        if terminal.vte.get_has_selection():
            clip = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
            self.searchstring = clip.wait_for_text().strip()
            self.searchstring = self.searchstring.replace("\n", " ")
            self.searchstring = self.searchstring.replace("\t", " ")
            self.searchstring = _spaces.sub(" ", self.searchstring)
        else:
            self.searchstring = None
        if self.searchstring:
            item.set_sensitive(True)
        else:
            item.set_sensitive(False)
        # Avoid turning any underscores in selection into menu accelerators
        item.set_use_underline(False)
        menuitems.append(item)
