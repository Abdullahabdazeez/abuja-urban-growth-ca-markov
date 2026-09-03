from pathlib import Path
import markdown
from weasyprint import HTML

ROOT = Path('.')
source = ROOT / 'docs' / 'PROJECT_REPORT.md'
out = ROOT / 'reports' / 'Abuja_Urban_Growth_Portfolio_Report.pdf'
out.parent.mkdir(parents=True, exist_ok=True)

body = markdown.markdown(source.read_text(encoding='utf-8'), extensions=['tables'])
css = '''
@page { size: A4; margin: 18mm; }
body { font-family: Arial, sans-serif; color: #243447; font-size: 10.5pt; line-height: 1.45; }
h1 { font-size: 22pt; margin-bottom: 8pt; color: #1f2937; }
h2 { font-size: 15pt; margin-top: 18pt; color: #1f2937; }
h3 { font-size: 12pt; margin-top: 14pt; }
table { border-collapse: collapse; width: 100%; margin: 10pt 0 16pt; font-size: 9.5pt; }
th, td { border: 1px solid #d7dde3; padding: 6pt; text-align: left; }
th { background: #eef2f5; }
strong { color: #1f2937; }
'''
html = f'<html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
HTML(string=html, base_url=str(ROOT.resolve())).write_pdf(out)
print(out)
