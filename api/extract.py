from oletools.olevba import VBA_Parser # type: ignore
import google.generativeai as genai # type: ignore
import os
from dotenv import load_dotenv # type: ignore
import json
import re
from Flowchart import draw_flowchart
import ast

file = "Download-Sample-File-xlsm.xlsm"


vba_parser = VBA_Parser(file)
if vba_parser.detect_vba_macros():
    vba = ''
    for (filename, stream_path, vba_filename, vba_code) in vba_parser.extract_macros():
        vba += f"Filename: {filename}\n"
        vba += f"Stream Path: {stream_path}\n"
        vba += f"VBA Filename: {vba_filename}\n"
        vba += f"VBA Code:\n{vba_code}\n\n"
else:
    print("No VBA macros found.")

vba_code = vba


load_dotenv()
genai.configure(api_key= os.getenv("GEMINI_API"))

model = genai.GenerativeModel('gemini-1.5-flash')


prompt = """I need assistance in analyzing VBA macros. Specifically, I'd like to extract the following information:

Functional Logic: Describe the core functionalities embedded within the VBA macros. This should explain what the macros are designed to achieve.

Documented VBA Code: Document the entire VBA code and output the code with documentation

Logic Flowchart: Produce me a flowchart component list where the vba function is being read, the logic is being extracted has loops, decisions, processes and the start/end. A dictionary has to be produced where the keys must be loops, decisions, processes and the start/end and the values must be nodes that are derived from the vba function being read(Name the nodes in terms of logic and not as present in function).Create edges as a list of tuples among the nodes where first node is the source and the second is the destination.

Security Check: Check the macros for security vulnerabilities

Code Efficiency: Check for codes efficiency i.e., is there a more efficient solution and give us the most efficient function code.

Python translation: Translate the vba function into a python code snippet.

Output:

Please provide the extracted information in the text format not in JSON. It should have the following fields:

ADD AN !-------------- DELIMITER
functionalLogic: Text description of the macro's functionalities.
ADD AN !-------------- DELIMITER
documented_code: Documented VBA code.
ADD AN !-------------- DELIMITER
logic_flowchart: Produce me the dictionary where keys must strictly be loops, decisions, processes and the start/end and the values are the nodes identified from the vba code(Name the nodes in terms of logic and not as present in function). And edges as a list of tuples where the first node is the source and the second node is the destination.
Important Note : IF MORE THAN 1 VALUE IS PRESENT FOR A KEY THEN PRODUCE THE VALUES AS A LIST.
Important Note : ADD <-----------------------> DELIMITER BETWEEN COMPONENT DICTIONARY AND EDGE LIST  
ADD AN !-------------- DELIMITER
security_vulnerabilities: yes if vulnerabilities exists, no if it doesn't exist
ADD AN !-------------- DELIMITER
code_efficiency: produce the code for the most efficient code if more efficient code exists, else produce the same code
ADD AN !-------------- DELIMITER
python_code: produce the python code snippet of the vba code given
ADD AN !-------------- DELIMITER

Important Note : ONLY OUTPUT THE REQUESTED FORMAT NOTHING ELSE IS REQUIRED. 
Avoid:
Including unnecessary conversational phrases like "I'm going to" or greetings.
Mentioning irrelevant details like extracting code or performing actions beyond analysis.

"""

response = model.generate_content(vba_code+prompt)

#print(response.text)

def split_sections(input_string):
    sections = input_string.split("!--------------")
    headings = ["Functional Logic", "Documented code", "Logic-Flowchart", "Security Vulnerabilities", "Code Efficiency", "Python code"]
    
    section_dict = {}
    
    for heading in headings:
        for section in sections:
            if section.strip().startswith(heading):
                section_content = section.strip().replace(f"{heading}:", "", 1).strip()
                section_dict[heading] = section_content
                break
    
    return section_dict

parsed_dict = split_sections(response.text)

print(parsed_dict['Logic-Flowchart'])

def parse_flowchart_string(flowchart_str):
    components,edges = flowchart_str.split('<----------------------->')
    components = components.strip()
    edges = edges.strip()

    components = ast.literal_eval(components)

    edges = ast.literal_eval(edges)

    return components, edges

components,edges = parse_flowchart_string(parsed_dict['Logic-Flowchart'])

draw_flowchart(components=components,edges=edges)