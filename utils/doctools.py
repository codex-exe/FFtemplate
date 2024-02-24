import json, re
from datetime import datetime, timezone
from fpdf import FPDF

def load_template():
    '''Loading the predefined document template'''
    with open('static/template.json', 'r') as file:
        template = json.load(file)
    return template

def new_doc(id):
    '''Creating a new document session by resetting the document'''
    doc = load_template()
    doc["FixID"] = id
    doc["DocumentLastUpdate"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open('cache/document.json', 'w') as file:
        file.write(json.dumps(doc, indent=4))
    return "New document has been created."

def load_doc():
    '''Loading the document from cache'''
    with open('cache/document.json', 'r') as file:
        doc = json.load(file)
    return doc

def update_doc(**kwargs):
    '''Updating the document with the given arguments'''
    if 'args' in kwargs.keys():
        kwargs = kwargs['args']
    doc = load_doc()
    doc.update(kwargs)
    doc["DocumentLastUpdate"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open('cache/document.json', 'w') as file:
        file.write(json.dumps(doc, indent=4))
    values = list(kwargs.keys())
    return f"{values} Updated!"

def load_tools():
    '''Loading the predefined chatbot tools'''
    with open('static/tools.json', 'r') as file:
        tools = json.load(file)
    return tools

class PDF(FPDF):
    temp = {
        "FixID": "",
        "DocumentLastUpdate": "",
        "Title": "",
        "Type": "",
        "Author": "",
        "Status": "",
        "SeverityLevel": "",
        "SkillLevel": "",
        "LevelOfEffort": "",
    }
    def header(self):
        self.image(r'utils/logo.png', 10, 10, 15)
        self.set_font('Arial', style='B', size=15)
        self.cell(80)
        self.cell(w=30,h=12, txt=self.temp['FixID'], align='C')
        self.set_font('Arial', size=10)
        self.set_text_color(128)
        self.cell(w=85,h=5, txt=self.temp["DocumentLastUpdate"], align='R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', style='I', size=8)
        self.set_text_color(128)
        self.cell(w=0, h=10, txt='Page ' + str(self.page_no()) + '/{nb}', border=0, ln=0, align='C')

    def metadata(self):
        self.set_font('Arial', size=12, style='B')
        self.multi_cell(w=0, h=10, txt=self.temp['Title'], align='C', border=1)
        self.ln(10)

        self.set_font('Arial', style='B', size=10)
        self.cell(w=10, h=10, txt="Type:", ln=0, align='L')
        self.set_font('Arial', size=10)
        self.cell(w=69, h=10, txt=self.temp['Type'], ln=0, align='L')

        self.set_font('Arial', style='B', size=10)
        self.cell(w=10, h=10, txt="Author:", ln=0, align='C')
        self.set_font('Arial', size=10)
        self.cell(w=30, h=10, txt=self.temp['Author'], ln=0, align='C')

        self.set_font('Arial', style='B', size=10)
        self.cell(w=50, h=10, txt="Status:", ln=0, align='R')
        self.set_font('Arial', size=10)
        self.cell(w=9, h=10, txt=self.temp['Status'], ln=1, align='R')

        self.set_font('Arial', style='B', size=10)
        self.cell(w=25, h=10, txt="Severity Level:", ln=0, align='L')
        self.set_font('Arial', size=10)
        self.cell(w=58, h=10, txt=self.temp['SeverityLevel'], ln=0, align='L')

        self.set_font('Arial', style='B', size=10)
        self.cell(w=8, h=10, txt="Skill Level:", ln=0, align='C')
        self.set_font('Arial', size=10)
        self.cell(w=21, h=10, txt=self.temp['SkillLevel'], ln=0, align='C')

        self.set_font('Arial', style='B', size=10)
        self.cell(w=60, h=10, txt="Level of Effort:", ln=0, align='R')
        self.set_font('Arial', size=10)
        self.cell(w=13, h=10, txt=self.temp['LevelOfEffort'], ln=1, align='R')
        
    def section(self, param):
        self.set_font('Arial', style='B', size=10)
        self.set_fill_color(200, 220, 255)
        self.cell(w=0, h=10, txt=param, ln=1, align='L', fill=1)
        self.ln(2)
        self.set_font('Arial', size=10)
        self.multi_cell(w=0, h=5, txt=self.temp[param], align='L')
        self.ln(2)

    def list_entry(self, param):
        self.set_font('Arial', style='B', size=10)
        self.set_fill_color(200, 220, 255)
        self.cell(w=0, h=10, txt=param, ln=1, align='L', fill=1)
        self.ln(2)
        def is_link(text):
            pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
            return re.match(pattern, text)
        for i in self.temp[param]:
            self.set_fill_color(0)
            self.rect(15, self.get_y() + 1.5, 1.5, 1.5, 'F')
            self.cell(8)
            self.set_font('Arial', size=8)
            if is_link(i):
                self.set_font('Arial', size=8, style='U')
                self.set_text_color(0, 0, 255)
                self.cell(w=0,h=5, txt=i, align='L', link=i)
            else:
                self.multi_cell(w=0,h=5, txt=i, align='L')
            self.ln(5) 
