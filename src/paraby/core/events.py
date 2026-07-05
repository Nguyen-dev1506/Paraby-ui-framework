def bind_event(widget, event_name, callback):
    """
    Binds an event handler (callback) to a widget.
    """
    evt = event_name.strip().lower()
    w_class = widget.__class__.__name__
    
    if evt in ("click_me", "click"):
        if w_class in ("CTkButton", "CTkCheckBox", "CTkSwitch"):
            widget.configure(command=callback)
        else:
            widget.bind("<Button-1>", lambda event: callback())
            
    elif evt in ("press_enter", "submit"):
        widget.bind("<Return>", lambda event: callback())
        
    elif evt in ("change", "slide", "value_change", "select"):
        if w_class in ("CTkSlider", "CTkComboBox", "CTkCheckBox", "CTkSwitch"):
            import inspect
            sig = inspect.signature(callback)
            if len(sig.parameters) > 0:
                widget.configure(command=callback)
            else:
                widget.configure(command=lambda value: callback())
        else:
            widget.bind("<Configure>", lambda event: callback())
            
    else:
        widget.bind(event_name, lambda event: callback())
