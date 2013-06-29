#!/usr/bin/env python

# Killing and restarting mpd this hardcore might make me seem like an amateur
# bastard but for the record you have know that I started out with the Python
# MPD client library which would have been the right approach to take if MPD
# wasn't so supremely unstable.

from sys import stdout
from time import sleep
import RPi.GPIO as GPIO
import pickle
from os import system
from os.path import expanduser, basename
from urllib2 import urlopen

# Define constants and initialize globals.

ALL_STATIONS_PLAYLIST = '~/pidio/my-stations.m3u'
CURRENT_STATION_PLAYLIST = '/var/lib/mpd/playlists/current-station.m3u';
STATE_FILE = '~/pidio/state.pkl';

INITIAL_VOLUME = 100  # percent

BUTTON_SCAN_INTERVAL = 0.01  # seconds
BUTTON_LONG_PRESS_INTERVAL = 2  # seconds
STATION_FETCH_TIMEOUT = 2  # seconds

PRESET_BUTTON_COUNT = 5
PREVIOUS_BUTTON_INDEX = 5
NEXT_BUTTON_INDEX = 6

button_gpio_numbers = [7, 8, 15, 23, 25, 18, 14]
button_press_lengths = [0 for button_gpio_number in button_gpio_numbers]
is_playback_active = False

# The following unbuffers stdout.  Useful if you want to log script output and tail it real-time.

class Unbuffered:
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

stdout=Unbuffered(stdout)

# Event handlers

def load_preset(preset_index):
    station_url = button_presets[preset_index]
    if station_url == None:
        print 'no preset set for button', preset_index
        return
    print 'loading preset for button %d: %s' % (preset_index, station_url)
    play_station(station_url)

def store_preset(preset_index):
    print 'storing preset for button', preset_index
    button_presets[preset_index] = get_current_station()
    save_state()
    play_current_station()  # Acknowledge storage by a short pause in playback.

def previous_station():
    global current_station_index
    print 'previous station'
    current_station_index -= 1
    if current_station_index < 0:
        current_station_index = len(stations)-1
    play_current_station()
    save_state()

def next_station():
    global current_station_index
    print 'next station'
    current_station_index += 1
    if current_station_index >= len(stations):
        current_station_index = 0
    play_current_station()
    save_state()

def stop_playback():
    global is_playback_active
    if is_playback_active:
        print 'stopping playback'
        system('(mpc stop; killall -9 mpd mpc) >/dev/null 2>&1 &')
        is_playback_active = False
    else:
        play_current_station()

# Helper functions

def play_current_station():
    play_station(get_current_station())

def play_station(station_url):
    global is_playback_active
    try:
        current_playlist = urlopen(station_url, None, STATION_FETCH_TIMEOUT).read()
        with open(expanduser(CURRENT_STATION_PLAYLIST), "w") as station_file:
            station_file.write(current_playlist)
        system('(killall -9 mpd mpc; service mpd start; mpc clear; mpc load %s; mpc play) >/dev/null 2>&1 &' %
               (basename(CURRENT_STATION_PLAYLIST)))
        print 'playing', station_url
        is_playback_active = True;
    except:
        print "couldn't load", station_url

def get_current_station():
    return stations[current_station_index]

def save_state():
    state = {'current_station_index': current_station_index, 'button_presets': button_presets}
    with open(expanduser(STATE_FILE), 'wb') as file:
        pickle.dump(state, file)

# Event router

def button_pressed(button_index, is_long_press):
    if button_index < PRESET_BUTTON_COUNT:
        if is_long_press:
            store_preset(button_index)
        else:
            load_preset(button_index)
    elif button_index == PREVIOUS_BUTTON_INDEX:
        if not is_long_press:
            previous_station()
    elif button_index == NEXT_BUTTON_INDEX:
        if is_long_press:
            stop_playback()
        else:
            next_station()

# Initialize the GPIO pins of the buttons.

GPIO.setmode(GPIO.BCM)
for gpio_number in button_gpio_numbers:
    GPIO.setup(gpio_number, GPIO.IN)

# Load the playlist.

stations = open(expanduser(ALL_STATIONS_PLAYLIST)).read().splitlines()

# Load state.

try:
    with open(expanduser(STATE_FILE), 'rb') as file:
        state = pickle.load(file)

    current_station_index = state['current_station_index']
    button_presets = state['button_presets']
except:
    current_station_index = 0;
    button_presets = [None for button_gpio_number in button_gpio_numbers]
    save_state()

# Main loop

while True:
    button_states = [not GPIO.input(button_gpio_number) for button_gpio_number in button_gpio_numbers]
    for button_index, is_button_pressed in enumerate(button_states):
        old_press_length = button_press_lengths[button_index]
        new_press_length = old_press_length + BUTTON_SCAN_INTERVAL

        if is_button_pressed:
            if old_press_length < BUTTON_LONG_PRESS_INTERVAL and BUTTON_LONG_PRESS_INTERVAL <= new_press_length:
                button_pressed(button_index, True)
            button_press_lengths[button_index] = new_press_length
        else:
            if 0 < old_press_length and old_press_length < BUTTON_LONG_PRESS_INTERVAL:
                button_pressed(button_index, False)
            button_press_lengths[button_index] = 0
    sleep(BUTTON_SCAN_INTERVAL)
