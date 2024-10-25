import os
from glob import glob
from datetime import datetime

from markdown import Markdown
from jinja2 import Environment, FileSystemLoader


template_path = "./assets/templates"
environment = Environment(loader = FileSystemLoader(template_path))

article = environment.get_template("article.html")
articles = environment.get_template("articles.html")
e404 = environment.get_template("404.html")


md = Markdown(
    extensions = [
        "meta",
        "toc",
        "fenced_code",
        "sane_lists",
        "tables"
    ]
)
md_paths = glob("./markdowns/*.md")

article_links = []
for path in md_paths:
    with open(path, "r", encoding = "utf-8") as f:
        html = md.reset().convert(f.read())

    meta = md.Meta
    if "title" not in meta:
        print(f"WARNING: Skipping {path}, because it does not contain title.")
        continue

    title = meta["title"][-1]
    md_name = os.path.basename(path)[:-3]
    md_last_mtime = (
        datetime
        .fromtimestamp(os.path.getmtime(path))
        .strftime("%Y-%m-%d")
    )
    html_path = (
        f"./articles/{md_name}.html"
        if md_name != "index"
        else "./index.html"
    )
    html_datas = {
        "title": title,
        "content": html
    }

    if md_name != "index":
        html_datas["mtime"] = md_last_mtime

    with open(html_path, "w", encoding = "utf-8") as f:
        f.write(article.render(html_datas))
        print(f"INFO: Output {html_path}.")

    if md_name == "index":
        continue

    article_links.append((title, html_path[1:]))


articles_path = "./articles.html"
articles_data = {
    "articles": article_links
}
with open(articles_path, "w", encoding = "utf-8") as f:
    f.write(articles.render(articles_data))
    print(f"INFO: Output {articles_path}.")


e404_path = "./404.html"
with open(e404_path, "w", encoding = "utf-8") as f:
    f.write(e404.render())
    print(f"INFO: Output {e404_path}.")
