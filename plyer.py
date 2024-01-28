import subprocess
import tracemalloc
import data_centre.length_setter as length_setter
import sys
import shlex
import os
from pythonosc import osc_message_builder
from pythonosc import dispatcher
from pythonosc import osc_server
import git
import threading
import argparse
from video_centre.capture import Capture
from video_centre.of_capture import OfCapture

class Actions(object):
    def __init__(self, tk, message_handler, data, video_driver, shaders, display, osc_client):
        self.tk = tk
        self.message_handler = message_handler
        self.data = data
        self.video_driver = video_driver
        self.shaders = shaders
        self.display = display
        self.osc_client = osc_client
        self.of_capture = OfCapture(self.tk, self.osc_client, self.message_handler, self.data)
        self.python_capture = self.capture = Capture(self.tk, self.message_handler, self.data)
        self.capture = None
        self.serial_port_process = None
        self.openframeworks_process = None
        self.set_capture_object('value')
        self.server = self.setup_osc_server()
        
    def set_capture_object(self, value):
        if self.data.settings['video']['VIDEOPLAYER_BACKEND']['value'] != 'omxplayer':
            self.python_capture.close_capture()
            self.capture = self.of_capture
        else:
            self.python_capture.close_capture()
            self.capture = self.python_capture
        self.display.capture = self.capture

    def move_browser_selection_down(self):
        self.display.browser_menu.navigate_menu_down()

    def move_browser_selection_up(self):
        self.display.browser_menu.navigate_menu_up()

    def enter_on_browser_selection(self):
        self.display.browser_menu.enter_on_browser_selection()

    def move_settings_selection_down(self):
        self.display.settings_menu.navigate_menu_down()

    def move_settings_selection_up(self):
        self.display.settings_menu.navigate_menu_up()

    def enter_on_settings_selection(self):
        is_setting, setting = self.display.settings_menu.enter_on_setting_selection()
        if is_setting:
            if setting['action']:
                if setting['value'] is None:
                    getattr(self, setting['action'])()
                else:
                    getattr(self, setting['action'])(setting['value'])

    def move_shaders_selection_down(self):
        self.shaders.shaders_menu.navigate_menu_down()

    def move_shaders_selection_up(self):
        self.shaders.shaders_menu.navigate_menu_up()

    def enter_on_shaders_selection(self):
        ##want to select shader if its not selected, and want to enter 'param' mode if it already is
        is_shader, is_selected_shader, selected_shader = self.shaders.enter_on_shaders_selection()
        if is_selected_shader and selected_shader['param_number'] > 0:
            self.set_shader_param_mode()

    def map_on_shaders_selection(self):
        self.shaders.map_on_shaders_selection()

    def clear_all_slots(self):
        self.data.clear_all_slots()
        self.display.browser_menu.generate_browser_list()

    def _load_this_slot_into_next_player(self, slot):
 ### load next player for seamless type otherwise respect player mode
        if self.data.settings['sampler']['LOOP_TYPE']['value'] == 'seamless':
            if self.data.update_next_slot_number(slot):
                print('should reload next player !! ')
                self.video_driver.reload_next_player()
        else:
            if self.data.player_mode == 'next':
                if self.data.update_next_slot_number(slot, is_current=False):
                    self.video_driver.reload_next_player()
            else:
                if self.data.update_next_slot_number(slot, is_current=True):
                    self.video_driver.reload_current_player()
           


    def load_slot_0_into_next_player(self):
        self._load_this_slot_into_next_player(0)

    def load_slot_1_into_next_player(self):
        self._load_this_slot_into_next_player(1)

    def load_slot_2_into_next_player(self):
        self._load_this_slot_into_next_player(2)

    def load_slot_3_into_next_player(self):
        self._load_this_slot_into_next_player(3)

    def load_slot_4_into_next_player(self):
        self._load_this_slot_into_next_player(4)

    def load_slot_5_into_next_player(self):
        self._load_this_slot_into_next_player(5)

    def load_slot_6_into_next_player(self):
        self._load_this_slot_into_next_player(6)

    def load_slot_7_into_next_player(self):
        self._load_this_slot_into_next_player(7)

    def load_slot_8_into_next_player(self):
        self._load_this_slot_into_next_player(8)

    def load_slot_9_into_next_player(self):
        self._load_this_slot_into_next_player(9)

    def switch_to_next_player(self):
        if self.data.settings['sampler']['LOOP_TYPE']['value'] == 'seamless':
            self.video_driver.switch_players_and_start_video()
        else:
            self.video_driver.current_player.toggle_show()
            if self.video_driver.current_player.show_toggle_on == self.video_driver.next_player.show_toggle_on:
                self.video_driver.next_player.toggle_show()


    def cycle_display_mode(self):
        display_modes = self.data.get_display_modes_list(with_nav_mode=True)

        current_mode_index = [index for index, i in enumerate(display_modes) if self.data.display_mode in i][0]
        next_mode_index = (current_mode_index + 1) % len(display_modes) 
        self.data.display_mode = display_modes[next_mode_index][0]
        self.data.control_mode = display_modes[next_mode_index][1]
