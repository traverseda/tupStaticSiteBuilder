#!/usr/bin/env python3
import sys, markdown
from markdown.extensions.toc import TocExtension

from collections import ChainMap

from jinja2 import Environment, FileSystemLoader, BaseLoader


def main(rootdir,infile,outfile):
    text=infile.read_text()
    defaults = {
        'STATIC_ROOT':rootdir,
        'infile':infile,
        'relpath':outfile.resolve().relative_to(rootdir.resolve()),
        'outfile':outfile,
        'title':[outfile.name,],
    }
    toc = TocExtension(
        baselevel=2,
        permalink=True,
        slugify=lambda orig, seperator: "".join((str(defaults['relpath']),seperator,orig))
    )

    extensions = ['markdown.extensions.meta',toc]
    md = markdown.Markdown(extensions = extensions)
    j2_env = Environment(loader=FileSystemLoader(str(rootdir/'./templates')),
    trim_blocks=True)
    html = md.convert(text)
    meta = md.Meta
    if hasattr(md, "Meta") and 'extensions' in md.Meta:
        md = markdown.Markdown(extensions = extensions+md.Meta.extensions)
        html = md.convert(text)
    html = "{% extends 'base.html' %}{% block content %}"+html+"{% endblock content %}"
    template_vars = ChainMap(meta,defaults)
    outfile.write_text(j2_env.from_string(html).render(**template_vars))

from pathlib import Path
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Command expects three arguments, <rootdir> <infile> <outfile>")
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
