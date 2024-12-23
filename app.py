
import base64
from flask import Flask, render_template, request, jsonify, url_for
import random
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from the .env file
load_dotenv()

# Now you can access environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

app = Flask(__name__)

# List of racing images (static image paths)
RACING_IMAGES = [
    "static/images/racing1.jpg",
    "static/images/racing2.jpg",
    "static/images/racing3.jpg"
]

def send_email(pdf, filename, recipient_email):
    # Convert the PDF binary data to base64
    pdf_base64 = base64.b64encode(pdf).decode('utf-8')  # Convert bytes to base64 string
    
    # Create the email message
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient_email,
        subject='Your Certificate of Participation from 5km Running Competiotion',
        html_content='<strong>Please find attached 5km Running Competion Certificate of Participation.</strong>'
    )

    # Create the attachment with base64-encoded PDF data
    attachment = Attachment(
        FileContent(pdf_base64),  # Base64-encoded file content
        FileName(filename),  # File name
        FileType('application/pdf'),  # MIME type
        Disposition('attachment')  # The disposition type (attachment)
    )

    # Add the attachment to the email
    message.add_attachment(attachment)

    # Send the email using SendGrid API
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent successfully to {recipient_email}!")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"Error sending email: {e}")

def convert_html_to_pdf_via_pdfshift(html_content):
    try:
        response = requests.post(
            'https://api.pdfshift.io/v3/convert/pdf',
            auth=('api', os.getenv('PDFSHIFT_API_KEY')),  # Using API key from .env file
            json={
                "source": html_content,  # HTML content directly
                "landscape": False,
                "use_print": False
            }
        )
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

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

    # Generate PDF from HTML using PDFShift API
    pdf_content = convert_html_to_pdf_via_pdfshift(rendered_html)
    
    if pdf_content:
        pdf_filename = f"{name}_certificate.pdf"
        pdf_folder_path = 'static/certificates'  # Folder to store certificates
        os.makedirs(pdf_folder_path, exist_ok=True)  # Ensure folder exists
        pdf_path = os.path.join(pdf_folder_path, pdf_filename)

        # Save the certificate to a file (optional)
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)
        print(f"Certificate saved to {pdf_path}")

        # Send the email with the PDF attached
        send_email(pdf_content, pdf_filename, recipient_email)

        # Redirect to the download page with the certificate path
        return render_template('certificate.html', certificate_url=url_for('static', filename=f'certificates/{pdf_filename}'))
    else:
        return jsonify({"error": "Failed to generate PDF"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the port from environment variables or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
