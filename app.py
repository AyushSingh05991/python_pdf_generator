from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from datetime import date

app = Flask(__name__)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('Sans', '', os.path.join('fonts', 'font.ttf'), uni=True)
        self.add_font('Montserrat', '', os.path.join('fonts', 'font.ttf'), uni=True)
        self.set_text_color(0, 0, 0)

    def header(self):
        if self.page_no() == 1:  # Only show logo on the first page
            self.set_fill_color(255, 255, 255)
            self.rect(0, 0, self.w, self.h, 'F')
            self.image("static/logo.png", 5, 5, 30)
            self.set_y(5)
            self.set_x(25)
            self.set_font('Sans', '', 12)
            self.cell(0, 10, "Programmer_Deepak", border=0, ln=True, align='C')

    def footer(self):
        self.set_y(-15)  # Position the footer 15 mm from the bottom
        self.set_font('Sans', '', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
current_date = date.today().strftime("%d-%m-%Y")
        


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the form data
        subject_name = request.form.get("subject_name")
        chapter_name = request.form.get("chapter_name")
        headings = request.form.getlist("heading")
        contents = request.form.getlist("content")

        # Get the current date
        current_date = date.today().strftime("%d-%m-%Y")

        # Create PDF instance
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Sans', '', 11)

        # Add subject and chapter name
        pdf.cell(0, 10, f"Subject: {subject_name}", ln=True, align='C')
        pdf.cell(0, 10, f"Chapter: {chapter_name}", ln=True, align='C')
        pdf.cell(0, 10, f"Date: {current_date}", ln=True, align='R')  # Add the current date
        pdf.ln(10)  # Line break

        # Add headings and content
        for heading, content in zip(headings, contents):
            # Add prefix before heading
            pdf.set_font('Sans', '', 11)
            pdf.cell(10, 10, ">>", ln=False)
            pdf.cell(0, 10, heading, ln=True)

            # Add content points
            pdf.set_font('Montserrat', '', 8)
            content_points = content.split('\n')
            for point in content_points:
                pdf.cell(0, 10, f'> {point}', ln=True)

        # Save the PDF file with the chapter name as file name
        pdf_output = f"{subject_name}_{chapter_name}_Notes.pdf"
        pdf_output_path = os.path.join(os.getcwd(), pdf_output)

        # Save PDF to file
        with open(pdf_output_path, 'wb') as f:
            f.write(pdf.output(dest='S').encode('latin1'))

        # Send the generated PDF for download
        return send_file(pdf_output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
