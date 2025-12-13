import difflib
from html import escape

def git_like_diff(content1: str, content2: str, name1="Old", name2="New"):

    lines1 = content1.splitlines()
    lines2 = content2.splitlines()

    diff = list(difflib.ndiff(lines1, lines2))

    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: monospace; }}
        table {{ border-collapse: collapse; width: 100%; }}
        td, th {{ vertical-align: top; padding: 2px 5px; white-space: pre; font-family: monospace; }}
        th {{ background-color: #f6f8fa; }}
        .line-num {{ width: 40px; text-align: right; color: #999; }}
        .added {{ background-color: #e6ffed; }}
        .removed {{ background-color: #ffeef0; }}
        .unchanged {{ background-color: #f8f8f8; }}
    </style>
    </head>
    <body>
    <h3>Diff: {name1} → {name2}</h3>
    <table border="1">
    <tr>
        <th>#</th><th>{name1}</th>
        <th>#</th><th>{name2}</th>
    </tr>
    """

    old_num = 1
    new_num = 1

    for line in diff:
        text = escape(line[2:])
        if line.startswith("  "):
            html += f"<tr><td class='line-num'>{old_num}</td><td class='unchanged'>{text}</td>" \
                    f"<td class='line-num'>{new_num}</td><td class='unchanged'>{text}</td></tr>"
            old_num += 1
            new_num += 1
        elif line.startswith("- "):
            html += f"<tr><td class='line-num'>{old_num}</td><td class='removed'>- {text}</td>" \
                    f"<td class='line-num'></td><td></td></tr>"
            old_num += 1
        elif line.startswith("+ "):
            html += f"<tr><td class='line-num'></td><td></td>" \
                    f"<td class='line-num'>{new_num}</td><td class='added'>+ {text}</td></tr>"
            new_num += 1
        elif line.startswith("? "):
            continue

    html += "</table></body></html>"

    return html
