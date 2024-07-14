from flask import Flask, request, jsonify
from oletools.olevba import VBA_Parser  # type: ignore
from flask_cors import CORS  # Import CORS
import google.generativeai as genai  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore
import re
from Flowchart import draw_flowchart
import ast
import tempfile

app = Flask(__name__)
CORS(app)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API"))

model = genai.GenerativeModel('gemini-1.5-flash')

def split_sections(input_string):
    sections = input_string.split("!--------------")
    headings = ["functionalLogic", "documented_code", "logic_flowchart", "security_vulnerabilities", "code_efficiency","macro_dependency","Error_detector_corrector","Process_optimizer","python_code"]

    section_dict = {}

    for heading in headings:
        for section in sections:
            if section.strip().startswith(heading):
                section_content = section.strip().replace(f"{heading}:", "", 1).strip()
                section_dict[heading] = section_content
                break

    return section_dict

def parse_flowchart_string(flowchart_str):
    components, edges = flowchart_str.split('<----------------------->')
    components = components.strip()
    edges = edges.strip()

    components = ast.literal_eval(components)
    edges = ast.literal_eval(edges)

    return components, edges

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsm') as tmp:
            file_path = tmp.name
            file.save(file_path)

        vba_parser = VBA_Parser(file_path)
        if vba_parser.detect_vba_macros():
            vba = ''
            for (filename, stream_path, vba_filename, vba_code) in vba_parser.extract_macros():
                vba += f"Filename: {filename}\n"
                vba += f"Stream Path: {stream_path}\n"
                vba += f"VBA Filename: {vba_filename}\n"
                vba += f"VBA Code:\n{vba_code}\n\n"
        else:
            return jsonify({'error': 'No VBA macros found.'}), 400

        vba_code = vba
        prompt = """I need assistance in analyzing VBA macros. Specifically, I'd like to extract the following information:

Functional Logic: Describe the core functionalities embedded within the VBA macros. This should explain what the macros are designed to achieve.

Documented VBA Code: Document the entire VBA code and output the code with documentation

Logic Flowchart: Produce me a flowchart component list where the vba function is being read, the logic is being extracted has loops, decisions, processes and the start/end. A dictionary has to be produced where the keys must be loops, decisions, processes and the start/end and the values must be nodes that are derived from the vba function being read(Name the nodes in terms of logic and not as present in function).Create edges as a list of tuples among the nodes where first node is the source and the second is the destination.

Security Check: Check the macros for security vulnerabilities

Code Efficiency: Check for codes efficiency i.e., is there a more efficient solution and give us the most efficient function code.

Macro Dependency Mapper: Analyse the vba code recommend the dependency of the macros code and which will suit the macros better.

Error Detection and Correction: Analyse the code detect the errors in the code and produce and corrected code if error exists, else generate the code as it is.

Process Optimizer: Analyse the function and produce a description on the current data flow and how it can the process be optimized

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
macro_dependency: Give us a description of the dependency of the macros vba code
ADD AN !-------------- DELIMITER
Error_detector_corrector: Check for errors in the vba code, if errors exist give us the corrected code else produce the code as it is
ADD AN !-------------- DELIMITER
Process_optimizer: Analyse the function process and give a description on how the current process is working and how it can be optimized
ADD AN !-------------- DELIMITER
python_code: produce the python code snippet of the vba code given
ADD AN !-------------- DELIMITER

Important Note : ONLY OUTPUT THE REQUESTED FORMAT NOTHING ELSE IS REQUIRED. 
Avoid:
Including unnecessary conversational phrases like "I'm going to" or greetings.
Mentioning irrelevant details like extracting code or performing actions beyond analysis.

"""

        response = model.generate_content(vba_code + prompt)

        parsed_dict = split_sections(response.text)
        components, edges = parse_flowchart_string(parsed_dict['logic_flowchart'])

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
            image_path = tmp_img.name
            draw_flowchart(components=components, edges=edges)

        return jsonify(parsed_dict)

    return jsonify({'error': 'File processing error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
