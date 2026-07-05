import os
import paraby as pb

fixtures = {
    "fixture1_basic": """window(
    title: Hello
    btn(
        text: click
        click:
            print("clicked")
    )
)""",
    "fixture2_loop": """window(
    loop(user in users) (
        btn(
            text: {user.name}
            click:
                print("click " + this.text)
        )
    )
)""",
    "fixture3_complex": """window(
    title: complex
    color: red
    my_frame = frame(
        my_btn = btn(text: ok, click: print(this))
    )
    my_entry = entry(
        change: print("changed")
    )
    if my_frame.click:
        pass
)""",
    "fixture4_implicit_event": """window(
    has_loop: true
    loop(i in items) (
        btn(
            click_me:
                print(this)
        )
    )
)""",
    "fixture5_root_event": """window(
    size: 500, 500
    my_lbl = label(text: test)
    click:
        print("window clicked")
)"""
}

all_match = True
for name, pui_code in fixtures.items():
    new_code = pb.transpile_pb(pui_code)
    with open(f"baselines/{name}.py", "r", encoding="utf-8") as f:
        old_code = f.read()
    if new_code != old_code:
        print(f"Mismatch in {name}!")
        all_match = False
        import difflib
        diff = difflib.unified_diff(old_code.splitlines(), new_code.splitlines(), fromfile='old', tofile='new')
        print('\n'.join(diff))

if all_match:
    print("All baselines match byte-by-byte!")
else:
    import sys
    sys.exit("Some baselines did not match!")
