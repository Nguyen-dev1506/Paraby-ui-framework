class btn:
    text: str
    click: bool
    click_me: bool

class button(btn): pass

class label:
    text: str

class text(label): pass
class lable(label): pass
class txt(label): pass

class entry:
    text: str
    submit: bool
    press_enter: bool

class checkbox:
    text: str
    click: bool
    change: bool

class tick(checkbox): pass

class switch:
    text: str
    click: bool
    change: bool

class slider:
    change: bool

class thanh_keo(slider): pass
class nut_gat(switch): pass

class combobox:
    change: bool
    select: bool
    
class dropdown(combobox): pass
class select(combobox): pass

class progress:
    value: float
    
class loading(progress): pass
class thanh_tien_do(progress): pass

class image:
    path: str
class img(image): pass
class anh(image): pass

class frame: pass
class hop(frame): pass

class text_box:
    text: str

class textbox(text_box): pass
class khung_chu(text_box): pass

class window: pass
