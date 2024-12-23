# from flask import Flask, render_template, request, send_file, redirect, url_for
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from PIL import Image
# import io
# import qrcode
# import random
# import tempfile  # To create temporary files

# app = Flask(__name__)

# # List of racing images (you can customize this with your own racing image URLs or paths)
# RACING_IMAGES = [
#     "static/images/racing1.jpg",
#     "static/images/racing2.jpg",
#     "static/images/racing3.jpg"
# ]

# # Function to generate QR Code
# def generate_qr_code(data):
#     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
#     qr.add_data(data)
#     qr.make(fit=True)
#     img = qr.make_image(fill="black", back_color="white")
#     qr_code_buffer = io.BytesIO()
#     img.save(qr_code_buffer)
#     qr_code_buffer.seek(0)
#     return qr_code_buffer

# # Function to generate certificate PDF
# def generate_certificate(name, course, date):
#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)

#     # Background image (e.g., a racing-themed image)
#     racing_image = random.choice(RACING_IMAGES)
#     c.drawImage(racing_image, 50, 400, width=500, height=200)  # Adjust position and size as needed

#     # Title
#     c.setFont("Helvetica", 24)
#     c.setFillColor(colors.red)
#     c.drawString(100, 700, "Certificate of Completion")

#     # Certificate details
#     c.setFont("Helvetica", 16)
#     c.setFillColor(colors.black)
#     c.drawString(100, 650, f"This is to certify that {name}")
#     c.drawString(100, 630, f"has completed the {course} course.")
#     c.drawString(100, 610, f"Date: {date}")

#     # Generate QR code and place it on the certificate
#     qr_data = f"Certificate for {name} - {course} - {date}"
#     qr_code_buffer = generate_qr_code(qr_data)
    
#     # Create a temporary file for QR code
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
#         qr_code_buffer.seek(0)
#         temp_file.write(qr_code_buffer.read())
#         qr_code_path = temp_file.name  # Save the path for later use

#     # Use the saved file path for the QR code image
#     c.drawImage(qr_code_path, 400, 100, width=100, height=100)  # Adjust position and size as needed

#     c.save()
#     buffer.seek(0)
#     return buffer

# # Home page to scan QR code and input details
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Handle form submission, generate certificate and show preview
# @app.route('/generate_certificate', methods=['POST'])
# def generate():
#     name = request.form['name']
#     course = request.form['course']
#     date = request.form['date']

#     # Generate certificate PDF
#     certificate_pdf = generate_certificate(name, course, date)

#     # Save the certificate to a file (optional)
#     certificate_filename = "static/certificates/certificate.pdf"
#     with open(certificate_filename, 'wb') as f:
#         f.write(certificate_pdf.read())

#     # Redirect to a confirmation page with the link to download the certificate
#     return render_template('certificate.html', certificate_filename=certificate_filename)

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)










# from flask import Flask, render_template, request, send_file, url_for, make_response
# import pdfkit
# import random
# import os

# app = Flask(__name__)

# # List of racing images (static image paths)
# RACING_IMAGES = [
#     "static/images/racing1.jpg",
#     "static/images/racing2.jpg",
#     "static/images/racing3.jpg"
# ]

# # Path to wkhtmltopdf executable (update this if wkhtmltopdf is not in PATH)
# WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# # Home page to input details
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Generate certificate route
# @app.route('/generate_certificate', methods=['POST'])
# def generate_certificate():
#     name = request.form['name']
#     course = request.form['course']

#     # Choose a random racing image for the certificate
#     racing_image = random.choice(RACING_IMAGES)

#     # Render the certificate HTML template
#     rendered_html = render_template(
#         'certificate_template.html',
#         name=name,
#         course=course,
#         racing_image=url_for('static', filename=racing_image)
#     )

#     # Configure pdfkit with the path to wkhtmltopdf
#     config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

#     # Add options to allow local file access
#     options = {
#         'enable-local-file-access': None
#     }

#     # Generate PDF from HTML
#     pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)

#     # Return the PDF as a downloadable response
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename={name}_certificate.pdf'
#     return response

# if __name__ == '__main__':
#     app.run(debug=True)











# from flask import Flask, render_template, request, make_response, url_for
# import pdfkit
# import random
# import os
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
# from email.mime.text import MIMEText

# app = Flask(__name__)

# # List of racing images (static image paths)
# RACING_IMAGES = [
#     "static/images/racing1.jpg",
#     "static/images/racing2.jpg",
#     "static/images/racing3.jpg"
# ]

# # Path to wkhtmltopdf executable (update this if wkhtmltopdf is not in PATH)
# WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# # SMTP server settings (you can use Gmail or another SMTP service)
# SMTP_SERVER = 'sandbox.smtp.mailtrap.io'  # Change to your email provider's SMTP server
# SMTP_PORT = 2525  # Common port for Gmail
# SENDER_EMAIL = 'dharmabhai18@gmail.com'  # Your email address
# SENDER_PASSWORD = 'b8f49bba22a9b2'  # Your email password (use app password if needed)

# # Home page to input details
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Function to send email with the attachment
# def send_email(pdf, filename, recipient_email):
#     # Create the email message
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = recipient_email
#     msg['Subject'] = 'Your Certificate of Completion'

#     # Add the body of the email
#     body = MIMEText("Please find attached your Certificate of Completion.", 'plain')
#     msg.attach(body)

