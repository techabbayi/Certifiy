from flask import Flask, render_template, request, make_response, url_for
import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from weasyprint import HTML  # Import WeasyPrint

app = Flask(__name__)

# List of racing images (static image paths)
RACING_IMAGES = [
    "static/images/racing1.jpg",
    "static/images/racing2.jpg",
    "static/images/racing3.jpg"
]

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

    # Generate PDF from HTML using WeasyPrint
    pdf = HTML(string=rendered_html).write_pdf()

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
