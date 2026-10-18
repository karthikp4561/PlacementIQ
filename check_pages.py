# check_pages.py
import docx

doc = docx.Document(r'c:\Users\karth\Downloads\siip\project\PlacementIQ_SIIP_Report.docx')

breaks = 0
for p in doc.paragraphs:
    for r in p.runs:
        if 'w:br' in r._r.xml and 'type="page"' in r._r.xml:
            breaks += 1

sec_count = len(doc.sections)
total_pages = breaks + (sec_count - 1) + 1
print(f"Total sections: {sec_count}")
print(f"Explicit page breaks: {breaks}")
print(f"Section breaks (new pages): {sec_count - 1}")
print(f"Total physical pages in Word: {total_pages}")
