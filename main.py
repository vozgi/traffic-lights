from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import dp
from kivy.core.window import Window
Window.clearcolor = (0.08, 0.09, 0.12, 1)

PRESETS = {
"RU-std":[{"name":"Красный","color":[1,0,0,1],"duration":20},{"name":"Кр+Жёл","color":[1,0.55,0,1],"duration":2},{"name":"Зелёный","color":[0,1,0,1],"duration":20},{"name":"Жёлтый","color":[1,1,0,1],"duration":3}],
"RU-arrow":[{"name":"Красный","color":[1,0,0,1],"duration":15},{"name":"Кр+▶","color":[1,0,0,1],"arrow":"right","arrow_color":[0,1,0,1],"duration":12},{"name":"Зелёный","color":[0,1,0,1],"duration":18},{"name":"Жёлтый","color":[1,1,0,1],"duration":3}],
"RU-ped":[{"name":"Стой","color":[1,0,0,1],"duration":20},{"name":"Иди","color":[0,1,0,1],"duration":15},{"name":"Мигает","color":[0,1,0,1],"blink":True,"duration":4}],
"US-std":[{"name":"Зелёный","color":[0,0.9,0,1],"duration":20},{"name":"Жёлтый","color":[1,0.8,0,1],"duration":4},{"name":"Красный","color":[1,0,0,1],"duration":20}],
"US-blink":[{"name":"Мигает","color":[1,0,0,1],"blink":True,"duration":30}],
"FR-std":[{"name":"Красный","color":[1,0,0,1],"duration":20},{"name":"Жёлтый","color":[1,1,0,1],"duration":3},{"name":"Зелёный","color":[0,1,0,1],"duration":20},{"name":"Жёлтый","color":[1,1,0,1],"duration":3}],
"LU-std":[{"name":"Красный","color":[1,0,0,1],"duration":15},{"name":"Кр+Жёл","color":[1,0.55,0,1],"duration":2},{"name":"Зелёный","color":[0,1,0,1],"duration":20},{"name":"Жёлтый","color":[1,1,0,1],"duration":3}],
"ZD-2":[{"name":"Красный","color":[1,0,0,1],"duration":10},{"name":"Зелёный","color":[0,1,0,1],"duration":15}],
"ZD-3":[{"name":"Красный","color":[1,0,0,1],"duration":10},{"name":"Жёлтый","color":[1,1,0,1],"duration":5},{"name":"Зелёный","color":[0,1,0,1],"duration":15},{"name":"Жёл миг","color":[1,1,0,1],"blink":True,"duration":5}],
"ZD-4":[{"name":"Красный","color":[1,0,0,1],"duration":8},{"name":"Жёлтый","color":[1,1,0,1],"duration":4},{"name":"Зел+Жёл","color":[1,0.7,0,1],"duration":4},{"name":"Зелёный","color":[0,1,0,1],"duration":12},{"name":"Лунно-бел","color":[0.85,0.95,1,1],"duration":6}],
"ZD-prigl":[{"name":"2 красных","color":[1,0,0,1],"duration":8},{"name":"Лунно-бел","color":[0.85,0.95,1,1],"duration":10}],
"SEM-1":[{"name":"Закрыт","color":[1,0,0,1],"semaphore":"up","duration":10},{"name":"Открыт","color":[0,1,0,1],"semaphore":"down","duration":15}],
"SEM-2":[{"name":"Стой","color":[1,0,0,1],"semaphore":"up","duration":8},{"name":"Скорость 20","color":[1,1,0,1],"semaphore":"up_one","duration":5},{"name":"Полный ход","color":[0,1,0,1],"semaphore":"down","duration":15}],
}

