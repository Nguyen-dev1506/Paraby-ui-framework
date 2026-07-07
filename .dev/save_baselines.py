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

os.makedirs(".dev/baselines", exist_ok=True)
for name, pui_code in fixtures.items():
    python_code = pb.transpile_pb(pui_code)
    with open(f".dev/baselines/{name}.py", "w", encoding="utf-8") as f:
        f.write(python_code)
print("Baselines saved to .dev/baselines/")
