import os
import re
from dotenv import load_dotenv

from playwright.sync_api import expect, sync_playwright

load_dotenv()
WORKFLOW = os.getenv('WORKFLOW')


with sync_playwright() as p:
    if WORKFLOW == 'local':
        baseurl = 'http://127.0.0.1:8000'
        browser = p.chromium.launch(headless=False, slow_mo=1000)
    else:
        baseurl = 'http://127.0.0.1:8000'
        browser = p.chromium.launch()

    page = browser.new_page()

    # page home
    page.goto(baseurl)
    expect(page).to_have_title(re.compile('Менеджер задач'))
    page.get_by_role('link', name='Пользователи').click()

    # page users
    expect(page).to_have_title(re.compile('Пользователи'))
    expect(page.get_by_text('tomilov')).to_be_visible()