class LightWidget(FloatLayout):
    current_index = NumericProperty(0)
    blink_state = NumericProperty(1)
    remaining_time = NumericProperty(0)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sequence = []
        self.show_timer = True
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_interval(self._blink, 0.4)
    def set_sequence(self, seq):
        self.sequence = seq
        self.current_index = 0
        self.redraw()
    def _blink(self, dt):
        self.blink_state = 1 - self.blink_state
        self.redraw()
    def redraw(self, *a):
        self.canvas.clear()
        if not self.sequence:
            return
        with self.canvas:
            n = len(self.sequence)
            cur = self.sequence[self.current_index % n]
            Color(0.1, 0.1, 0.1, 1)
            bw = min(self.width * 0.8, dp(220))
            bh = max(self.height * 0.75, dp(200))
            bx = self.center_x - bw / 2
            by = self.y + dp(10)
            Rectangle(pos=(bx, by), size=(bw, bh))
            rad = min(bw / 2.6, (bh / n) / 2.4)
            sp = bh / n
            for i, sig in enumerate(self.sequence):
                cy = by + bh - sp * (i + 0.5)
                col = sig.get("color", [0.3, 0.3, 0.3, 1])
                on = (i == self.current_index % n)
                if on and not (sig.get("blink") and self.blink_state == 0):
                    Color(*col)
                else:
                    Color(col[0]*0.15, col[1]*0.15, col[2]*0.15, 1)
                Ellipse(pos=(self.center_x - rad, cy - rad), size=(rad*2, rad*2))
                if on and sig.get("arrow"):
                    self._arrow(self.center_x, cy, rad, sig["arrow"], sig.get("arrow_color", [0,0,0,1]))
            if cur.get("semaphore"):
                self._sem(self.center_x, self.y + self.height * 0.9, cur["semaphore"], cur.get("color", [1,0,0,1]))
            if self.show_timer and self.remaining_time > 0:
                self._timer(self.center_x, self.y + self.height * 0.97)
    def _arrow(self, cx, cy, r, d, col):
        Color(*col)
        Line(points=[cx - r*0.5, cy, cx + r*0.5, cy], width=dp(4))
        if d == "right":
            Line(points=[cx + r*0.15, cy + r*0.35, cx + r*0.6, cy, cx + r*0.15, cy - r*0.35], width=dp(4))
        elif d == "left":
            Line(points=[cx - r*0.15, cy + r*0.35, cx - r*0.6, cy, cx - r*0.15, cy - r*0.35], width=dp(4))
    def _sem(self, cx, cy, mode, color):
        Color(0.4, 0.3, 0.2, 1)
        Rectangle(pos=(cx - dp(4), cy - dp(120)), size=(dp(8), dp(120)))
        wl = dp(70)
        if mode == "up":
            Color(0.8, 0.1, 0.1, 1)
            Rectangle(pos=(cx, cy - dp(20)), size=(wl, dp(12)))
            Rectangle(pos=(cx - wl, cy - dp(20)), size=(wl, dp(12)))
        elif mode == "up_one":
            Color(0.8, 0.1, 0.1, 1)
            Rectangle(pos=(cx, cy - dp(20)), size=(wl, dp(12)))
            Color(0.1, 0.7, 0.1, 1)
            Rectangle(pos=(cx - wl, cy - dp(20)), size=(wl, dp(12)))
        else:
            Color(0.1, 0.7, 0.1, 1)
            Rectangle(pos=(cx, cy - dp(20)), size=(wl, dp(12)))
            Rectangle(pos=(cx - wl, cy - dp(20)), size=(wl, dp(12)))
        Color(*color)
        Ellipse(pos=(cx - dp(15), cy - dp(15)), size=(dp(30), dp(30)))
    def _timer(self, cx, cy):
        from kivy.core.text import Label as CoreLabel
        Color(0, 0, 0, 0.7)
        Rectangle(pos=(cx - dp(35), cy - dp(5)), size=(dp(70), dp(45)))
        lbl = CoreLabel(text=str(int(self.remaining_time + 0.99)), font_size=dp(36), color=(1,1,1,1))
        lbl.refresh()
        tex = lbl.texture
        Color(1, 1, 1, 1)
        Rectangle(texture=tex, pos=(cx - tex.width/2, cy + dp(2)), size=tex.size)

