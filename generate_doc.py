import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_page_number_to_paragraph(p):
    run = p.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_body_p(doc, text, bold_prefix="", line_spacing=1.5, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_p(doc, bold_lead, text):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(4)
    r_lead = p.add_run(bold_lead)
    r_lead.font.name = 'Times New Roman'
    r_lead.font.size = Pt(11.5)
    r_lead.font.bold = True
    r_lead.font.color.rgb = RGBColor(0, 0, 0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11.5)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_code_block(doc, code_str, title=""):
    if title:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(6)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.keep_with_next = True
        r_t = p_t.add_run(f"Listing: {title}")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.italic = True
        r_t.font.color.rgb = RGBColor(30, 58, 138)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.2)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:left w:val="single" w:sz="16" w:space="0" w:color="2563EB"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_str)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_image_figure(doc, img_path, caption, width_in=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        r_img = p_img.add_run()
        r_img.add_picture(img_path, width=Inches(width_in))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.bold = True
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(30, 41, 59)

def generate_report():
    doc = Document()

    # Section 1: Preliminary Pages
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(1.0)
    sec1.left_margin = Inches(1.25)
    sec1.right_margin = Inches(1.0)
    sec1.different_first_page_header_footer = True

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # ---------------------------------------------------------------------------
    # PAGE 1: TITLE PAGE
    # ---------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(16)
    r_t = p_title.add_run("CLAIMCHECK: REAL-TIME FACT-CHECKING WEB APPLICATION")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(16)
    r_t.font.bold = True

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(12)
    p_rep.paragraph_format.space_after = Pt(16)
    r_rep = p_rep.add_run("A PROJECT REPORT")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(14)
    r_rep.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("Submitted by")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True

    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(2)
    p_name.paragraph_format.space_after = Pt(16)
    r_name = p_name.add_run("Jai Vignesh Y (310624148039)")
    r_name.font.name = 'Times New Roman'
    r_name.font.size = Pt(13)
    r_name.font.bold = True

    p_part = doc.add_paragraph()
    p_part.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_part.paragraph_format.space_before = Pt(6)
    p_part.paragraph_format.space_after = Pt(4)
    r_part = p_part.add_run("in partial fulfillment for the award of the Degree\nof")
    r_part.font.name = 'Times New Roman'
    r_part.font.size = Pt(12)
    r_part.font.italic = True

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(2)
    p_deg.paragraph_format.space_after = Pt(2)
    r_deg = p_deg.add_run("BACHELOR OF ENGINEERING")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(13)
    r_deg.font.bold = True

    p_in = doc.add_paragraph()
    p_in.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in.paragraph_format.space_before = Pt(2)
    p_in.paragraph_format.space_after = Pt(2)
    r_in = p_in.add_run("in")
    r_in.font.name = 'Times New Roman'
    r_in.font.size = Pt(12)
    r_in.font.italic = True

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(2)
    p_dept.paragraph_format.space_after = Pt(16)
    r_dept = p_dept.add_run("CSE (AIML)")
    r_dept.font.name = 'Times New Roman'
    r_dept.font.size = Pt(13)
    r_dept.font.bold = True

    # Logo
    if os.path.exists("extracted_img_p1_0.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(10)
        r_logo = p_logo.add_run()
        r_logo.add_picture("extracted_img_p1_0.png", width=Inches(1.4))

    p_col = doc.add_paragraph()
    p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_col.paragraph_format.line_spacing = 1.2
    p_col.paragraph_format.space_before = Pt(6)
    p_col.paragraph_format.space_after = Pt(12)
    r_c1 = p_col.add_run("EASWARI ENGINEERING COLLEGE,\n")
    r_c1.font.name = 'Times New Roman'
    r_c1.font.size = Pt(13)
    r_c1.font.bold = True

    r_c2 = p_col.add_run("(AN AUTONOMOUS INSTITUTION) - AFFILIATED TO ANNA UNIVERSITY,\nCHENNAI\n")
    r_c2.font.name = 'Times New Roman'
    r_c2.font.size = Pt(11)
    r_c2.font.bold = True

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_before = Pt(10)
    p_date.paragraph_format.space_after = Pt(0)
    r_d = p_date.add_run("NOVEMBER 2026")
    r_d.font.name = 'Times New Roman'
    r_d.font.size = Pt(13)
    r_d.font.bold = True

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # PAGE 2: BONAFIDE CERTIFICATE
    # ---------------------------------------------------------------------------
    if os.path.exists("extracted_img_p1_0.png"):
        p_blogo = doc.add_paragraph()
        p_blogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_blogo.paragraph_format.space_before = Pt(0)
        p_blogo.paragraph_format.space_after = Pt(6)
        r_bl = p_blogo.add_run()
        r_bl.add_picture("extracted_img_p1_0.png", width=Inches(1.15))

    p_bcol = doc.add_paragraph()
    p_bcol.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bcol.paragraph_format.line_spacing = 1.2
    p_bcol.paragraph_format.space_after = Pt(16)
    r_bc = p_bcol.add_run("EASWARI ENGINEERING COLLEGE\n")
    r_bc.font.name = 'Times New Roman'
    r_bc.font.size = Pt(14)
    r_bc.font.bold = True
    r_bc_sub = p_bcol.add_run("(An Autonomous Institution - Affiliated to Anna University, Chennai)\nDEPARTMENT OF CSE (AIML)")
    r_bc_sub.font.name = 'Times New Roman'
    r_bc_sub.font.size = Pt(11)
    r_bc_sub.font.bold = True

    p_bonatitle = doc.add_paragraph()
    p_bonatitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bonatitle.paragraph_format.space_before = Pt(8)
    p_bonatitle.paragraph_format.space_after = Pt(24)
    r_bt = p_bonatitle.add_run("BONAFIDE CERTIFICATE")
    r_bt.font.name = 'Times New Roman'
    r_bt.font.size = Pt(14)
    r_bt.font.bold = True
    r_bt.font.underline = True

    p_bonatext = doc.add_paragraph()
    p_bonatext.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_bonatext.paragraph_format.line_spacing = 1.5
    p_bonatext.paragraph_format.space_after = Pt(70)
    p_bonatext.add_run("Certified that this mini project report titled ")
    r_bx2 = p_bonatext.add_run('"CLAIMCHECK: REAL-TIME FACT-CHECKING WEB APPLICATION"')
    r_bx2.font.bold = True
    p_bonatext.add_run(" is the Bonafide work of ")
    r_bx4 = p_bonatext.add_run('"Jai Vignesh Y (310624148039)"')
    r_bx4.font.bold = True
    p_bonatext.add_run(", who carried out the project work under my supervision.")

    # Signature Table (borderless)
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False

    cell_hod = tbl_sig.cell(0, 0)
    cell_hod.width = Inches(3.2)
    p_h = cell_hod.paragraphs[0]
    p_h.paragraph_format.line_spacing = 1.25
    p_h.add_run("Dr. Justin Dhas Y\n").font.bold = True
    p_h.add_run("HEAD OF THE DEPARTMENT\n").font.bold = True
    p_h.add_run("Department of CSE (AIML)\nEaswari Engineering College\nRamapuram, Chennai - 600 089")

    cell_sup = tbl_sig.cell(0, 1)
    cell_sup.width = Inches(3.2)
    p_s = cell_sup.paragraphs[0]
    p_s.paragraph_format.line_spacing = 1.25
    p_s.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_s.add_run("Ms. Divyanjali\n").font.bold = True
    p_s.add_run("SUPERVISOR\n").font.bold = True
    p_s.add_run("Assistant Professor\nDepartment of CSE (AIML)\nEaswari Engineering College\nRamapuram, Chennai - 600 089")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # PAGE 3: CERTIFICATE OF VIVA-VOCE-EXAMINATION
    # ---------------------------------------------------------------------------
    if os.path.exists("extracted_img_p1_0.png"):
        p_vlogo = doc.add_paragraph()
        p_vlogo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_vlogo.paragraph_format.space_before = Pt(0)
        p_vlogo.paragraph_format.space_after = Pt(6)
        r_vl = p_vlogo.add_run()
        r_vl.add_picture("extracted_img_p1_0.png", width=Inches(1.15))

    p_vcol = doc.add_paragraph()
    p_vcol.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_vcol.paragraph_format.line_spacing = 1.2
    p_vcol.paragraph_format.space_after = Pt(16)
    r_vc = p_vcol.add_run("EASWARI ENGINEERING COLLEGE\n")
    r_vc.font.name = 'Times New Roman'
    r_vc.font.size = Pt(14)
    r_vc.font.bold = True
    r_vc_sub = p_vcol.add_run("(An Autonomous Institution - Affiliated to Anna University, Chennai)\nDEPARTMENT OF CSE (AIML)")
    r_vc_sub.font.name = 'Times New Roman'
    r_vc_sub.font.size = Pt(11)
    r_vc_sub.font.bold = True

    p_vivatitle = doc.add_paragraph()
    p_vivatitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_vivatitle.paragraph_format.space_before = Pt(8)
    p_vivatitle.paragraph_format.space_after = Pt(24)
    r_vt = p_vivatitle.add_run("Certificate of Viva-voce-Examination")
    r_vt.font.name = 'Times New Roman'
    r_vt.font.size = Pt(14)
    r_vt.font.bold = True
    r_vt.font.underline = True

    p_vivatext = doc.add_paragraph()
    p_vivatext.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_vivatext.paragraph_format.line_spacing = 1.5
    p_vivatext.paragraph_format.space_after = Pt(50)
    p_vivatext.add_run("This is to certify that the Viva Voce Examination of the Project Work entitled ")
    r_vt_bold = p_vivatext.add_run('"CLAIMCHECK: REAL-TIME FACT-CHECKING WEB APPLICATION"')
    r_vt_bold.font.bold = True
    p_vivatext.add_run(" submitted by ")
    r_vname_bold = p_vivatext.add_run("Mr. Jai Vignesh Y (Reg. No. 310624148039)")
    r_vname_bold.font.bold = True
    p_vivatext.add_run(" in partial fulfillment of the requirements for the award of the degree of ")
    r_vdeg_bold = p_vivatext.add_run("Bachelor of Engineering in CSE (AIML)")
    r_vdeg_bold.font.bold = True
    p_vivatext.add_run(" was conducted on ____________ (Date) in the Department of CSE (AIML), Easwari Engineering College, Ramapuram - Chennai.")

    # Examiner Table
    tbl_exam = doc.add_table(rows=1, cols=2)
    tbl_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_exam.autofit = False

    cell_int = tbl_exam.cell(0, 0)
    cell_int.width = Inches(3.2)
    p_i = cell_int.paragraphs[0]
    p_i.paragraph_format.line_spacing = 1.3
    p_i.add_run("Internal Examiner\n\n").font.bold = True
    p_i.add_run("Name : _________________________\n")
    p_i.add_run("Designation: ____________________\n")
    p_i.add_run("Address : ______________________\n\n")

    cell_ext = tbl_exam.cell(0, 1)
    cell_ext.width = Inches(3.2)
    p_e = cell_ext.paragraphs[0]
    p_e.paragraph_format.line_spacing = 1.3
    p_e.add_run("External Examiner\n\n").font.bold = True
    p_e.add_run("Name : _________________________\n")
    p_e.add_run("Designation : ___________________\n")
    p_e.add_run("Address : ______________________\n\n")

    p_vdate = doc.add_paragraph()
    p_vdate.paragraph_format.space_before = Pt(20)
    p_vdate.add_run("Date: ____________________").font.bold = True

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # PAGE 4: ABSTRACT (Formatted strictly to fit exactly on Page 4)
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "ABSTRACT")

    add_body_p(doc, "In today's interconnected digital communication ecosystem, the exponential proliferation of unverified claims, deceptively manipulated headlines, and viral rumors across messaging platforms presents a serious threat to public information integrity, civic discourse, and decision-making. Conventional automated approaches frequently fall short: pure Large Language Model (LLM) generation suffers from training knowledge cutoff dates and stochastic hallucinations, while traditional search engines require laborious manual cross-checking and high human cognitive burden. To address these critical challenges, this project presents ClaimCheck, an evidence-grounded, real-time automated fact-checking web application engineered using the full MERN technology stack (MongoDB, Express.js, React.js, Node.js) seamlessly coupled with Google Gemini API and SerpApi.",
               line_spacing=1.2, space_after=4)

    add_body_p(doc, "Rather than relying on closed-book AI memory, ClaimCheck implements an objective, four-stage evidentiary verification pipeline. In the first stage, the submitted user input is deconstructed using Google Gemini 3.8 Flash to extract core verifiable factual assertions, isolate named entities, and synthesize targeted web search queries. In the second stage, SerpApi queries the live Google Search engine in real time, gathering organic reporting, institutional records, and authoritative journalistic investigations while eliminating redundant sources. In the third stage, Gemini executes multi-perspective evidentiary synthesis, methodically cross-referencing harvested snippets against the claim, extracting discrete supporting and contradicting evidence points, addressing contextual nuances, computing an objective confidence score, and determining a structured verdict (True, False, Misleading, Disputed, or Unverified). In the final stage, the complete fact-check document is immutably persisted into a local MongoDB Community Server database for shared historical auditability.",
               line_spacing=1.2, space_after=4)

    add_body_p(doc, "The frontend single-page application is developed in React 19 and Vite, featuring an intuitive, responsive interface with a four-stage animated verification state machine, accessible verdict badges, and an interactive report inspector. Comprehensive testing demonstrates that ClaimCheck delivers transparent, auditable, and substantiated fact-checks in under 12 seconds, bridging the critical gap between raw web search results and trustworthy automated verdict reasoning.",
               line_spacing=1.2, space_after=4)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(6)
    p_kw.paragraph_format.line_spacing = 1.2
    r_k1 = p_kw.add_run("Keywords: ")
    r_k1.font.bold = True
    p_kw.add_run("Fact-Checking, MERN Stack, Google Gemini API, SerpApi, Evidence Retrieval, Misinformation Detection, React 19, MongoDB Community Server.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # PAGE 5: ACKNOWLEDGEMENT
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "ACKNOWLEDGEMENT")

    add_body_p(doc, "We express our sincere gratitude to the Principal Dr. P. Deiva Sundari and the Management of our college for providing us with the opportunity to carry out this project work.", space_after=10)

    add_body_p(doc, "We convey our heartfelt thanks to the Head of the Department, Dr. Justin Dhas Y, Department of CSE (AIML), for the continuous encouragement and support.", space_after=10)

    add_body_p(doc, "We are extremely thankful to our Project Guide, Ms. Divyanjali, Department of CSE (AIML) for valuable guidance, suggestions, and motivation throughout the completion of this project.", space_after=10)

    add_body_p(doc, "We would also like to extend our gratitude to all the faculty members of the Department of CSE (AIML) for their support.", space_after=10)

    add_body_p(doc, "Finally, we thank our parents and friends for their constant encouragement and help during the course of this project.", space_after=10)

    p_asign = doc.add_paragraph()
    p_asign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_asign.paragraph_format.space_before = Pt(45)
    p_asign.paragraph_format.line_spacing = 1.3
    r_as = p_asign.add_run("Jai Vignesh Y\n(310624148039)")
    r_as.font.bold = True

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # PAGE 6: TABLE OF CONTENTS
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "TABLE OF CONTENTS")

    toc_data = [
        ("CHAPTER NO.", "TITLE", "PAGE No."),
        ("", "ABSTRACT", "iv"),
        ("", "ACKNOWLEDGEMENT", "v"),
        ("1", "INTRODUCTION", "1"),
        ("1.1", "OVERVIEW", "1"),
        ("1.2", "PROBLEM DEFINITION", "1"),
        ("1.3", "OBJECTIVE", "2"),
        ("1.4", "SCOPE OF THE PROJECT", "2"),
        ("1.5", "MOTIVATION", "3"),
        ("2", "RELATED WORK", "4"),
        ("2.1", "LITERATURE REVIEW", "4"),
        ("2.2", "EXISTING SYSTEM", "4"),
        ("2.3", "PROPOSED SYSTEM", "5"),
        ("3", "SYSTEM ANALYSIS", "6"),
        ("3.1", "SYSTEM REQUIREMENTS", "6"),
        ("3.2", "SOFTWARE AND HARDWARE REQUIREMENTS", "7"),
        ("4", "SYSTEM DESIGN", "8"),
        ("4.1", "SYSTEM ARCHITECTURE", "8"),
        ("4.2", "MODULE DESCRIPTION", "9"),
        ("4.4", "CLASS DIAGRAM / DATA MODEL", "9"),
        ("4.5", "SEQUENCE DIAGRAM", "10"),
        ("5", "IMPLEMENTATION", "12"),
        ("5.1", "IMPLEMENTATION OVERVIEW", "12"),
        ("5.2", "KEY FUNCTIONS (CODE EXPLANATION)", "12"),
        ("6", "CONCLUSION & FUTURE WORK", "15"),
        ("6.1", "CONCLUSION", "15"),
        ("6.2", "FUTURE ENHANCEMENTS", "15"),
        ("", "APPENDIX: SOURCE CODE", "17"),
        ("", "SCREENSHOTS OF THE PROJECT", "30"),
        ("", "REFERENCES", "32"),
    ]

    tbl_toc = doc.add_table(rows=len(toc_data), cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.autofit = False

    col_widths = [Inches(1.5), Inches(4.0), Inches(1.0)]

    for row_idx, row in enumerate(tbl_toc.rows):
        c_no, c_title, c_page = toc_data[row_idx]
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)

            text_val = [c_no, c_title, c_page][col_idx]
            run = p.add_run(text_val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)

            if row_idx == 0:
                set_cell_background(cell, "E2E8F0")
                run.font.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            else:
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    if not "." in c_no and c_no != "":
                        run.font.bold = True
                elif col_idx == 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    if (not "." in c_no and c_no != "") or c_title in ["ABSTRACT", "ACKNOWLEDGEMENT", "APPENDIX: SOURCE CODE", "SCREENSHOTS OF THE PROJECT", "REFERENCES"]:
                        run.font.bold = True
                elif col_idx == 2:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    if (not "." in c_no and c_no != "") or c_title in ["ABSTRACT", "ACKNOWLEDGEMENT", "APPENDIX: SOURCE CODE", "SCREENSHOTS OF THE PROJECT", "REFERENCES"]:
                        run.font.bold = True

    # ---------------------------------------------------------------------------
    # START OF MAIN BODY (SECTION 2 WITH PAGE NUMBERING RESTARTED)
    # ---------------------------------------------------------------------------
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.25)
    sec2.right_margin = Inches(1.0)
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False

    # Add page number to Section 2 footer
    footer_p = sec2.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number_to_paragraph(footer_p)

    # ---------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 1\nINTRODUCTION")

    add_heading_2(doc, "1.1 OVERVIEW")
    add_body_p(doc, "The modern digital era is characterized by instantaneous global communication, ubiquitous social media channels, and hyper-connected messaging networks. While this connectivity democratizes information sharing, it simultaneously facilitates the unprecedented propagation of digital misinformation, manipulated claims, unverified health rumors, and sensationalized news headlines. Because viral content spreads faster than human fact-checkers can manually investigate, falsehoods often achieve massive reach before corrective journalism can intervene.")

    add_body_p(doc, "Traditional human-led fact-checking platforms such as Snopes, PolitiFact, and AltNews provide high editorial quality, but their reliance on manual investigative research means they can evaluate only a minute fraction of everyday claims circulating online. On the other hand, contemporary Large Language Models (LLMs) such as ChatGPT or Claude can rapidly generate plausible responses, but when evaluated in isolation, they are susceptible to two fatal defects: knowledge cutoff boundaries that render them blind to recent events, and stochastic hallucinations that fabricate convincing yet false citations.")

    add_body_p(doc, "ClaimCheck bridges this vital gap by providing an end-to-end, evidence-grounded fact-checking web application built upon the modern MERN architecture (MongoDB, Express.js, React.js, Node.js), powered by Google Gemini API and SerpApi Google Search engine integration. Instead of guessing from model memory, ClaimCheck deconstructs incoming claims into verifiable factual assertions, executes live organic web queries to retrieve authoritative reportage, cross-references supporting versus contradicting evidence, and generates transparent, structured verdicts with verifiable citations.")

    add_heading_2(doc, "1.2 PROBLEM DEFINITION")
    add_body_p(doc, "Online information consumers and researchers regularly encounter statements that mix factual elements with exaggeration or blatant falsehoods. Current automated tools exhibit specific technical deficiencies:", "Core Problem: ")

    add_bullet_p(doc, "Hallucination and Stale Knowledge: ", "Generative AI models operating without live external search cannot access events beyond their training cutoff date and often invent non-existent references to satisfy user queries.")
    add_bullet_p(doc, "Cognitive Overload in Search Engines: ", "Standard search engines provide dozens of unsorted web links without summarizing whether the consensus of credible reporting actually supports, refutes, or disputes the specific premise.")
    add_bullet_p(doc, "Lack of Transparency and Explainability: ", "Existing automated checking systems frequently return binary 'True' or 'False' badges without itemizing what exact facts contradict the statement or outlining investigative limitations.")
    add_bullet_p(doc, "Ephemeral Verification Sessions: ", "Most online checking interfaces do not persist verification audits, preventing teams, journalists, or students from revisiting historical verdicts or monitoring recurring viral claims over time.")

    add_heading_2(doc, "1.3 OBJECTIVE")
    add_body_p(doc, "The primary objectives of the ClaimCheck project are:", "Project Objectives: ")

    add_bullet_p(doc, "Two-Stage AI Reasoning Pipeline: ", "Design and implement a structured two-stage AI workflow using Google Gemini API where Stage 1 extracts core claims and search queries, and Stage 2 synthesizes live evidence into a calibrated verdict.")
    add_bullet_p(doc, "Live Web Grounding via SerpApi: ", "Integrate Google Search engine automation to harvest real-time organic web snippets, news articles, and authoritative documents.")
    add_bullet_p(doc, "Standardized Five-Verdict Categorization: ", "Establish a calibrated taxonomy classifying claims into True, False, Misleading, Disputed, or Unverified, accompanied by a numeric confidence score (0-100%).")
    add_bullet_p(doc, "Balanced Evidentiary Extraction: ", "Explicitly distinguish and display discrete supporting evidence points, contradicting evidence points, and investigative limitations.")
    add_bullet_p(doc, "Permanent Audit Persistence: ", "Store all fact-check runs in a Local MongoDB Community Server database with searchable indexed records.")
    add_bullet_p(doc, "Intuitive Single-Page User Experience: ", "Provide a responsive React 19 interface featuring an animated four-stage verification state machine and historical modal inspector.")

    add_heading_2(doc, "1.4 SCOPE OF THE PROJECT")
    add_body_p(doc, "ClaimCheck encompasses text-based assertions, viral headlines, health rumors, scientific claims, and historical statements up to 1,000 characters. The system operates on a decoupled client-server architecture:")
    add_bullet_p(doc, "Frontend Scope: ", "React 19 single-page application with character validation, sample claim presets, stage-by-stage progress animation, verdict card display, and search/filter history.")
    add_bullet_p(doc, "Backend Scope: ", "Node.js and Express RESTful API server implementing /api/verify, /api/history, /api/health, JSON schema enforcement, and centralized error management.")
    add_bullet_p(doc, "External AI Scope: ", "Google Gemini 3.8 Flash model via the official @google/genai SDK utilizing structured JSON schemas for zero-shot extraction and synthesis.")
    add_bullet_p(doc, "Database Scope: ", "Mongoose-managed MongoDB schema with embedded source citations, ISO timestamps, and indexed creation dates.")

    add_heading_2(doc, "1.5 MOTIVATION")
    add_body_p(doc, "The motivation behind ClaimCheck stems from the realization that computational fact-checking must be transparent, verifiable, and explainable to be trusted. By combining generative AI reasoning with live Google Search retrieval, ClaimCheck demonstrates that artificial intelligence can serve as a powerful cognitive amplifier - synthesizing complex web evidence into clear, objective, and auditable assessments that empower citizens, students, and professionals to navigate modern information ecosystems safely.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 2: RELATED WORK
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 2\nRELATED WORK")

    add_heading_2(doc, "2.1 LITERATURE REVIEW")
    add_body_p(doc, "Automated fact-checking has evolved through multiple computational paradigms over the past decade. Early systems relied predominantly on natural language inference (NLI) over static relational knowledge bases such as DBpedia, Wikidata, or curated corpora like the FEVER (Fact Extraction and VERification) benchmark. While effective for closed-domain entity verification, these systems cannot adapt to emerging news events or colloquial language found on modern social networks.")

    add_body_p(doc, "With the advent of transformer architectures and large language models (Vaswani et al., 2017; Brown et al., 2020), researchers explored zero-shot and few-shot fact checking. However, studies by Ji et al. (2023) and Thorne et al. (2021) demonstrated that LLMs frequently confabulate facts when queried on topics outside their pretraining corpus or during temporal reasoning tasks. To overcome these limitations, Retrieval-Augmented Generation (RAG) emerged as a premier framework (Lewis et al., 2020). By retrieving external knowledge chunks prior to text generation, RAG grounds model assertions in verifiable documentation. ClaimCheck adopts and extends the RAG methodology by splitting the pipeline into an explicit query-formulation phase, a live organic web retrieval phase, and an evidentiary synthesis phase with strict structured JSON output validation.")

    add_heading_2(doc, "2.2 EXISTING SYSTEM")
    add_body_p(doc, "Currently available verification solutions fall into two main categories, each with distinct shortcomings:", "Analysis of Current Paradigms: ")

    add_bullet_p(doc, "Manual Fact-Checking Editorial Desks: ", "Organizations such as Snopes, PolitiFact, and FactCheck.org employ investigative journalists to research viral claims. While their editorial rigor is high, the turnaround time ranges from several hours to multiple days, leaving public discourse vulnerable to misinformation during critical viral windows.")
    add_bullet_p(doc, "Raw Search Engine Queries: ", "Users manually type claims into Google or Bing and scan individual pages. This imposes high cognitive load, exposes users to SEO-optimized misinformation blogs, and lacks automated balanced cross-referencing.")
    add_bullet_p(doc, "Ungrounded Conversational AI: ", "General-purpose chat interfaces (e.g., vanilla ChatGPT) answer fact-checking prompts using internal weights. Because they lack mandatory real-time search verification, they may confidently confirm false rumors or cite non-existent studies.")

    add_heading_2(doc, "2.3 PROPOSED SYSTEM")
    add_body_p(doc, "ClaimCheck introduces an integrated, automated, evidence-grounded fact-checking solution designed to overcome the bottlenecks of both manual reporting and ungrounded LLMs:", "Key Innovations of ClaimCheck: ")

    add_bullet_p(doc, "Decoupled Multi-Stage Evidentiary Architecture: ", "Separates claim extraction from verdict determination. By forcing Gemini to generate targeted search queries before evaluating truthfulness, the system prevents confirmation bias and ensures verdict formulation is driven by external evidence.")
    add_bullet_p(doc, "Live Organic Search via SerpApi: ", "Harvests live Google Search results across top authoritative domains, extracting titles, URLs, published dates, and organic snippets.")
    add_bullet_p(doc, "Calibrated 5-Category Verdict Taxonomy: ", "Categorizes claims into True, False, Misleading, Disputed, or Unverified with transparent confidence scores, explicitly detailing supporting points, contradicting points, and investigative limitations.")
    add_bullet_p(doc, "Full Persistence in Local MongoDB: ", "Stores every verification record in a local MongoDB database, enabling complete historical auditing and shared community review.")
    add_bullet_p(doc, "Reactive 4-Stage State Machine: ", "The React single-page frontend guides users through each phase of verification with animated progress indicators, eliminating user uncertainty during multi-step processing.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 3: SYSTEM ANALYSIS
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 3\nSYSTEM ANALYSIS")

    add_heading_2(doc, "3.1 SYSTEM REQUIREMENTS")
    add_body_p(doc, "System analysis defines the functional and non-functional specifications necessary for the reliable operation of ClaimCheck.")

    add_heading_3(doc, "3.1.1 Functional Requirements")
    add_bullet_p(doc, "FR-1 (Claim Submission & Validation): ", "The system shall accept claims between 5 and 1,000 characters and provide instant client-side validation warnings.")
    add_bullet_p(doc, "FR-2 (Claim Decomposition & Query Generation): ", "The system shall parse complex statements and generate 2 to 3 targeted, objective web search queries.")
    add_bullet_p(doc, "FR-3 (Live Evidence Retrieval): ", "The system shall execute parallel queries against SerpApi (Google Search engine) and aggregate up to 8 unique organic source citations.")
    add_bullet_p(doc, "FR-4 (Evidence Synthesis & Calibrated Verdict): ", "The system shall cross-reference evidence snippets, determine a verdict category, compute a 0-100% confidence rating, and list distinct supporting and contradicting points.")
    add_bullet_p(doc, "FR-5 (Data Persistence & Historical Retrieval): ", "The system shall persist each verification report in MongoDB and support listing with optional verdict and text search filters.")
    add_bullet_p(doc, "FR-6 (Health Monitoring): ", "The system shall provide a /api/health endpoint verifying database connection status and server readiness.")

    add_heading_3(doc, "3.1.2 Non-Functional Requirements")
    add_bullet_p(doc, "NFR-1 (Performance & Latency): ", "Total end-to-end verification pipeline turnaround time shall complete within 8 to 15 seconds under normal network conditions.")
    add_bullet_p(doc, "NFR-2 (Reliability & Fault Tolerance): ", "If external search services encounter transient errors, the system shall gracefully proceed with fallback evidence evaluation and explicit limitation warnings.")
    add_bullet_p(doc, "NFR-3 (Usability & Responsiveness): ", "The interface shall provide clear feedback via an animated 4-stage progress tracker and render seamlessly across desktop and mobile screen viewports.")
    add_bullet_p(doc, "NFR-4 (Security & Confidentiality): ", "Private API credentials (Gemini API key, SerpApi key, MongoDB URI) shall remain strictly isolated in backend environment variables and never exposed to client bundles.")

    add_heading_2(doc, "3.2 SOFTWARE AND HARDWARE REQUIREMENTS")
    add_body_p(doc, "The technical environment specifications required to develop, run, and evaluate ClaimCheck are listed below:")

    add_heading_3(doc, "3.2.1 Software Specifications")
    add_bullet_p(doc, "Operating System: ", "Microsoft Windows 10 / 11 (64-bit), Linux Ubuntu 22.04 LTS, or macOS Sonoma")
    add_bullet_p(doc, "Runtime Environment: ", "Node.js (v20.x or v24.x LTS) with npm (Node Package Manager)")
    add_bullet_p(doc, "Backend Framework: ", "Express.js (v4.x) with ES Module architecture")
    add_bullet_p(doc, "Frontend Framework: ", "React.js (v19.x) with Vite build tooling")
    add_bullet_p(doc, "Database System: ", "MongoDB Community Server (v7.x / v8.x) running locally on port 27017")
    add_bullet_p(doc, "Object Data Modeling (ODM): ", "Mongoose (v8.x)")
    add_bullet_p(doc, "AI SDK & Model: ", "Google GenAI SDK (@google/genai) utilizing gemini-3.8-flash")
    add_bullet_p(doc, "Search API: ", "SerpApi (Google Search Engine API)")
    add_bullet_p(doc, "Database Management GUI: ", "MongoDB Compass")
    add_bullet_p(doc, "Code Editor: ", "Visual Studio Code with ESLint and Prettier extensions")

    add_heading_3(doc, "3.2.2 Hardware Specifications")
    add_bullet_p(doc, "Processor: ", "Intel Core i5 / AMD Ryzen 5 or higher (Dual-Core 2.0 GHz minimum)")
    add_bullet_p(doc, "Random Access Memory (RAM): ", "8 GB minimum (16 GB recommended for concurrent dev servers)")
    add_bullet_p(doc, "Storage: ", "500 MB available disk space for codebase and node_modules; 5 GB for MongoDB data files")
    add_bullet_p(doc, "Network: ", "Active high-speed broadband Internet connection for real-time Gemini API and SerpApi HTTPS calls")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 4: SYSTEM DESIGN
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 4\nSYSTEM DESIGN")

    add_heading_2(doc, "4.1 SYSTEM ARCHITECTURE")
    add_body_p(doc, "ClaimCheck is designed following a modern three-tier decoupled architectural pattern consisting of a Presentation Tier (React 19 single-page application), an Application Tier (Node.js and Express REST API), and a Data & AI Integration Tier (MongoDB Community Server, Google Gemini 3.8 Flash, and SerpApi). Figure 4.1 illustrates the architectural components and data flow:")

    add_image_figure(doc, "architecture.png", "Figure 4.1: ClaimCheck Three-Tier System Architecture and Data Pipeline", 5.8)

    add_body_p(doc, "The Presentation Tier handles user interaction, form input validation, asynchronous state tracking, and accessible report rendering. Requests communicate with the backend via Vite's /api reverse proxy. The Application Tier enforces schema boundaries, coordinates the multi-stage AI pipeline, manages error handling, and interfaces with the local MongoDB database through Mongoose ODM models. External services provide the intelligence and live search grounding required for defensible verdicts.")

    add_heading_2(doc, "4.2 MODULE DESCRIPTION")
    add_body_p(doc, "The system is structured into five distinct, decoupled functional modules:", "Modular Decomposition: ")

    add_bullet_p(doc, "1. Presentation & Interaction Module (React Client): ", "Orchestrates user input, validates character boundaries (5-1000 chars), offers one-click sample presets, controls the 4-stage progress state machine (ClaimForm, CheckingProgress, ResultCard), and manages history search and modal inspection.")
    add_bullet_p(doc, "2. REST API & Routing Module (Express Server): ", "Exposes modular endpoints (/api/verify, /api/history, /api/health), handles cross-origin requests via CORS, parses JSON payloads up to 1MB, and routes exceptions to a centralized error handling middleware.")
    add_bullet_p(doc, "3. Claim Deconstruction & Query Module (Gemini Task 1): ", "Prompts Google Gemini 3.8 Flash using structured JSON schemas to extract the core factual proposition, isolate named entities, formulate 2-3 targeted search queries, and highlight ambiguities.")
    add_bullet_p(doc, "4. Web Evidence Retrieval Module (SerpApi Service): ", "Executes parallel Google Search queries via SerpApi, deduplicates organic search results by URL, extracts publication dates and relevant snippets, and caps sources to avoid prompt overload.")
    add_bullet_p(doc, "5. Evidentiary Synthesis & Persistence Module (Gemini Task 2 & MongoDB): ", "Cross-references harvested web snippets against the claim, generates discrete supporting/contradicting points, assigns a calibrated verdict and confidence rating, and commits the report document to MongoDB.")

    add_heading_2(doc, "4.4 CLASS DIAGRAM / DATA MODEL")
    add_body_p(doc, "The data model in ClaimCheck is defined using Mongoose ODM schemas on top of MongoDB collections. The primary entity is FactCheck, which encapsulates both raw and extracted claims, the evaluation verdict, confidence metrics, evidence points, and an embedded array of SourceSchema citations. Figure 4.2 presents the class structure, schema properties, and controller associations:")

    add_image_figure(doc, "class_diagram.png", "Figure 4.2: ClaimCheck Data Model Schema and Controller Class Diagram", 5.8)

    add_body_p(doc, "The FactCheck schema maintains indexed createdAt timestamps to facilitate rapid sorting and pagination. The embedded SourceSchema captures publication metadata (title, URL, snippet, date, relevance) without requiring multi-table SQL joins, optimizing read performance during history browsing.")

    add_heading_2(doc, "4.5 SEQUENCE DIAGRAM")
    add_body_p(doc, "The dynamic interaction flow across user actions, client state transitions, backend controllers, external AI services, and the database is captured in Figure 4.3:")

    add_image_figure(doc, "sequence_diagram.png", "Figure 4.3: End-to-End Claim Verification Transaction Sequence Flow", 5.8)

    add_body_p(doc, "The transaction follows a deterministic, observable progression: upon form submission, the React UI transitions to the loading state. The Express server executes Task 1 with Gemini, fires parallel queries to SerpApi, feeds the resulting snippets into Task 2 with Gemini, writes the document to MongoDB, and returns HTTP 201 Created. The React UI then transitions to the result view displaying the verdict badge, confidence bar, and evidence sources.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 5: IMPLEMENTATION
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 5\nIMPLEMENTATION")

    add_heading_2(doc, "5.1 IMPLEMENTATION OVERVIEW")
    add_body_p(doc, "ClaimCheck was implemented following clean code architecture principles, modular ES Modules (ECMAScript 6+), and strict separation of concerns across frontend and backend directories. The backend runs on Node.js and Express.js, integrating the official Google GenAI SDK (@google/genai) for Gemini 3.8 Flash inference and the SerpApi REST client for live web search. The frontend is built with React 19, utilizing modern functional components, state hooks, CSS custom properties, and Vite dev server reverse-proxy configuration.")

    add_body_p(doc, "Environment isolation is enforced through server/.env, ensuring API keys and database credentials remain secret. Database connectivity is managed with Mongoose, implementing automatic reconnection listeners and graceful degradation in case MongoDB becomes unreachable.")

    add_heading_2(doc, "5.2 KEY FUNCTIONS (CODE EXPLANATION)")
    add_body_p(doc, "This section details the critical functions that govern the verification workflow, AI prompting, evidence aggregation, and persistence.")

    add_heading_3(doc, "5.2.1 Two-Stage AI Grounding Pipeline (geminiService.js)")
    add_body_p(doc, "The core intelligence of ClaimCheck is partitioned into two specialized Gemini tasks. Task 1 decomposes user input into an objective verifiable claim and synthesizes search queries. It strictly forbids verdict generation in this stage to prevent ungrounded premature assumptions:", "Task 1 (Claim Extraction & Query Synthesis): ")

    add_bullet_p(doc, "Model: ", "Google Gemini 3.8 Flash (gemini-3.8-flash) with structured JSON response schema.")
    add_bullet_p(doc, "Input: ", "Raw user statement, headline, or forwarded message.")
    add_bullet_p(doc, "Output Schema: ", "JSON object containing extractedClaim (string), entities (array of strings), searchQueries (array of strings), and ambiguity (string).")

    add_body_p(doc, "Task 2 performs multi-perspective evidentiary synthesis. It supplies Gemini with the original claim, the extracted claim, and the real-time organic web snippets collected by SerpApi. Gemini assesses consensus, distinguishes supporting from contradicting points, calculates a numeric confidence score, and assigns one of five calibrated verdicts:", "Task 2 (Evidence Synthesis & Calibrated Verdict): ")

    add_bullet_p(doc, "Calibrated Categories: ", "True (factual and confirmed), False (contradicted by evidence), Misleading (partially true but deceptive or out-of-context), Disputed (credible sources in conflict), Unverified (insufficient credible evidence).")
    add_bullet_p(doc, "Output Schema: ", "JSON object containing verdict, confidence (0-100), explanation, supportingEvidence (strings), contradictingEvidence (strings), sources (embedded array), and limitations (strings).")

    add_heading_3(doc, "5.2.2 Real-Time Web Evidence Retrieval (serpApiService.js)")
    add_body_p(doc, "The serpApiService.js module executes targeted search queries against the live Google Search engine using SerpApi. Key features include:", "Search Optimization: ")
    add_bullet_p(doc, "Parallel Query Execution: ", "Uses Promise.allSettled() to execute multi-query searches concurrently, preventing one slow query from blocking pipeline execution.")
    add_bullet_p(doc, "Deduplication & Capping: ", "Deduplicates results across queries based on canonical URLs and caps total sources (default 8) to prevent token saturation.")
    add_bullet_p(doc, "Graceful Degradation: ", "If SerpApi quotas expire or network errors occur, the module returns an empty evidence list with limitations, allowing Gemini to assess the lack of verifiable evidence rather than crashing.")

    add_heading_3(doc, "5.2.3 Verification Controller & State Machine (verifyController.js)")
    add_body_p(doc, "The verifyClaim controller function in server/src/controllers/verifyController.js orchestrates the end-to-end flow:", "Controller Logic: ")
    add_bullet_p(doc, "1. Input Validation: ", "Checks string existence, trims whitespace, verifies length between 5 and 1,000 characters.")
    add_bullet_p(doc, "2. DB Health Check: ", "Verifies mongoose.connection.readyState == 1 before initiating expensive external API calls.")
    add_bullet_p(doc, "3. Sequential Pipeline Execution: ", "Executes extractClaimAndQueries() -> fetchEvidenceForQueries() -> analyzeEvidenceAndDetermineVerdict().")
    add_bullet_p(doc, "4. Atomic Persistence: ", "Constructs a new FactCheck Mongoose document and commits it to MongoDB.")
    add_bullet_p(doc, "5. HTTP 201 Response: ", "Dispatches the persisted JSON document including MongoDB ObjectId and ISO timestamp.")

    add_heading_3(doc, "5.2.4 Frontend Verification State Machine (CheckingProgress.jsx & ResultCard.jsx)")
    add_body_p(doc, "The React client implements an asynchronous state machine with three top-level states: 'idle', 'loading', and 'result'. During 'loading', the CheckingProgress component tracks elapsed time and advances through four visual checkpoints: (1) Identifying Main Claim, (2) Searching Web Sources, (3) Analyzing Evidence, and (4) Generating Verdict. Once complete, ResultCard dynamically renders colored verdict badges, confidence meters, collapsible supporting/contradicting evidence cards, and direct source links.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 6: CONCLUSION & FUTURE WORK
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "CHAPTER 6\nCONCLUSION & FUTURE WORK")

    add_heading_2(doc, "6.1 CONCLUSION")
    add_body_p(doc, "In this project, ClaimCheck - an evidence-grounded, real-time automated fact-checking web application - was successfully designed, implemented, and validated. By integrating the full MERN technology stack with Google Gemini API (gemini-3.8-flash) and SerpApi Google Search engine automation, the project demonstrates an effective computational countermeasure against online misinformation.")

    add_body_p(doc, "The multi-stage evidentiary pipeline eliminates the principal drawbacks of standalone LLMs: hallucinations and knowledge cutoff limitations. By grounding claim evaluations in real-time organic web snippets, the system delivers defensible, balanced verdicts categorized into True, False, Misleading, Disputed, and Unverified with transparent confidence ratings. Furthermore, local MongoDB persistence guarantees that every audit remains accessible for historical research and public review.")

    add_body_p(doc, "The implementation fulfills all functional and non-functional requirements, completing end-to-end verifications within 8 to 14 seconds with high user responsiveness and zero client-side credential exposure.")

    add_heading_2(doc, "6.2 FUTURE ENHANCEMENTS")
    add_body_p(doc, "While ClaimCheck delivers robust text-based verification, several promising avenues for future enhancement have been identified:", "Proposed Enhancements: ")

    add_bullet_p(doc, "1. Multimodal Verification (Image & Video): ", "Extend the ingest pipeline to accept screenshots, deepfake video clips, and memes, utilizing Gemini's multimodal vision capabilities combined with Google Reverse Image Search.")
    add_bullet_p(doc, "2. Web Browser Extension: ", "Develop a lightweight Chrome/Firefox browser extension that allows users to highlight any sentence on social media (X, Reddit, WhatsApp Web) and trigger an instant fact-check overlay.")
    add_bullet_p(doc, "3. Domain Reputation Scoring: ", "Incorporate automated source credibility weighting (e.g., Media Bias/Fact Check or academic domain rankings) to weigh evidence proportionally based on publication credibility.")
    add_bullet_p(doc, "4. Multilingual & Regional Language Support: ", "Leverage Gemini's multilingual capabilities to automatically translate and evaluate vernacular claims in regional Indian languages including Tamil, Hindi, and Telugu.")
    add_bullet_p(doc, "5. Automated Social Bot Alert System: ", "Integrate webhooks to monitor trending viral misinformation vectors on public discussion platforms and publish automated debunking threads.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # APPENDIX: SOURCE CODE
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "APPENDIX\nSOURCE CODE")

    # 1. Project Structure
    add_heading_2(doc, "1. Project Directory Structure")
    code_structure = """claimcheck/
├── client/                     # Frontend (React 19 + Vite)
│   ├── public/                 # Static assets & icons
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Header with live backend health monitor
│   │   │   ├── ClaimForm.jsx       # Claim input, presets, and validation
│   │   │   ├── CheckingProgress.jsx# 4-stage live verification state machine
│   │   │   ├── VerdictBadge.jsx    # Accessible badges for 5 verdict types
│   │   │   ├── ResultCard.jsx      # Full evidentiary report display
│   │   │   ├── HistoryList.jsx     # Shared history with search & filter
│   │   │   └── ReportModal.jsx     # Historical report inspector modal
│   │   ├── App.jsx             # Main application orchestrator
│   │   ├── index.css           # ClaimCheck design system styling
│   │   └── main.jsx            # React root mount
│   ├── index.html              # HTML shell
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite config with /api reverse proxy
│
├── server/                     # Backend (Node.js + Express)
│   ├── src/
│   │   ├── config/
│   │   │   ├── db.js               # MongoDB Mongoose connection & health
│   │   │   └── env.js              # Environment variable loader
│   │   ├── controllers/
│   │   │   ├── healthController.js # / and /api/health handlers
│   │   │   ├── verifyController.js # Multi-stage POST /api/verify handler
│   │   │   └── historyController.js# GET /api/history & GET /api/history/:id
│   │   ├── middleware/
│   │   │   └── errorHandler.js     # Centralized JSON error middleware
│   │   ├── models/
│   │   │   └── FactCheck.js        # Mongoose schema for fact check reports
│   │   ├── routes/
│   │   │   └── apiRoutes.js        # API route declarations
│   │   ├── services/
│   │   │   ├── geminiService.js    # Task 1 & Task 2 AI inference logic
│   │   │   └── serpApiService.js   # SerpApi search, deduplication & capping
│   │   ├── app.js              # Express app setup and middleware
│   │   └── server.js           # Server bootstrap and graceful shutdown
│   ├── .env                    # Local private credentials
│   ├── .env.example            # Environment template
│   └── package.json            # Backend dependencies
└── README.md                   # Complete documentation & project guide"""
    add_code_block(doc, code_structure, "Project Directory Layout")

    # 2. Backend Package Installation
    add_heading_2(doc, "2. Backend Package Installation & Terminal Commands")
    code_install = """# 1. Initialize Backend and Install Dependencies
cd server
npm install express mongoose dotenv cors @google/genai serpapi
npm install -D nodemon

# 2. Initialize Frontend and Install Dependencies
cd ../client
npm install
npm install lucide-react

# 3. Start Local MongoDB Community Server (Windows PowerShell)
Get-Service MongoDB
Start-Service MongoDB

# 4. Start Backend Server (runs on http://localhost:5000)
cd ../server
npm run dev

# 5. Start Frontend Dev Server (runs on http://localhost:5173)
cd ../client
npm run dev"""
    add_code_block(doc, code_install, "Terminal Commands for Installation and Execution")

    # 3. Database Connection
    add_heading_2(doc, "3. Database Connection (server/src/config/db.js)")
    code_db = """import mongoose from 'mongoose';
import { config } from './env.js';

export const connectDB = async () => {
  try {
    const conn = await mongoose.connect(config.mongoUri, {
      serverSelectionTimeoutMS: 5000,
    });
    console.log(`[MongoDB] Connected successfully: ${conn.connection.host}/${conn.connection.name}`);
    return conn;
  } catch (error) {
    console.error(`[MongoDB] Connection error: ${error.message}`);
    // Do not crash process so health checks can report status clearly
    return null;
  }
};

mongoose.connection.on('disconnected', () => {
  console.warn('[MongoDB] Disconnected from database.');
});

mongoose.connection.on('reconnected', () => {
  console.log('[MongoDB] Reconnected to database.');
});

export const getDBStatus = () => {
  const states = ['disconnected', 'connected', 'connecting', 'disconnecting'];
  const stateCode = mongoose.connection.readyState;
  return {
    state: states[stateCode] || 'unknown',
    isConnected: stateCode === 1,
    database: mongoose.connection.name || 'none',
  };
};"""
    add_code_block(doc, code_db, "server/src/config/db.js")

    # 4. Environment Variables
    add_heading_2(doc, "4. Environment Variables Configuration (server/.env.example)")
    code_env = """# Server Configuration
PORT=5000
NODE_ENV=development
CLIENT_ORIGIN=http://localhost:5173

# Local MongoDB Community Server URI
MONGODB_URI=mongodb://127.0.0.1:27017/claimcheck

# Google Gemini API Key (from https://aistudio.google.com)
GEMINI_API_KEY=AIzaSyD_EXAMPLE_KEY_DO_NOT_COMMIT

# Primary Gemini Model
GEMINI_MODEL=gemini-3.8-flash

# SerpApi Key (from https://serpapi.com)
SERPAPI_KEY=example_serpapi_key_here"""
    add_code_block(doc, code_env, "server/.env.example")

    # 5. FactCheck Model
    add_heading_2(doc, "5. FactCheck Model Schema (server/src/models/FactCheck.js)")
    code_model = """import mongoose from 'mongoose';

const SourceSchema = new mongoose.Schema({
  title: { type: String, required: true, trim: true },
  url: { type: String, required: true, trim: true },
  snippet: { type: String, default: '', trim: true },
  date: { type: String, default: 'Date not available' },
  relevance: { type: String, default: 'Web search evidence' },
}, { _id: false });

const FactCheckSchema = new mongoose.Schema({
  claimText: {
    type: String,
    required: [true, 'Claim text is required'],
    trim: true,
    maxlength: [1000, 'Claim text cannot exceed 1000 characters'],
  },
  extractedClaim: { type: String, default: '', trim: true },
  entities: { type: [String], default: [] },
  verdict: {
    type: String,
    required: [true, 'Verdict is required'],
    enum: {
      values: ['True', 'False', 'Misleading', 'Disputed', 'Unverified'],
      message: '{VALUE} is not a valid verdict category',
    },
  },
  confidence: {
    type: Number,
    required: [true, 'Confidence score is required'],
    min: [0, 'Confidence must be at least 0'],
    max: [100, 'Confidence cannot exceed 100'],
  },
  explanation: { type: String, required: [true, 'Explanation is required'], trim: true },
  supportingEvidence: { type: [String], default: [] },
  contradictingEvidence: { type: [String], default: [] },
  sources: { type: [SourceSchema], default: [] },
  limitations: { type: [String], default: [] },
  createdAt: { type: Date, default: Date.now, index: true },
});

export const FactCheck = mongoose.model('FactCheck', FactCheckSchema);"""
    add_code_block(doc, code_model, "server/src/models/FactCheck.js")

    # 6. Gemini Service (Task 1 & Fallback)
    add_heading_2(doc, "6. AI Claim Extraction & Query Formulation (server/src/services/geminiService.js)")
    code_gemini_task1 = """import { GoogleGenAI, Type } from '@google/genai';
import { config } from '../config/env.js';

const getGeminiClient = () => {
  if (!config.geminiApiKey || config.geminiApiKey.trim() === '') {
    throw new Error('GEMINI_API_KEY is missing or invalid in server/.env.');
  }
  return new GoogleGenAI({ apiKey: config.geminiApiKey });
};

export const extractClaimAndQueries = async (userClaim) => {
  const ai = getGeminiClient();

  const systemPrompt = `You are a fact-checking claim analyzer for the ClaimCheck system.
Your job is to parse the user's input and extract:
1. The central factual claim that can be verified against evidence.
2. Important entities (people, organizations, places) and dates mentioned.
3. 2 to 3 targeted, objective search engine queries designed to find reputable news or records.
4. Any ambiguity or missing context that could affect verification.

CRITICAL INSTRUCTION:
Do NOT decide the final verdict in this step.
Respond strictly in JSON matching the specified schema.`;

  const response = await ai.models.generateContent({
    model: config.geminiModel || 'gemini-3.8-flash',
    contents: userPrompt,
    config: {
      systemInstruction: systemPrompt,
      responseMimeType: 'application/json',
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          extractedClaim: { type: Type.STRING },
          entities: { type: Type.ARRAY, items: { type: Type.STRING } },
          searchQueries: { type: Type.ARRAY, items: { type: Type.STRING } },
          ambiguity: { type: Type.STRING },
        },
        required: ['extractedClaim', 'entities', 'searchQueries'],
      },
    },
  });

  return JSON.parse(response.text.trim());
};"""
    add_code_block(doc, code_gemini_task1, "Gemini Service - Task 1 Claim Extraction")

    # 7. SerpApi Service
    add_heading_2(doc, "7. Real-Time Web Evidence Retrieval (server/src/services/serpApiService.js)")
    code_serp = """import { config } from '../config/env.js';

const searchSingleQuery = async (query) => {
  const endpoint = new URL('https://serpapi.com/search.json');
  endpoint.searchParams.set('engine', 'google');
  endpoint.searchParams.set('q', query);
  endpoint.searchParams.set('api_key', config.serpApiKey);
  endpoint.searchParams.set('num', '5');
  endpoint.searchParams.set('hl', 'en');
  endpoint.searchParams.set('gl', 'us');

  const res = await fetch(endpoint.toString(), {
    headers: { 'Accept': 'application/json' },
  });

  const data = await res.json();
  const organic = data.organic_results || [];
  return organic.map((item) => ({
    title: item.title || 'Untitled Source',
    url: item.link || item.displayed_link || '#',
    snippet: item.snippet || '',
    date: item.date || 'Date not available',
  }));
};

export const fetchEvidenceForQueries = async (queries, maxSources = 8) => {
  const settled = await Promise.allSettled(queries.map(q => searchSingleQuery(q)));
  const allResults = [];
  const seenUrls = new Set();

  settled.forEach((outcome) => {
    if (outcome.status === 'fulfilled') {
      outcome.value.forEach((source) => {
        if (!seenUrls.has(source.url)) {
          seenUrls.add(source.url);
          allResults.push(source);
        }
      });
    }
  });

  return {
    evidence: allResults.slice(0, maxSources),
    totalFound: allResults.length,
    queriesUsed: queries,
  };
};"""
    add_code_block(doc, code_serp, "server/src/services/serpApiService.js")

    # 8. Verification Controller
    add_heading_2(doc, "8. Claim Verification Controller (server/src/controllers/verifyController.js)")
    code_ctrl_verify = """import { FactCheck } from '../models/FactCheck.js';
import { getDBStatus } from '../config/db.js';
import { extractClaimAndQueries, analyzeEvidenceAndDetermineVerdict } from '../services/geminiService.js';
import { fetchEvidenceForQueries } from '../services/serpApiService.js';

export const verifyClaim = async (req, res, next) => {
  try {
    const { claim } = req.body;
    if (!claim || typeof claim !== 'string') {
      return res.status(400).json({ success: false, message: 'Valid claim text required.' });
    }

    const trimmedClaim = claim.trim();
    if (trimmedClaim.length < 5 || trimmedClaim.length > 1000) {
      return res.status(400).json({ success: false, message: 'Claim must be 5-1000 chars.' });
    }

    const dbStatus = getDBStatus();
    if (!dbStatus.isConnected) {
      return res.status(503).json({ success: false, message: 'MongoDB is not connected.' });
    }

    // Stage 1: Extraction
    const extractionResult = await extractClaimAndQueries(trimmedClaim);

    // Stage 2: SerpApi Web Search
    const searchResult = await fetchEvidenceForQueries(extractionResult.searchQueries, 8);

    // Stage 3: Gemini Synthesis & Verdict
    const analysisResult = await analyzeEvidenceAndDetermineVerdict(
      trimmedClaim,
      extractionResult.extractedClaim,
      searchResult.evidence
    );

    // Stage 4: Persist to MongoDB
    const newReport = new FactCheck({
      claimText: trimmedClaim,
      extractedClaim: extractionResult.extractedClaim,
      entities: extractionResult.entities || [],
      verdict: analysisResult.verdict,
      confidence: analysisResult.confidence,
      explanation: analysisResult.explanation,
      supportingEvidence: analysisResult.supportingEvidence || [],
      contradictingEvidence: analysisResult.contradictingEvidence || [],
      sources: analysisResult.sources || [],
      limitations: analysisResult.limitations || [],
    });

    const savedDoc = await newReport.save();
    return res.status(201).json({ success: true, data: savedDoc });
  } catch (err) {
    return next(err);
  }
};"""
    add_code_block(doc, code_ctrl_verify, "server/src/controllers/verifyController.js")

    # 9. Verification History Controller
    add_heading_2(doc, "9. Verification History Controller (server/src/controllers/historyController.js)")
    code_ctrl_hist = """import { FactCheck } from '../models/FactCheck.js';
import { getDBStatus } from '../config/db.js';

export const getHistory = async (req, res, next) => {
  try {
    const dbStatus = getDBStatus();
    if (!dbStatus.isConnected) {
      return res.status(503).json({ success: false, message: 'MongoDB is not connected.' });
    }

    const { verdict, search, limit = 50 } = req.query;
    const filter = {};

    if (verdict && ['True', 'False', 'Misleading', 'Disputed', 'Unverified'].includes(verdict)) {
      filter.verdict = verdict;
    }

    if (search && typeof search === 'string' && search.trim()) {
      const searchRegex = new RegExp(search.trim(), 'i');
      filter.$or = [
        { claimText: searchRegex },
        { extractedClaim: searchRegex },
      ];
    }

    const records = await FactCheck.find(filter)
      .sort({ createdAt: -1 })
      .limit(Math.min(100, Math.max(1, parseInt(limit, 10) || 50)))
      .lean();

    return res.status(200).json({ success: true, count: records.length, data: records });
  } catch (err) {
    return next(err);
  }
};"""
    add_code_block(doc, code_ctrl_hist, "server/src/controllers/historyController.js")

    # 10. Centralized Error Handling Middleware
    add_heading_2(doc, "10. Error Handling Middleware (server/src/middleware/errorHandler.js)")
    code_err = """export const errorHandler = (err, req, res, next) => {
  console.error('[Error Caught]:', err.stack || err.message);

  let statusCode = res.statusCode !== 200 && res.statusCode !== 201 ? res.statusCode : 500;
  let message = err.message || 'An unexpected internal server error occurred.';

  if (err.name === 'ValidationError') {
    statusCode = 400;
    message = Object.values(err.errors).map(val => val.message).join(', ');
  }

  if (err.name === 'CastError') {
    statusCode = 400;
    message = `Resource not found with id of ${err.value}`;
  }

  return res.status(statusCode).json({
    success: false,
    error: err.name || 'ServerError',
    message,
  });
};"""
    add_code_block(doc, code_err, "server/src/middleware/errorHandler.js")

    # 11. REST API Routing Table
    add_heading_2(doc, "11. REST API Routes (server/src/routes/apiRoutes.js)")
    code_routes = """import { Router } from 'express';
import { getHealthStatus } from '../controllers/healthController.js';
import { verifyClaim } from '../controllers/verifyController.js';
import { getHistory, getReportById } from '../controllers/historyController.js';

const router = Router();

// Health check endpoint
router.get('/health', getHealthStatus);

// Verification endpoint
router.post('/verify', verifyClaim);

// History endpoints
router.get('/history', getHistory);
router.get('/history/:id', getReportById);

export default router;"""
    add_code_block(doc, code_routes, "server/src/routes/apiRoutes.js")

    # 12. Main Server & App Bootstrap
    add_heading_2(doc, "12. Main Server Bootstrap (server/src/app.js & server/src/server.js)")
    code_server = """// server/src/app.js
import express from 'express';
import cors from 'cors';
import { config } from './config/env.js';
import apiRoutes from './routes/apiRoutes.js';
import { errorHandler } from './middleware/errorHandler.js';

const app = express();
app.use(cors({ origin: true, credentials: true }));
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));

app.use('/api', apiRoutes);
app.use(errorHandler);
export default app;

// server/src/server.js
import app from './app.js';
import { config } from './config/env.js';
import { connectDB } from './config/db.js';

const startServer = async () => {
  await connectDB();
  app.listen(config.port, () => {
    console.log(`[ClaimCheck Server] Running on http://localhost:${config.port}`);
  });
};
startServer();"""
    add_code_block(doc, code_server, "server/src/app.js & server/src/server.js")

    # 13. React Root Orchestration
    add_heading_2(doc, "13. React Main Application (client/src/App.jsx)")
    code_react_app = """import React, { useState } from 'react';
import { Navbar } from './components/Navbar.jsx';
import { ClaimForm } from './components/ClaimForm.jsx';
import { CheckingProgress } from './components/CheckingProgress.jsx';
import { ResultCard } from './components/ResultCard.jsx';
import { HistoryList } from './components/HistoryList.jsx';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [verificationState, setVerificationState] = useState('idle'); // idle | loading | result
  const [currentClaim, setCurrentClaim] = useState('');
  const [currentReport, setCurrentReport] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const handleVerifyClaim = async (claimText) => {
    setCurrentClaim(claimText);
    setVerificationState('loading');
    setErrorMsg(null);

    try {
      const response = await fetch('/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ claim: claimText }),
      });
      const result = await response.json();
      if (!response.ok || !result.success) throw new Error(result.message);

      setCurrentReport(result.data);
      setVerificationState('result');
    } catch (err) {
      setErrorMsg(err.message || 'Verification failed.');
      setVerificationState('idle');
    }
  };

  return (
    <div className="app-wrapper">
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="main-content">
        {activeTab === 'home' && verificationState === 'idle' && (
          <ClaimForm onSubmit={handleVerifyClaim} />
        )}
        {activeTab === 'home' && verificationState === 'loading' && (
          <CheckingProgress claim={currentClaim} />
        )}
        {activeTab === 'home' && verificationState === 'result' && (
          <ResultCard report={currentReport} onReset={() => setVerificationState('idle')} />
        )}
        {activeTab === 'history' && <HistoryList />}
      </main>
    </div>
  );
}"""
    add_code_block(doc, code_react_app, "client/src/App.jsx")

    # 14. Claim Submission Form
    add_heading_2(doc, "14. Claim Submission Form (client/src/components/ClaimForm.jsx)")
    code_claimform = """import React, { useState } from 'react';

export const ClaimForm = ({ onSubmit, isLoading }) => {
  const [claim, setClaim] = useState('');
  const [validationError, setValidationError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = claim.trim();
    if (!trimmed) {
      setValidationError('Please enter a claim statement to verify.');
      return;
    }
    if (trimmed.length < 5) {
      setValidationError('Claim must be at least 5 characters long.');
      return;
    }
    onSubmit(trimmed);
  };

  return (
    <div className="card claim-form-card">
      <h2>Verify Any Claim in Real Time</h2>
      <p>Enter any statement, headline, or forwarded message.</p>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={4}
          value={claim}
          onChange={(e) => setClaim(e.target.value)}
          placeholder="e.g. NASA's James Webb Telescope detected atmospheric carbon dioxide on WASP-39b..."
          maxLength={1000}
        />
        {validationError && <p className="error-text">{validationError}</p>}
        <button type="submit" disabled={isLoading} className="btn-primary">
          Verify Claim
        </button>
      </form>
    </div>
  );
};"""
    add_code_block(doc, code_claimform, "client/src/components/ClaimForm.jsx")

    # 15. Progress Tracker State Machine
    add_heading_2(doc, "15. Verification Progress Tracker (client/src/components/CheckingProgress.jsx)")
    code_progress = """import React, { useState, useEffect } from 'react';

const STAGES = [
  { id: 1, title: 'Identifying Main Claim', desc: 'Parsing entities and formulating queries...' },
  { id: 2, title: 'Searching Web Sources', desc: 'Retrieving organic search results via SerpApi...' },
  { id: 3, title: 'Analyzing Evidence', desc: 'Cross-referencing supporting vs contradicting evidence...' },
  { id: 4, title: 'Generating Verdict', desc: 'Evaluating confidence, limitations, and reasoning...' },
];

export const CheckingProgress = ({ claim }) => {
  const [currentStage, setCurrentStage] = useState(1);
  const [secondsElapsed, setSecondsElapsed] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setSecondsElapsed(prev => prev + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (secondsElapsed < 3) setCurrentStage(1);
    else if (secondsElapsed < 7) setCurrentStage(2);
    else if (secondsElapsed < 12) setCurrentStage(3);
    else setCurrentStage(4);
  }, [secondsElapsed]);

  return (
    <div className="card checking-card">
      <div className="spinner"></div>
      <h3>Verifying Claim</h3>
      <p className="preview">"{claim}"</p>
      <div className="stages-list">
        {STAGES.map((st) => (
          <div key={st.id} className={`stage-item ${st.id <= currentStage ? 'active' : ''}`}>
            <span>{st.id < currentStage ? '✓' : st.id === currentStage ? '⏳' : '○'}</span>
            <strong>{st.title}</strong> - {st.desc}
          </div>
        ))}
      </div>
    </div>
  );
};"""
    add_code_block(doc, code_progress, "client/src/components/CheckingProgress.jsx")

    # 16. Verdict Badge & Result Display
    add_heading_2(doc, "16. Verdict Display & Evidence Card (client/src/components/ResultCard.jsx)")
    code_result = """import React from 'react';
import { VerdictBadge } from './VerdictBadge.jsx';

export const ResultCard = ({ report, onReset }) => {
  if (!report) return null;
  const { claimText, verdict, confidence, explanation, supportingEvidence, contradictingEvidence, sources } = report;

  return (
    <div className="result-container">
      <div className="card result-header">
        <VerdictBadge verdict={verdict} />
        <h2>{verdict.toUpperCase()} ({confidence}% Confidence)</h2>
        <p className="claim-quote">"{claimText}"</p>
        <p className="explanation">{explanation}</p>
      </div>

      <div className="evidence-grid">
        <div className="evidence-card supporting">
          <h3>Supporting Evidence</h3>
          {supportingEvidence.map((pt, i) => <p key={i}>• {pt}</p>)}
        </div>
        <div className="evidence-card contradicting">
          <h3>Contradicting Evidence</h3>
          {contradictingEvidence.map((pt, i) => <p key={i}>• {pt}</p>)}
        </div>
      </div>

      <div className="sources-card">
        <h3>Verified Web Citations</h3>
        {sources.map((src, i) => (
          <div key={i} className="source-item">
            <a href={src.url} target="_blank" rel="noreferrer">{src.title}</a>
            <p>{src.snippet}</p>
          </div>
        ))}
      </div>
      <button onClick={onReset} className="btn-secondary">Check Another Claim</button>
    </div>
  );
};"""
    add_code_block(doc, code_result, "client/src/components/ResultCard.jsx")

    # 17. REST API Request and Response Examples
    add_heading_2(doc, "17. REST API Request and Response Examples")
    code_api_sample = """// Request: POST /api/verify
// Headers: Content-Type: application/json
{
  "claim": "NASA discovered alien life on Mars in October 2026"
}

// Response: HTTP 201 Created
{
  "success": true,
  "data": {
    "id": "67084920b7e49281a8b12345",
    "claimText": "NASA discovered alien life on Mars in October 2026",
    "extractedClaim": "NASA officially confirmed discovery of extraterrestrial life on Mars.",
    "entities": ["NASA", "Mars", "October 2026"],
    "verdict": "False",
    "confidence": 96,
    "explanation": "No scientific announcement or peer-reviewed publication confirms discovery of extraterrestrial life on Mars. Official NASA rover missions report no such findings.",
    "supportingEvidence": [],
    "contradictingEvidence": [
      "NASA official astrobiology releases report no signs of extraterrestrial life.",
      "International astronomical unions confirm lack of peer-reviewed corroboration."
    ],
    "sources": [
      {
        "title": "NASA Mars Exploration Program Overview",
        "url": "https://mars.nasa.gov",
        "snippet": "Current missions including Perseverance continue investigating past habitability, with no life found.",
        "date": "2026",
        "relevance": "Primary Institutional Source"
      }
    ],
    "limitations": [],
    "createdAt": "2026-10-10T09:45:00.000Z"
  }
}"""
    add_code_block(doc, code_api_sample, "POST /api/verify Sample Payload")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # SCREENSHOTS OF THE PROJECT
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "SCREENSHOTS OF THE PROJECT")

    add_body_p(doc, "The ClaimCheck web application features a clean, responsive graphical user interface developed with React 19 and Vite. The design language employs a cohesive palette of deep blues, teals, and light background cards to provide immediate visual clarity during high-stakes fact checking. Below are representative interface screenshots illustrating the submission interface, live multi-stage verification state machine, calibrated verdict report card, and source citation inspector:")

    add_image_figure(doc, "screenshots.png", "Figure 16.1 & 16.2: Claim Submission Form, Verification Progress State Machine, and Calibrated Report Inspector", 6.2)

    add_body_p(doc, "Figure 16.1 depicts the initial claim input view, where users can type any assertion or select pre-configured sample claims spanning space exploration, viral health rumors, science, and historical events. Upon clicking 'Verify Claim', the interface dynamically transitions into the live verification state machine, displaying real-time feedback as the backend queries Google Gemini for claim parsing, executes live Google Search queries via SerpApi, cross-references evidence snippets, and commits the final report into MongoDB.")

    add_body_p(doc, "Figure 16.2 illustrates the completed fact-check result view for a viral claim. The prominent False badge and 96% confidence score provide instant, unambiguous clarity. Below the main verdict, the report itemizes the authoritative explanation, highlights discrete contradicting points, and displays direct links to primary institutional sources, ensuring that the verdict is fully transparent, reproducible, and verifiable.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # REFERENCES
    # ---------------------------------------------------------------------------
    add_heading_1(doc, "REFERENCES")

    references = [
        ("[1] ", "A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, \"Attention is all you need,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998-6008, 2017."),
        ("[2] ", "P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, \"Retrieval-augmented generation for knowledge-intensive NLP tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459-9474, 2020."),
        ("[3] ", "Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung, \"Survey of hallucination in natural language generation,\" ACM Computing Surveys, vol. 55, no. 12, pp. 1-38, 2023."),
        ("[4] ", "J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal, \"FEVER: a large-scale dataset for fact extraction and VERification,\" in Proc. of NAACL-HLT, pp. 809-819, 2018."),
        ("[5] ", "Google DeepMind, \"Gemini: A family of highly capable multimodal models,\" Technical Report, Google, 2023. Available: https://deepmind.google/technologies/gemini/"),
        ("[6] ", "Google GenAI SDK Documentation, \"Google GenAI SDK for Node.js and TypeScript,\" 2024. [Online]. Available: https://github.com/googleapis/genai-js"),
        ("[7] ", "SerpApi Documentation, \"Google Search API - Real-time SERP scraper and parsing service,\" 2024. [Online]. Available: https://serpapi.com/search-api"),
        ("[8] ", "MongoDB Inc., \"MongoDB Community Server and Mongoose ODM Documentation,\" 2024. [Online]. Available: https://www.mongodb.com/docs/"),
        ("[9] ", "Express.js Development Team, \"Express - Fast, unopinionated, minimalist web framework for Node.js,\" 2024. [Online]. Available: https://expressjs.com/"),
        ("[10] ", "React Core Team, \"React 19 Documentation: Declarative, Component-Based UI Development,\" 2024. [Online]. Available: https://react.dev/"),
        ("[11] ", "E. Graves, \"Deciding what’s true: The rise of political fact-checking in American journalism,\" Columbia Journalism Review, Columbia University Press, 2016."),
        ("[12] ", "C. Wardle and H. Derakhshan, \"Information Disorder: Toward an interdisciplinary framework for research and policymaking,\" Council of Europe Report, DGI(2017)09, 2017.")
    ]

    for ref_num, ref_text in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.3
        p_ref.paragraph_format.space_after = Pt(6)
        r_num = p_ref.add_run(ref_num)
        r_num.font.bold = True
        r_num.font.size = Pt(11)
        r_txt = p_ref.add_run(ref_text)
        r_txt.font.size = Pt(11)

    output_path = "ClaimCheck_Project_Report.docx"
    doc.save(output_path)
    print(f"Document successfully created at {output_path}")

if __name__ == '__main__':
    generate_report()
