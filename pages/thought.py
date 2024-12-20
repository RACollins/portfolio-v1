from fasthtml.common import *
from components import TopBar
import yaml
import datetime
from markdown import markdown
import re

# Ensure the extensions are correctly specified and add proper styling
md_exts = ["extra", "codehilite", "nl2br", "smarty", "sane_lists"]


def Markdown(s, exts=md_exts, **kw):
    default_cls = "prose max-w-3xl prose-headings:text-darkblue-800 dark:prose-headings:text-gray-200 prose-p:text-darkblue-800 dark:prose-p:text-gray-200"
    if "cls" in kw:
        kw["cls"] = f"{default_cls} {kw['cls']}"
    else:
        kw["cls"] = default_cls

    # Convert markdown to HTML
    html = markdown(s, extensions=exts)

    # Transform code blocks to match HighlightJS structure
    html = re.sub(
        r'<div class="codehilite"><pre><span></span><code>',
        '<div class="codehilite"><pre><code class="hljs language-python">',
        html
    )

    # If there's already a language specified, ensure it's python
    html = re.sub(
        r'<div class="codehilite"><pre><span></span><code[^>]*class="[^"]*"',
        '<div class="codehilite"><pre><code class="hljs language-python"',
        html
    )

    return Div(NotStr(html), **kw)


def ThoughtPage(slug: str):
    with open(f"thoughts/{slug}.md", "r") as file:
        content = file.read()
        header_info, thought_body = content.split("---")[1:]

        ### Populate thought with metadata
        thought = yaml.safe_load(header_info)
        thought["body"] = thought_body.strip()

        ### Convert date string to datetime object if it exists
        if "date" in thought and isinstance(thought["date"], str):
            thought["date"] = datetime.datetime.strptime(thought["date"], "%Y-%m-%d")

    return Div(
        TopBar(),
        Main(
            H2(
                thought["title"],
                cls="max-w-3xl mx-auto px-4 mb-4 text-3xl font-bold text-darkblue-800 dark:text-gray-200",
            ),
            Div(
                Div(
                    "Author: Richard Collins",
                ),
                Div(
                    "Published: {}".format(thought["date"].strftime("%d %b %Y")),
                ),
                cls="max-w-3xl mx-auto px-4 mb-4 italic text-sm text-darkblue-600 dark:text-gray-400",
            ),
            Markdown(
                thought["body"],
                cls="max-w-3xl mx-auto px-4 mb-4 text-darkblue-800 dark:text-gray-200",
            ),
            cls="py-8",
        ),
        cls="min-h-screen bg-[radial-gradient(ellipse_at_top_left,_#fff0d1_0%,_#ffffff_60%,_#cce6ff_100%)] dark:bg-[radial-gradient(ellipse_at_top_left,_#003196_0%,_#000000_60%,_#6a3400_100%)]",
    )


### May need this code in future
# Add copy button to codehilite blocks
# html = html.replace(
#     '<div class="codehilite">',
#     """<div class="codehilite relative group">
#         <button onclick="copyCode(this)"
#                 class="absolute top-2 right-2 p-1.5 rounded bg-darkblue-800 text-white
#                        opacity-0 group-hover:opacity-100 hover:bg-darkblue-400 transition-all duration-200">
#             <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
#                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
#                 <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
#                 <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
#                 <path d="M12 11v6"/>
#                 <path d="M9 14h6"/>
#             </svg>
#         </button>""",
#     )
