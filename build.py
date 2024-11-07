from datetime import datetime
from glob import glob
import os

from jinja2 import Environment, FileSystemLoader, Template
from markdown import Markdown


this_path = os.path.dirname(os.path.abspath(__file__))
template_path: str = os.path.join(this_path, "assets", "templates")
environment: Environment = Environment(
    loader=FileSystemLoader(template_path)
)

article: Template = environment.get_template(name="article.html")
articles: Template = environment.get_template(name="articles.html")
e404: Template = environment.get_template(name="404.html")

md = Markdown(
    extensions=["meta", "toc", "fenced_code", "sane_lists", "tables"]
)
md_paths = glob(pathname=os.path.join(this_path, "markdowns", "*.md"))

article_links: list[tuple[str, str]] = []
for path in md_paths:
    with open(file=path, mode="r", encoding="utf-8") as f:
        html: str = md.reset().convert(f.read())

    meta = md.Meta
    if "title" not in meta:
        print(
            f"WARNING: Skipping {path}, as it doesn't have title (meta)."
        )
        continue

    title: str = meta["title"][-1]
    md_name: str = os.path.basename(path)[:-3]
    md_last_modified_time: str = datetime.fromtimestamp(
        os.path.getmtime(path)
    ).strftime("%Y-%m-%d")

    html_path: str = (
        os.path.join(this_path, "articles", f"{md_name}.html")
        if md_name != "index"
        else os.path.join(this_path, "index.html")
    )
    html_datas: dict[str, str] = {"title": title, "content": html}

    if md_name != "index":
        html_datas["mtime"] = md_last_modified_time

    with open(file=html_path, mode="w", encoding="utf-8") as f:
        f.write(article.render(html_datas))
        print(f"INFO: Wrote {html_path}.")

    if md_name == "index":
        continue

    article_link: str = f"/articles/{md_name}.html"
    article_links.append((title, article_link))

articles_path: str = os.path.join(this_path, "articles.html")
articles_data: dict[str, str] = {"articles": article_links}
with open(file=articles_path, mode="w", encoding="utf-8") as f:
    f.write(articles.render(articles_data))
    print(f"INFO: Wrote {articles_path}.")

e404_path: str = os.path.join(this_path, "404.html")
with open(file=e404_path, mode="w", encoding="utf-8") as f:
    f.write(e404.render())
    print(f"INFO: Wrote {e404_path}.")