#     # Attach the PDF certificate
#     attachment = MIMEApplication(pdf, _subtype='pdf')
#     attachment.add_header('Content-Disposition', 'attachment', filename=filename)
#     msg.attach(attachment)

#     # Connect to the SMTP server and send the email
#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()  # Secure the connection
#             server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in to the email account
#             server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # Send the email
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Error sending email: {e}")

# # Generate certificate route
# @app.route('/generate_certificate', methods=['POST'])
# def generate_certificate():
#     name = request.form['name']
#     course = request.form['course']
#     recipient_email = request.form['recipient_email']  # Get recipient email from the form

#     # Choose a random racing image for the certificate
#     racing_image = random.choice(RACING_IMAGES)

#     # Render the certificate HTML template
#     rendered_html = render_template(
#         'certificate_template.html',
#         name=name,
#         course=course,
#         racing_image=url_for('static', filename=racing_image)
#     )

#     # Configure pdfkit with the path to wkhtmltopdf
#     config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

#     # Add options to allow local file access
#     options = {
#         'enable-local-file-access': None
#     }

#     # Generate PDF from HTML
#     pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)

#     # Generate the PDF filename
#     pdf_filename = f"{name}_certificate.pdf"

#     # Send email with PDF attachment
#     send_email(pdf, pdf_filename, recipient_email)

#     # Return the PDF as a downloadable response
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename={pdf_filename}'
#     return response

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, make_response, url_for
import pdfkit
import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

app = Flask(__name__)

# List of racing images (static image paths)
RACING_IMAGES = [
    "static/images/racing1.jpg",
    "static/images/racing2.jpg",
    "static/images/racing3.jpg"
]

# Path to wkhtmltopdf executable (update this if wkhtmltopdf is not in PATH)
WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# SMTP server settings (you can use Gmail or another SMTP service)
SMTP_SERVER = 'sandbox.smtp.mailtrap.io'  # Change to your email provider's SMTP server
SMTP_PORT = 2525  # Common port for Gmail
SENDER_EMAIL = 'dharmabhai18@gmail.com'  # Your email address
SENDER_PASSWORD = 'b8f49bba22a9b2'  # Your email password (use app password if needed)

# Home page to input details
@app.route('/')
def index():
    return render_template('index.html')

# Function to send email with the attachment
def send_email(pdf, filename, recipient_email):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = 'Your Certificate of Completion'

    # Add the body of the email
    body = MIMEText("Please find attached your Certificate of Completion.", 'plain')
    msg.attach(body)

    # Attach the PDF certificate
    attachment = MIMEApplication(pdf, _subtype='pdf')
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in to the email account
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # Send the email
        print(f"Email sent successfully to {recipient_email}!")
    except Exception as e:
        print(f"Error sending email: {e}")


# @app.route('/generate_certificate', methods=['POST'])
# def generate_certificate():
#     name = request.form['name']
#     course = request.form['course']
#     recipient_email = request.form['recipient_email']  # Get recipient email from the form

#     # Choose a random racing image for the certificate
#     racing_image = random.choice(RACING_IMAGES)

#     # Render the certificate HTML template
#     rendered_html = render_template(
#         'certificate_template.html',
#         name=name,
#         course=course,
#         racing_image=url_for('static', filename=racing_image)
#     )

#     # Configure pdfkit with the path to wkhtmltopdf
#     config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

#     # Add options to allow local file access
#     options = {
#         'enable-local-file-access': None
#     }

#     # Generate PDF from HTML
#     pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)

#     # Generate the PDF filename and path
#     pdf_filename = f"{name}_certificate.pdf"
#     pdf_folder_path = 'static/certificates'  # Folder to store certificates
#     os.makedirs(pdf_folder_path, exist_ok=True)  # Ensure folder exists
#     pdf_path = os.path.join(pdf_folder_path, pdf_filename)

#     # Save the certificate to a file (optional)
#     with open(pdf_path, 'wb') as f:
#         f.write(pdf)
#     print(f"Certificate saved to {pdf_path}")

#     # Return the PDF as a downloadable response
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename={pdf_filename}'

#     return response

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    name = request.form['name']
    course = request.form['course']
    recipient_email = request.form['recipient_email']  # Get recipient email from the form

    # Choose a random racing image for the certificate
    racing_image = random.choice(RACING_IMAGES)

    # Render the certificate HTML template
    rendered_html = render_template(
        'certificate_template.html',
        name=name,
        course=course,
        racing_image=url_for('static', filename=racing_image)
    )

    # Configure pdfkit with the path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

    # Add options to allow local file access
    options = {
        'enable-local-file-access': None
    }

    # Generate PDF from HTML
    pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)

    # Generate the PDF filename and path
    pdf_filename = f"{name}_certificate.pdf"
    pdf_folder_path = 'static/certificates'  # Folder to store certificates
    os.makedirs(pdf_folder_path, exist_ok=True)  # Ensure folder exists
    pdf_path = os.path.join(pdf_folder_path, pdf_filename)

    # Save the certificate to a file (optional)
    with open(pdf_path, 'wb') as f:
        f.write(pdf)
    print(f"Certificate saved to {pdf_path}")

    # Redirect to the download page with the certificate path
    return render_template('certificate.html', certificate_url=url_for('static', filename=f'certificates/{pdf_filename}'))



# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)

