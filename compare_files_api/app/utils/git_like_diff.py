import difflib
from html import escape
from app.db.models import File

def git_like_diff(file1: File, file2: File, text1: str, text2: str):
    """
    GitHub-style optimized 2-column diff:
    - file1: old file
    - file2: new file
    - text1/text2: decoded content
    """

    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    diff = list(difflib.ndiff(lines1, lines2))

    html = f"""
    <html>
    <head>
    <style>
        body {{ font-family: monospace; }}
        .diff-table {{ border-collapse: collapse; width: 100%; display: block; overflow-x: auto; white-space: nowrap; }}
        td, th {{ vertical-align: top; padding: 2px 5px; white-space: pre; }}
        th {{ background-color: #f6f8fa; position: sticky; top: 0; }}
        .line-num {{ width: 40px; text-align: right; position: sticky; left: 0; background-color: #f6f8fa; }}
        .line-num-added {{ background-color: #aceebb; }}
        .line-num-removed {{ background-color: #ffcecb; }}
        .added {{ background-color: #e6ffed; }}
        .removed {{ background-color: #ffeef0; }}
        .unchanged:nth-child(even) {{ background-color: #f3f3f3; }}
        .unchanged:nth-child(odd) {{ background-color: #f8f8f8; }}
    </style>
    </head>
    <body>
    <h3>Diff: {escape(file1.filename)} → {escape(file2.filename)}</h3>
    <table class="diff-table" border="1">
    <tr>
        <th colspan="2">{escape(file1.filename)}<br>Type: {file1.filetype}</th>
        <th colspan="2">{escape(file2.filename)}<br>Type: {file2.filetype}</th>
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
            html += f"<tr><td class='line-num line-num-removed'>{old_num}</td><td class='removed'>{text}</td>" \
                    f"<td class='line-num'></td><td></td></tr>"
            old_num += 1
        elif line.startswith("+ "):
            html += f"<tr><td class='line-num'></td><td></td>" \
                    f"<td class='line-num line-num-added'>{new_num}</td><td class='added'>{text}</td></tr>"
            new_num += 1
        elif line.startswith("? "):
            continue

    html += "</table></body></html>"
    return html
