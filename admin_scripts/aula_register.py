#!/usr/bin/env python

#================================================================
# HEADER
#================================================================
#% SYNOPSIS
#+    aula_register.py [URL, REGISTERCODE]
#%
#% DESCRIPTION
#%    This script registers a Aula "kommegaa" screen.
#%
#%    It takes three mandatory parameters:
#%      * The url for the registration to take place.
#%      * The register code needed to activate the "kommegaa" screen.
#%      * Should the cookies table be deleted and restored (Ja/Nej)
#%
#================================================================
#- IMPLEMENTATION
#-    version         aula_register.py (magenta.dk) 1.0.0
#-    author          Danni Als
#-    copyright       Copyright 2019, Magenta ApS
#-    license         GNU General Public License v3+
#-    email           danni@magenta.dk
#-
#================================================================
#  HISTORY
#     2019/10/28 : da : Script created
#     2019/11/11 : da : The scripts now tries to detect if the Google Chrome cookies table is out of date.
#     2019/11/11 : da : Added the option to completely reset cookie store.
#
#================================================================
# END_OF_HEADER
#================================================================

import os
import glob
import sys
import stat
import datetime
import subprocess

subprocess.call([sys.executable, "-m", "pip", "install", 'wget'])
subprocess.call([sys.executable, "-m", "pip", "install", 'selenium'])

print('Installed wget and selenium.')

import wget
import zipfile
import sqlite3

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.common.exceptions import InvalidArgumentException

if len(sys.argv) == 4:
    url = sys.argv[1]
    print('Aula registration URL: {}'.format(url))
    register_code = sys.argv[2]
    print('Registration code: {}'.format(register_code))
    try:
        int(register_code)
    except ValueError:
        print('Registration code is not a number.')
        print('Registration code is of type {}'.format(type(register_code)))
        sys.exit(1)
    if len(register_code) != 8:
        print('Registration code does not have the correct lenght.')
        sys.exit(1)

    # Option for HARD reset of cookies table.
    hard_reset_cookies = sys.argv[3]
else:
    print('One or more parameters are missing.')
    sys.exit(1)

# get chrome version
chrome_version = os.popen('google-chrome --version').read()
# String returned is always 'Google Chrome xx.x.xxxx.xx'
chrome_version = chrome_version.split(' ')
chrome_version = chrome_version[2].split('.')[0]
print('Chrome version installed: {}'.format(chrome_version))
if chrome_version == '74':
    driver_version = '74.0.3729.6'
elif chrome_version == '75':
    driver_version = '75.0.3770.140'
elif chrome_version =='76':
    driver_version = '76.0.3809.126'
elif chrome_version == '77':
    driver_version = '77.0.3865.40'
elif chrome_version == '78':
    driver_version = '78.0.3904.70'
else:
    print('Chrome version not supported.')
    sys.exit(1)

system_path = '/usr/local/bin'
zipfile_name = driver_version + 'chromedriver_linux64.zip'
zip_path = os.path.join(system_path, zipfile_name)
extracted_filename = 'chromedriver'
extracted_filepath = os.path.join(system_path, extracted_filename)

# download gecko and setup
if not os.path.isfile(zip_path):
    try:
        for fl in glob.glob(system_path + '/*chromedriver_linux64.zip'):
            os.remove(fl)
        for fl1 in glob.glob(system_path + '/chromedriver'):
            os.remove(fl1)
    except OSError:
        pass

    chromedriver_url = 'https://chromedriver.storage.googleapis.com/' + driver_version + '/chromedriver_linux64.zip'
    wget.download(chromedriver_url, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(system_path)

    os.chmod(extracted_filepath, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IXOTH)

    print('Chromedriver downloaded and extracted to path: {}'.format(
        extracted_filepath)
    )
else:
    print('Chromedriver {} is already setup.'.format(driver_version))

user_dir = '/home/.skjult/.config/google-chrome/'

if hard_reset_cookies == 'Ja':
    os.remove(user_dir + '/Default/Cookies')

# start chrome headless
opts = Options()
# opts.set_headless()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('user-data-dir=' + user_dir)
# assert opts.headless  # Operating in headless mode
browser = Chrome(chrome_options=opts, executable_path=extracted_filepath)
wait = WebDriverWait(browser, timeout=10)
try:
    browser.get(url)
except InvalidArgumentException as iae:
    print('Invalid argument given: {} of type {}'.format(url, type(url)))
    print(iae.message)
    sys.exit(1)

print('Chrome browser opened headless with url: {}'.format(url))
register_code_list = list(str(register_code))
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__11'))).send_keys('' + register_code_list[0] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__12'))).send_keys('' + register_code_list[1] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__13'))).send_keys('' + register_code_list[2] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__14'))).send_keys('' + register_code_list[3] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__15'))).send_keys('' + register_code_list[4] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__16'))).send_keys('' + register_code_list[5] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__17'))).send_keys('' + register_code_list[6] + Keys.ENTER)
wait.until(expected.visibility_of_element_located((By.ID, '__BVID__18'))).send_keys('' + register_code_list[7] + Keys.ENTER)

try:
    wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'aula-presence-overview')))
except Exception:
    print('Aula presence overview did not show up. Check that the register code is correct and valid: {}'.format(register_code))
    sys.exit(1)

cookies_list = browser.get_cookies()
print('Cookies {}'.format(cookies_list))

browser.close()
print('Google Chrome headless browser closed.')

chrome_db_path = user_dir + '/Default/Cookies'
conn = None
try:
    conn = sqlite3.connect(chrome_db_path)
except Error as e:
    print('DB connection could not be established on path {}'.format(chrome_db_path))
    sys.exit(1)

cursor = conn.cursor()

# look for old aula cookies and remove if present.
if hard_reset_cookies == 'Nej':
    cursor.execute("SELECT host_key FROM cookies WHERE host_key LIKE '%aula%'")

    if len(cursor.fetchall()) > 1:
        # Remove old cookies.
        cursor.execute("DELETE FROM cookies WHERE host_key LIKE '%aula%'")
        conn.commit()
        print('Old aula cookies removed.')

for cookie in cookies_list:
    # Timedelta since epoch to now.
    epoch_delta = datetime.datetime.now() - datetime.datetime(1601, 1, 1)
    # Creation time in milliseconds from epoch (Google chrome needs this).
    creation_utc = int((epoch_delta).total_seconds() * 1e6)
    # Experation is 1 year into the future.
    # expires_utc = int((epoch_delta + datetime.timedelta(days=365)).total_seconds() * 1e6)
    # Example of a cookie insert
    # insert into cookies (creation_utc, host_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, encrypted_value, samesite)  values (13217424586631416, 'uddannelse.aula.dk', 'Csrfp-Token', '', '/', 0, 1, 0, 13217424586631416, 0, 0, 1, '833a0a025e2bc7539c3289980099d738', -1)
    has_expires = 1
    if cookie.get('name') == 'PHPSESSID':
        has_expires = 0
    cursor.execute("INSERT INTO cookies (creation_utc, host_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, encrypted_value) VALUES ({}, '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, '{}')".format(creation_utc, cookie.get('domain'), cookie.get('name'), 'd' ,cookie.get('path'), 0, int(cookie.get('secure')), int(cookie.get('httpOnly')), creation_utc, has_expires, 1, 1, cookie.get('value')))
    conn.commit()
    print('Cookie with name {} stored in cookie db.'.format(cookie.get('name')))

conn.close()
