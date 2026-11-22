# aprameyacv.site

Personal site: a single page plus one page per project, and the full technical
reports copied in under `/reports`.

## Structure

```
index.html              home
work/<slug>.html        one page per project
reports/<slug>/         full reports, generated from the project repos
assets/site.css         all styles
assets/site.js          scroll reveal
build.py                regenerates index.html and work/*.html
```

`build.py` holds the project copy and numbers in one place. Edit it, run
`python3 build.py`, and the pages are rewritten. The report folders are copies:
update them from their source repos, not here.

## Run locally

```bash
python3 -m http.server 8099
```

