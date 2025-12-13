import difflib
from .git_like_diff import git_like_diff

def generate_diff_html_old(content1: str, content2: str, name1: str, name2: str):
    lines1 = content1.splitlines()
    lines2 = content2.splitlines()
    return difflib.HtmlDiff().make_file(lines1, lines2, name1, name2)


def generate_diff_html(content1, content2, name1="Old", name2="New"):
    return git_like_diff(content1, content2, name1, name2)
