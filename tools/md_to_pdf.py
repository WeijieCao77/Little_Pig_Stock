#!/usr/bin/env python3
"""
Markdown -> PDF with Chinese font support (xhtml2pdf + Takao Gothic for CJK).
Usage: python3 tools/md_to_pdf.py <input.md> <output.pdf>
"""
import sys
import os
import re
import markdown
from xhtml2pdf import pisa

# WenQuanYi Zen Hei has full Simplified + Traditional Chinese coverage.
# xhtml2pdf handles this TTC fine via @font-face.
CN_FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
assert os.path.exists(CN_FONT_PATH), f"CJK font not found at {CN_FONT_PATH}"

CSS = f"""
@font-face {{
    font-family: 'cjk';
    src: url('{CN_FONT_PATH}');
}}
@page {{
    size: A4;
    margin: 1.6cm 1.4cm 1.6cm 1.4cm;
    @frame footer_frame {{
        -pdf-frame-content: footer_content;
        left: 1.4cm; width: 18.2cm;
        bottom: 0.7cm; height: 0.8cm;
    }}
}}
body {{ font-family: cjk; font-size: 9.5pt; line-height: 1.5; color: #1a1a1a; }}
h1  {{ font-family: cjk; font-size: 18pt; font-weight: bold; color: #0d3a66;
       border-bottom: 2px solid #0d3a66;
       padding-bottom: 4pt; margin-top: 6pt; margin-bottom: 12pt; }}
h2  {{ font-family: cjk; font-size: 14pt; font-weight: bold; color: #0d3a66;
       border-bottom: 1px solid #c0d0e0;
       padding-bottom: 2pt; margin-top: 18pt; margin-bottom: 8pt; }}
h3  {{ font-family: cjk; font-size: 12pt; font-weight: bold; color: #1c5294;
       margin-top: 12pt; margin-bottom: 6pt; }}
h4  {{ font-family: cjk; font-size: 10.5pt; font-weight: bold; color: #444;
       margin-top: 8pt; margin-bottom: 4pt; }}
p   {{ font-family: cjk; margin-top: 0; margin-bottom: 6pt; }}
strong {{ font-family: cjk; color: #b22222; }}
em  {{ font-family: cjk; color: #555; }}
hr  {{ border: 0; border-top: 1px dashed #999; margin: 10pt 0; }}
ul, ol {{ margin-top: 2pt; margin-bottom: 6pt; padding-left: 16pt; }}
li  {{ font-family: cjk; margin-bottom: 2pt; }}
code {{ font-family: Courier; font-size: 9pt; background: #f0f0f0; padding: 1pt 2pt; }}
pre  {{ font-family: Courier; font-size: 8.5pt; background: #f6f8fa; padding: 6pt;
        border-left: 3px solid #c0c0c0; margin: 6pt 0; }}
blockquote {{ font-family: cjk; color: #555; border-left: 3px solid #c0c0c0;
              padding: 4pt 8pt; margin: 6pt 0; background: #fafafa; }}
table {{ border-collapse: collapse; width: 100%; margin: 6pt 0; }}
th    {{ font-family: cjk; background: #e8eef5; color: #0d3a66; font-weight: bold;
         border: 1px solid #b0c0d0; padding: 4pt 6pt; font-size: 9pt; text-align: left; }}
td    {{ font-family: cjk; border: 1px solid #d0d0d0; padding: 4pt 6pt;
         font-size: 9pt; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f8f9fc; }}
.footer {{ font-family: cjk; font-size: 8pt; color: #999; text-align: center; }}
"""

FOOTER_HTML = """
<div id="footer_content" class="footer">
  Little Pig Stock · 内部研究底稿 · 教育性, 非投资建议 · 第 <pdf:pagenumber/> 页 / 共 <pdf:pagecount/> 页
</div>
"""

def md_to_html(md_text):
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
        output_format="xhtml",
    )

def build_doc(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    body = md_to_html(md_text)
    # strip emoji that xhtml2pdf doesn't render
    body = re.sub(r"[✅❌⚠️\U0001F534\U0001F7E1\U0001F7E2]", "", body)
    html = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<style>{CSS}</style></head><body>{body}{FOOTER_HTML}</body></html>'
    )
    return html

def main():
    if len(sys.argv) != 3:
        print("Usage: md_to_pdf.py <input.md> <output.pdf>", file=sys.stderr)
        sys.exit(2)
    in_path, out_path = sys.argv[1], sys.argv[2]
    html = build_doc(in_path)
    with open(out_path, "wb") as outf:
        result = pisa.CreatePDF(html, dest=outf, encoding="utf-8")
    if result.err:
        print(f"PDF generation FAILED with {result.err} error(s)", file=sys.stderr)
        sys.exit(1)
    print(f"OK: wrote {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    main()
