"""Headless functional + responsive verification; NOT a real human-device study."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


def test_desktop_and_mobile(tmp_path):
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        _run_browser(server.server_port)
    finally:
        server.shutdown();server.server_close()

def _run_browser(port):
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for label,viewport in [('mobile',{'width':390,'height':844}),('desktop',{'width':1440,'height':980})]:
            page=browser.new_page(viewport=viewport,is_mobile=(label=='mobile'),has_touch=(label=='mobile'))
            errors=[]
            page.on('pageerror',lambda error: errors.append(str(error)))
            page.set_content((ROOT/'index.html').read_text('utf-8'),wait_until='load')
            assert page.locator('#layout-picks button').count()==5
            assert page.locator('#demo-board .key').count()==29
            assert page.locator('#metric-grid .metric').count()==4
            assert page.locator('text=14.811').count()>=1
            page.screenshot(path=str(ROOT/'report'/f'ui_{label}_analysis.png'),full_page=True)
            page.locator('button[data-tab="calibrate"]').click()
            page.locator('#left-hand').click()
            assert '0 / 30' in page.locator('#cal-progress').inner_text()
            assert page.locator('#cal-board .target').count()==1
            target=page.locator('#cal-board .target')
            target.dispatch_event('pointerdown',{'pointerType':'touch','button':0,'clientX':80,'clientY':100})
            assert page.locator('#cal-progress').inner_text()=='1 / 30'
            assert '1/30' in page.locator('#heat-stats').inner_text()
            page.screenshot(path=str(ROOT/'report'/f'ui_{label}_calibration.png'),full_page=True)
            # Artificial events cover code paths, not human performance.
            for hand in ('left','right'):
                page.locator(f'#{hand}-hand').click()
                for _ in range(30):
                    page.locator('#cal-board .target').dispatch_event('pointerdown',{
                        'pointerType':'touch','button':0,'clientX':80,'clientY':100
                    })
            assert not page.locator('#make-personal').is_disabled()
            page.locator('#make-personal').click()
            assert page.locator('#layout-picks button').count()==6
            assert page.locator('#demo-board .key').count()==29
            assert page.locator('#test-layout option[value="P29"]').count()==1
            page.locator('button[data-tab="typing"]').click()
            assert page.locator('#typing-board .key').count()==29
            page.locator('#test-layout').select_option('Q32')
            assert page.locator('#typing-board .key').count()==32
            prompt=page.locator('#prompt').inner_text()
            for ch in prompt:
                if ch==' ': page.locator('#key-space').dispatch_event('pointerdown',{'pointerType':'touch','button':0})
                else:page.locator(f'#typing-board button[data-letter="{ch}"]').dispatch_event('pointerdown',{'pointerType':'touch','button':0})
            assert page.locator('#trial-history tbody tr').count()==1
            assert page.locator('#export-trials-raw').count()==1
            assert 'tamamlandı' in page.locator('#test-status').inner_text()
            page.screenshot(path=str(ROOT/'report'/f'ui_{label}_typing.png'),full_page=True)
            over=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
            assert not over, f'{label}: unexpected horizontal viewport overflow'
            assert len(page.locator('.entry').inner_text())>=len(prompt)
            assert not errors, f'{label} JavaScript errors: {errors}'
            page.close()
        browser.close()