class PixelEditor(FloatLayout):
    def __init__(self, on_save, **kw):
        super().__init__(**kw)
        self.on_save = on_save
        self.pixels = [[None]*16 for _ in range(16)]
        self.current_color = [1, 0, 0, 1]
        self.bind(pos=self.redraw, size=self.redraw)
        pal = BoxLayout(size_hint=(1, None), height=dp(40), pos_hint={"x":0,"top":1})
        for c in ([1,0,0,1],[1,1,0,1],[0,1,0,1],[0.85,0.95,1,1],[1,0.55,0,1],[0,0,0,1],[1,1,1,1]):
            b = Button(background_color=c)
            b.bind(on_release=lambda i, c=c: setattr(self, "current_color", c))
            pal.add_widget(b)
        self.add_widget(pal)
        btns = BoxLayout(size_hint=(1, None), height=dp(44), pos_hint={"x":0,"y":0}, spacing=dp(4))
        cl = Button(text="Очистить"); cl.bind(on_release=self.clear)
        btns.add_widget(cl)
        sv = Button(text="Готово", background_color=(0.2,0.7,0.2,1))
        sv.bind(on_release=lambda *a: self.on_save(self.export()))
        btns.add_widget(sv)
        self.add_widget(btns)
        self.redraw()
    def clear(self, *a):
        self.pixels = [[None]*16 for _ in range(16)]
        self.redraw()
    def export(self):
        rows = []
        cols = []
        for y in range(16):
            row = ""
            crow = []
            for x in range(16):
                p = self.pixels[y][x]
                row += "." if p is None else "#"
                crow.append(list(p) if p else None)
            rows.append(row)
            cols.append(crow)
        return {"name":"Свой","color":[1,1,1,1],"duration":3,"pixel":rows,"pixel_colors":cols}
    def cell(self):
        return min(self.width, self.height - dp(90)) / 16
    def redraw(self, *a):
        self.canvas.clear()
        c = self.cell()
        ox = (self.width - c*16)/2
        oy = dp(44)
        with self.canvas:
            Color(0.2,0.2,0.2,1)
            Rectangle(pos=(ox-2, oy-2), size=(c*16+4, c*16+4))
            for y in range(16):
                for x in range(16):
                    p = self.pixels[y][x]
                    Color(*(p if p else [0.12,0.12,0.15,1]))
                    Rectangle(pos=(ox + x*c, oy + y*c), size=(c-1, c-1))
    def on_touch_down(self, touch):
        if touch.y < dp(44) or touch.y > self.height - dp(40):
            return False
        c = self.cell()
        ox = (self.width - c*16)/2
        gx = int((touch.x - ox) / c)
        gy = int((touch.y - dp(44)) / c)
        if 0 <= gx < 16 and 0 <= gy < 16:
            self.pixels[gy][gx] = list(self.current_color)
            self.redraw()
        return True
    def on_touch_move(self, touch):
        return self.on_touch_down(touch)

class SignalRow(BoxLayout):
    def __init__(self, sig, on_del, on_pix, **kw):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(50), spacing=dp(3), **kw)
        self.signal = sig
        self.on_pix = on_pix
        self.name_in = TextInput(text=sig.get("name","Сигнал"), multiline=False, size_hint_x=0.3)
        self.add_widget(self.name_in)
        self.color_btn = Button(size_hint_x=0.12, background_color=(sig["color"][0],sig["color"][1],sig["color"][2],1))
        self.color_btn.bind(on_release=self.pick_color)
        self.add_widget(self.color_btn)
        self.dur = TextInput(text=str(sig.get("duration",3)), multiline=False, input_filter="float", size_hint_x=0.13)
        self.add_widget(self.dur)
        self.arrow = Spinner(text=sig.get("arrow","нет"), values=("нет","left","right"), size_hint_x=0.13)
        self.add_widget(self.arrow)
        self.sem = Spinner(text=sig.get("semaphore","нет"), values=("нет","up","up_one","down"), size_hint_x=0.13)
        self.add_widget(self.sem)
        self.blink_cb = CheckBox(active=sig.get("blink",False), size_hint_x=0.08)
        self.add_widget(self.blink_cb)
        px = Button(text="🖌", size_hint_x=0.06)
        px.bind(on_release=lambda *a: self.on_pix(self))
        self.add_widget(px)
        dl = Button(text="✕", size_hint_x=0.06, background_color=(0.8,0.2,0.2,1))
        dl.bind(on_release=lambda *a: on_del(self))
        self.add_widget(dl)
    def pick_color(self, *a):
        content = BoxLayout(orientation="vertical", spacing=dp(4))
        for r in (0, 0.5, 1):
            row = BoxLayout(spacing=dp(4))
            for g in (0, 0.5, 1):
                for b in (0, 0.5, 1):
                    btn = Button(background_color=(r,g,b,1))
                    btn.bind(on_release=lambda i, r=r, g=g, b=b: self._setc(r,g,b))
                    row.add_widget(btn)
            content.add_widget(row)
        self._pop = Popup(title="Цвет", content=content, size_hint=(0.9,0.7))
        self._pop.open()
    def _setc(self, r, g, b):
        self.signal["color"] = [r,g,b,1]
        self.color_btn.background_color = (r,g,b,1)
        self._pop.dismiss()
    def apply(self):
        self.signal["name"] = self.name_in.text
        try: self.signal["duration"] = float(self.dur.text)
        except: self.signal["duration"] = 1.0
        a = self.arrow.text
        self.signal["arrow"] = None if a == "нет" else a
        s = self.sem.text
        self.signal["semaphore"] = None if s == "нет" else s
        self.signal["blink"] = self.blink_cb.active

