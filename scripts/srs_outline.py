"""CI-only reader to show SRS headings and requirement sections for manual traceability.

Does not change or publish the PDF. Repo SRS is already public. Truncates
the job log to prevent overly large outputs.
"""
from pathlib import Path
import re
from pypdf import PdfReader

source = Path("SRS_Project_ID_22.pdf")
reader = PdfReader(str(source))
budget = 42000
pattern = re.compile(r"functional|non.functional|requirement|use.case|constraint|performance|security|architecture|role|user.story|recommendation|learning|resource|progress|dashboard|course|certification|FR-|NFR-", re.I)
print("SRS pages:", len(reader.pages))
for number, page in enumerate(reader.pages, 1):
    raw = page.extract_text() or ""
    lines = [re.sub(r"\s+", " ", line).strip() for line in raw.splitlines()]
    lines = [line for line in lines if line]
    selected = pattern.search(raw) is not None or 9 <= number <= 13
    if not selected:
        continue
    chunk = "\n".join(lines)
    excerpt = chunk[:6500]
    if len(excerpt) > budget:
        excerpt = excerpt[:budget]
    print("\n==== SRS PAGE", number, "====\n", excerpt)
    budget -= len(excerpt)
    if budget <= 0:
        break
