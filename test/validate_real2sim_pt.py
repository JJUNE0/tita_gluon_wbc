"""DESKTOP_DRY_RUN: offline Chrome CDP presentation QA (stdlib only).

Start a dedicated headless Chrome on port 9327 first. No robot/network APIs.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "docs/exp/2026-10-19/real2sim2real_pt"
EVIDENCE = DECK / "assets"


class CDP:
    def __init__(self):
        targets = json.load(urllib.request.urlopen("http://127.0.0.1:9327/json"))
        target = next(t for t in targets if t["type"] == "page")
        url = target["webSocketDebuggerUrl"]
        path = "/" + url.split("/", 3)[3]
        self.sock = socket.create_connection(("127.0.0.1", 9327), timeout=20)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f"GET {path} HTTP/1.1\r\nHost: localhost:9327\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\nOrigin: http://localhost:9327\r\n\r\n").encode())
        response = b""
        while not response.endswith(b"\r\n\r\n"):
            response += self.sock.recv(1)
        assert response.split(b"\r\n", 1)[0].split()[1] == b"101", response
        accept = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest())
        assert accept in response
        self.counter = 0
        self.errors = []

    def read(self, count):
        data = b""
        while len(data) < count:
            chunk = self.sock.recv(count - len(data))
            if not chunk:
                raise RuntimeError("CDP disconnected")
            data += chunk
        return data

    def receive(self):
        header = self.read(2)
        length = header[1] & 127
        if length == 126:
            length = struct.unpack("!H", self.read(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self.read(8))[0]
        return json.loads(self.read(length))

    def call(self, method, **params):
        self.counter += 1
        payload = json.dumps({"id": self.counter, "method": method, "params": params}).encode()
        mask = os.urandom(4)
        header = bytes([0x81])
        if len(payload) < 126:
            header += bytes([0x80 | len(payload)])
        elif len(payload) < 65536:
            header += bytes([0x80 | 126]) + struct.pack("!H", len(payload))
        else:
            header += bytes([0x80 | 127]) + struct.pack("!Q", len(payload))
        self.sock.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
        while True:
            message = self.receive()
            if message.get("method") == "Runtime.exceptionThrown":
                self.errors.append(message)
            if message.get("id") == self.counter:
                if "error" in message:
                    raise RuntimeError(message)
                return message.get("result", {})

    def evaluate(self, expression):
        result = self.call("Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in result:
            raise RuntimeError(result["exceptionDetails"])
        return result.get("result", {}).get("value")

    def settle(self):
        self.evaluate("new Promise(resolve=>setTimeout(()=>resolve(true),450))")

    def capture(self, name):
        result = self.call("Page.captureScreenshot", format="png", captureBeyondViewport=False)
        (EVIDENCE / name).write_bytes(base64.b64decode(result["data"]))


def main():
    c = CDP()
    c.call("Page.enable")
    c.call("Runtime.enable")
    c.call("Emulation.setDeviceMetricsOverride", width=1600, height=900, deviceScaleFactor=1, mobile=False)
    c.call("Page.navigate", url=(DECK / "index.html").as_uri())
    c.settle()
    assert c.evaluate("window.PT.count") == 8
    c.evaluate("document.querySelector('#pause-button').click()")
    checks = []
    for i in range(8):
        c.evaluate(f"PT.go({i})")
        if i < 4:
            c.evaluate("PT.seekX(30)")
        elif i == 5:
            c.evaluate("PT.seekContact(23.98)")
        else:
            c.evaluate("PT.seekMotion(16)")
        c.settle()
        state = c.evaluate("""(()=>{const s=document.querySelector('.slide.active');return {
          slide:PT.current+1, title:s.dataset.title,
          canvases:[...s.querySelectorAll('canvas')].map(c=>({rendered:c.dataset.rendered,error:c.dataset.renderError||null})),
          verticalOverflow:s.scrollHeight>s.clientHeight+2,
          horizontalOverflow:s.scrollWidth>s.clientWidth+2,
          linksValid:PT.records[PT.current].sources.map(x=>x.href)
        }})()""")
        assert all(x["rendered"] == "true" and not x["error"] for x in state["canvases"]), state
        assert not state["horizontalOverflow"], state
        assert not state["verticalOverflow"], state
        for link in state["linksValid"]:
            assert (DECK / link).resolve().exists(), link
        checks.append(state)
        c.capture(f"slide-{i+1:02d}.png")
        if i == 0:
            png = c.evaluate("document.querySelector('canvas').toDataURL('image/png').split(',')[1]")
            (EVIDENCE / "tita-fallback.png").write_bytes(base64.b64decode(png))
    # X drift is real world translation, synchronized camera/time and source endpoints.
    c.evaluate("PT.go(2);document.querySelector('.slide.active .x-scrub').value=30;document.querySelector('.slide.active .x-scrub').dispatchEvent(new Event('input'))")
    xy=c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].map(c=>[Number(c.dataset.x),Number(c.dataset.y)])")
    assert abs(xy[0][0]-.425853)<1e-5 and abs(xy[1][0]+.0001714)<1e-5,xy
    c.evaluate("document.querySelector('.slide.active canvas').dispatchEvent(new WheelEvent('wheel',{deltaY:100,cancelable:true}))")
    assert c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].map(c=>c.dataset.camera).every((v,i,a)=>v===a[0])")
    c.evaluate("document.querySelector('.slide.active canvas').dispatchEvent(new MouseEvent('dblclick'))")
    c.capture("eight-x-comparison-30s.png")
    c.evaluate("document.querySelector('.slide.active [data-range=\"300\"]').click();document.querySelector('.slide.active .x-scrub').value=300;document.querySelector('.slide.active .x-scrub').dispatchEvent(new Event('input'))")
    assert c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].every(c=>Number(c.dataset.replayTime)===300)")
    assert c.evaluate("Math.abs(Number(document.querySelector('.slide.active [data-scene=xBefore]').dataset.x)-PT_REPLAYS.x_nominal_0.xy.at(-1)[0])<1e-6")
    assert c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].map(c=>c.dataset.camera).every((v,i,a)=>v===a[0])")
    c.capture("eight-x-comparison-300s.png")
    for condition in ["nominal","low_friction","com_forward_mass115","com_backward_mass115"]:
        c.evaluate(f"PT.go(3);document.querySelector('[data-x-case={condition}]').click();PT.setXRange(300);PT.seekX(300)")
        assert c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].every(c=>Number(c.dataset.replayTime)===300&&c.dataset.rendered==='true')")
        assert c.evaluate(f"PT_REPLAYS.x_{condition}_0.initial_state_sha256===PT_REPLAYS.x_{condition}_1.initial_state_sha256")
        assert c.evaluate(f"Math.abs(Number(document.querySelector('.slide.active [data-scene=xBefore]').dataset.x)-PT_REPLAYS.x_{condition}_0.xy.at(-1)[0])<1e-6")
    c.evaluate("PT.setXCase('com_backward_mass115');PT.setXRange(30);PT.seekX(30)")
    c.capture("eight-x-mismatch.png")
    # Revisit disposes/reinitializes GPU buffers; test a complete return trip.
    c.evaluate("PT.go(5);document.querySelector('#contact-scrub').value=23.98;document.querySelector('#contact-scrub').dispatchEvent(new Event('input'))")
    end_angles=c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].map(c=>Number(c.dataset.rotation)*180/Math.PI)")
    assert abs(end_angles[0]-4.0817764)<.001 and abs(end_angles[1]-53.8172131)<.001, end_angles
    assert c.evaluate("document.querySelector('#contact-play').getAttribute('aria-pressed')") == "false"
    c.capture("motion-contact-end.png")
    c.evaluate("document.querySelector('#contact-scrub').value=0;document.querySelector('#contact-scrub').dispatchEvent(new Event('input'))")
    assert c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].every(c=>Math.abs(Number(c.dataset.rotation))<1e-6)")
    c.evaluate("PT.go(7);PT.seekMotion(16)")
    heading_angles=c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].map(c=>Number(c.dataset.rotation)*180/Math.PI)")
    assert heading_angles[0]>80 and abs(heading_angles[1])<.5, heading_angles
    c.capture("motion-heading-end.png")
    c.evaluate("PT.go(5); document.querySelector('#collision-toggle').click(); document.querySelector('#contact-zoom').click()")
    c.settle()
    assert c.evaluate("document.querySelector('#collision-toggle').getAttribute('aria-pressed')") == "false"
    assert c.evaluate("document.querySelector('#contact-zoom').getAttribute('aria-pressed')") == "true"
    c.capture("contact-zoom.png")
    c.evaluate("document.querySelector('#collision-toggle').click(); document.querySelector('#contact-zoom').click(); document.querySelector('#notes-button').click()")
    assert c.evaluate("!document.querySelector('#drawer').hidden && document.querySelector('#drawer-content').textContent.includes('collision')")
    c.evaluate("document.querySelector('#evidence-button').click()")
    assert c.evaluate("document.querySelector('#drawer-content').textContent.includes('SHA256')")
    c.evaluate("document.querySelector('#drawer-close').click(); document.querySelector('#overview-button').click()")
    assert c.evaluate("document.querySelector('#overview').open")
    c.evaluate("document.querySelector('#overview-close').click(); PT.go(0)")
    c.call("Input.dispatchKeyEvent", type="keyDown", key="ArrowRight")
    c.call("Input.dispatchKeyEvent", type="keyUp", key="ArrowRight")
    assert c.evaluate("PT.current") == 1
    # Desktop laptop and mobile widths: readable scrolling is allowed on mobile.
    for width, height in [(1366, 768), (390, 844), (820, 1180)]:
        c.call("Emulation.setDeviceMetricsOverride", width=width, height=height, deviceScaleFactor=1, mobile=False)
        for i in range(8):
            c.evaluate(f"PT.go({i})")
            c.settle()
            layout = c.evaluate("(()=>{const s=document.querySelector('.slide.active'); return {horizontal:s.scrollWidth>s.clientWidth+2, vertical:s.scrollHeight>s.clientHeight+2, canvases:[...s.querySelectorAll('canvas')].every(c=>c.dataset.rendered==='true'&&!c.dataset.renderError)}})()")
            assert not layout["horizontal"], (width, i+1, layout)
            assert layout["canvases"], (width, i+1, layout)
            if width == 1366:
                assert not layout["vertical"], (width, i+1, layout)
            if i in [0, 2, 5, 7] and width != 1366:
                c.capture(f"responsive-{width}-slide-{i+1:02d}.png")
    assert not c.errors, c.errors
    result = {"execution_domain": "DESKTOP_DRY_RUN", "evidence_status": "PASS", "desktop_slides": checks,
              "sizes": ["1600x900", "1366x768", "390x844", "820x1180"],
              "checks": ["all WebGL scenes rendered", "source links exist", "keyboard navigation", "notes/evidence/overview", "collision toggle", "zoom", "revisit GPU resources", "no horizontal overflow", "no desktop vertical overflow", "zero JS runtime exceptions", "recorded contact endpoint yaw 4.0818 vs 53.8172 deg", "scrub returns both replays to zero", "real-log heading before/after playback", "X translation at 30s and 300s", "X before/after synchronized camera", "four X physics-condition selectors", "X initial-state hashes paired"],
              "limitations": ["Recorded q/orientation replay; no new physics", "Real world position anchored", "X: ground-truth XY evaluation replay, control remains sensor-only", "X real-hardware drift remains unresolved", "no robot or policy execution"]}
    (DECK / "qa-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print("DESKTOP_DRY_RUN PASS: 8 slides × 4 viewports, WebGL, navigation, notes, sources, collision toggles, zero runtime exceptions")


def standalone_smoke():
    c = CDP()
    c.call("Page.enable")
    c.call("Runtime.enable")
    c.call("Emulation.setDeviceMetricsOverride", width=1600, height=900, deviceScaleFactor=1, mobile=False)
    c.call("Page.navigate", url=(DECK / "standalone.html").as_uri())
    c.settle()
    c.evaluate("document.querySelector('#pause-button').click()")
    for i in range(8):
        c.evaluate(f"PT.go({i})")
        if i < 4:
            c.evaluate("PT.seekX(30)")
        elif i == 5:
            c.evaluate("PT.seekContact(23.98)")
        else:
            c.evaluate("PT.seekMotion(16)")
        c.settle()
        assert c.evaluate("[...document.querySelector('.slide.active').querySelectorAll('canvas')].every(c=>c.dataset.rendered==='true'&&!c.dataset.renderError)")
        assert c.evaluate("(()=>{const s=document.querySelector('.slide.active');return s.scrollHeight<=s.clientHeight+2&&s.scrollWidth<=s.clientWidth+2})()")
        if i in [0, 2, 5, 7]:
            c.capture(f"standalone-slide-{i+1:02d}.png")
    assert c.evaluate("performance.getEntriesByType('resource').length") == 0
    assert not c.errors, c.errors
    c.evaluate("PT.go(0)")
    pdf = c.call("Page.printToPDF", landscape=True, displayHeaderFooter=False, printBackground=True, preferCSSPageSize=True)
    (DECK / "real2sim2real_pt.pdf").write_bytes(base64.b64decode(pdf["data"]))
    # Deliberately disable WebGL, then confirm the self-contained image fallback.
    injection = c.call("Page.addScriptToEvaluateOnNewDocument", source="const getContext=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(type==='webgl')return null;return getContext.call(this,type,...args)}")
    c.call("Page.reload")
    c.settle()
    assert c.evaluate("document.querySelector('.webgl-fallback img').complete && document.querySelector('.webgl-fallback img').naturalWidth>0")
    c.capture("fallback-no-webgl.png")
    c.call("Page.removeScriptToEvaluateOnNewDocument", identifier=injection["identifier"])
    c.call("Page.reload")
    c.settle()
    result = {"execution_domain": "DESKTOP_DRY_RUN", "evidence_status": "PASS", "slides": 8,
              "external_resource_requests": 0, "fallback_without_webgl": "PASS", "pdf_generated": True,
              "runtime_exceptions": len(c.errors)}
    (DECK / "standalone-qa-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("DESKTOP_DRY_RUN PASS: standalone 8 slides, zero external resources, PDF generated, WebGL fallback")


if __name__ == "__main__":
    if "--standalone" in sys.argv:
        standalone_smoke()
    else:
        main()