class Root(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", padding=dp(5), spacing=dp(5), **kw)
        self.store = JsonStore("user_presets.json")
        top = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(4))
        self.preset = Spinner(text="Пресеты", values=list(PRESETS.keys()), size_hint_x=0.55)
        self.preset.bind(text=self.load)
        top.add_widget(self.preset)
        m = Button(text="Мои", size_hint_x=0.15); m.bind(on_release=self.show_user); top.add_widget(m)
        s = Button(text="💾", size_hint_x=0.15); s.bind(on_release=self.save_user); top.add_widget(s)
        self.run_btn = Button(text="▶", size_hint_x=0.15, background_color=(0.2,0.7,0.2,1))
        self.run_btn.bind(on_release=self.toggle_run); top.add_widget(self.run_btn)
        self.add_widget(top)
        self.light = LightWidget(size_hint_y=0.55)
        self.add_widget(self.light)
        tmr = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(4))
        tmr.add_widget(Label(text="Показывать таймер:", size_hint_x=0.6))
        self.timer_cb = CheckBox(active=True, size_hint_x=0.4)
        self.timer_cb.bind(active=self._tog_timer)
        tmr.add_widget(self.timer_cb)
        self.add_widget(tmr)
        self.status = Label(text="Готов", size_hint_y=None, height=dp(28))
        self.add_widget(self.status)
        ctrl = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(4))
        add = Button(text="+ сигнал"); add.bind(on_release=self.add_signal); ctrl.add_widget(add)
        clr = Button(text="Очистить"); clr.bind(on_release=lambda *a: self.set_seq([])); ctrl.add_widget(clr)
        pix = Button(text="🖌 Пиксель"); pix.bind(on_release=self.new_pixel); ctrl.add_widget(pix)
        self.add_widget(ctrl)
        sc = ScrollView()
        self.box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(3))
        self.box.bind(minimum_height=self.box.setter("height"))
        sc.add_widget(self.box)
        self.add_widget(sc)
        self.sequence = []
        self.rows = []
        self.running = False
        self.current = 0
        self.tick_ev = None
        self.remaining = 0
        self.load(None, "RU-std")
    def _tog_timer(self, cb, v):
        self.light.show_timer = v
        self.light.redraw()
    def load(self, sp, name):
        if name in PRESETS:
            self.set_seq([dict(s) for s in PRESETS[name]])
    def set_seq(self, seq):
        self.stop()
        self.sequence = seq
        self.box.clear_widgets()
        self.rows = []
        for s in seq:
            s.setdefault("color", [1,0,0,1])
            s.setdefault("duration", 3)
            r = SignalRow(s, self.del_row, self.edit_pix)
            self.rows.append(r)
            self.box.add_widget(r)
        self.light.set_sequence(self.sequence)
        self.current = 0
    def add_signal(self, *a):
        s = {"name":"Новый","color":[1,1,1,1],"duration":1}
        self.sequence.append(s)
        r = SignalRow(s, self.del_row, self.edit_pix)
        self.rows.append(r)
        self.box.add_widget(r)
        self.light.set_sequence(self.sequence)
    def del_row(self, row):
        if row in self.rows:
            self.rows.remove(row)
            self.box.remove_widget(row)
            if row.signal in self.sequence:
                self.sequence.remove(row.signal)
        self.light.set_sequence(self.sequence)
    def edit_pix(self, row):
        def save(ns):
            row.signal.update(ns)
            row.name_in.text = ns["name"]
            p.dismiss()
            self.light.redraw()
        p = Popup(title="Нарисуй", content=PixelEditor(save), size_hint=(0.95,0.9))
        p.open()
    def new_pixel(self, *a):
        def save(ns):
            self.sequence.append(ns)
            r = SignalRow(ns, self.del_row, self.edit_pix)
            self.rows.append(r)
            self.box.add_widget(r)
            self.light.set_sequence(self.sequence)
            p.dismiss()
        p = Popup(title="Новый", content=PixelEditor(save), size_hint=(0.95,0.9))
        p.open()
    def toggle_run(self, *a):
        if self.running:
            self.stop()
        else:
            self.start()
    def start(self):
        if not self.sequence:
            self.status.text = "Нет сигналов"
            return
        for r in self.rows:
            r.apply()
        self.running = True
        self.run_btn.text = "⏸"
        self.current = 0
        self._play()
    def stop(self):
        self.running = False
        self.run_btn.text = "▶"
        if self.tick_ev:
            self.tick_ev.cancel()
            self.tick_ev = None
        self.light.remaining_time = 0
        self.light.redraw()
    def _play(self):
        if not self.running or not self.sequence:
            return
        idx = self.current % len(self.sequence)
        self.light.current_index = idx
        sig = self.sequence[idx]
        dur = max(0.1, float(sig.get("duration",1)))
        self.remaining = dur
        self.light.remaining_time = dur
        self.status.text = f"{sig['name']} — {dur:.1f}с"
        self.light.redraw()
        if self.tick_ev:
            self.tick_ev.cancel()
        self.tick_ev = Clock.schedule_interval(self._tick, 0.1)
    def _tick(self, dt):
        self.remaining -= dt
        self.light.remaining_time = max(0, self.remaining)
        if self.remaining <= 0:
            self.tick_ev.cancel()
            self.current = (self.current + 1) % len(self.sequence)
            self._play()
        else:
            sig = self.sequence[self.current % len(self.sequence)]
            self.status.text = f"{sig['name']} — {self.remaining:.1f}с"
    def save_user(self, *a):
        for r in self.rows:
            r.apply()
        content = BoxLayout(orientation="vertical", spacing=dp(6))
        name = TextInput(hint_text="Название", multiline=False, size_hint_y=None, height=dp(44))
        content.add_widget(name)
        br = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        ok = Button(text="Сохранить"); cancel = Button(text="Отмена")
        br.add_widget(ok); br.add_widget(cancel)
        content.add_widget(br)
        p = Popup(title="Сохранить", content=content, size_hint=(0.85,0.4))
        def do(*a):
            n = name.text.strip() or "Без названия"
            self.store.put(n, sequence=self.sequence)
            self.status.text = f"Сохранено: {n}"
            p.dismiss()
        ok.bind(on_release=do)
        cancel.bind(on_release=lambda *a: p.dismiss())
        p.open()
    def show_user(self, *a):
        keys = list(self.store.keys())
        content = BoxLayout(orientation="vertical", spacing=dp(4))
        if not keys:
            content.add_widget(Label(text="Нет сохранённых"))
        for k in keys:
            b = Button(text=k, size_hint_y=None, height=dp(44))
            b.bind(on_release=lambda i, k=k: self._load_user(k))
            content.add_widget(b)
        self._up = Popup(title="Мои", content=content, size_hint=(0.85,0.7))
        self._up.open()
    def _load_user(self, key):
        d = self.store.get(key)
        self.set_seq([dict(s) for s in d["sequence"]])
        self._up.dismiss()

class TrafficApp(App):
    def build(self):
        self.title = "Светофоры мира"
        return Root()

TrafficApp().run()
