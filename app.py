from flask import Flask, render_template, request, send_file, redirect, url_for
from fpdf import FPDF
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = '16kudixit@gmail.com'
EMAIL_PASSWORD = 'tfyg ikir iisk yslm'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(to_email, file_data):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = 'Your Basketball Game Report'

    body = 'Please find attached the basketball game report you requested.'
    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(file_data)
    encoders.encode_base64(attachment)
    attachment.add_header(
        'Content-Disposition',
        'attachment; filename="report.pdf"',
    )
    msg.attach(attachment)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    player_name = request.form.get('player_name')
    game_date = request.form.get('game_date')
    teams_playing = request.form.get('teams_playing')
    free_throws_made = int(request.form.get('free_throws_made', 0))
    free_throws_attempted = int(request.form.get('free_throws_attempted', 0))
    two_pointers_made = int(request.form.get('two_pointers_made', 0))
    two_pointers_attempted = int(request.form.get('two_pointers_attempted', 0))
    three_pointers_made = int(request.form.get('three_pointers_made', 0))
    three_pointers_attempted = int(request.form.get('three_pointers_attempted', 0))
    total_points = int(request.form.get('total_points', 0))
    steals = int(request.form.get('steals', 0))
    blocks = int(request.form.get('blocks', 0))
    turnovers = int(request.form.get('turnovers', 0))
    total_time = float(request.form.get('total_time', 0))

    fg_percentage = (total_field_goals_made / (total_field_goals_attempted or 1)) * 100
    fg_percentage_ft = (total_free_throws_made / (total_free_throws_attempted or 1)) * 100
    fg_percentage_2pt = (two_pointers_made / (two_pointers_attempted or 1)) * 100
    fg_percentage_3pt = (three_pointers_made / (three_pointers_attempted or 1)) * 100
    points_per_minute = total_points / (total_time or 1)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    text = (
        f"Basketball Game Report\n\n"
        f"Player: {player_name}\n"
        f"Game Date: {game_date}\n"
        f"Teams Playing: {teams_playing}\n\n"
        f"STATS:\n"
        f"Total Points: {total_points}\n"
        f"Field Goal Percentage: {fg_percentage:.2f}%\n"
        f"Field Goal Percentage Free Throw: {fg_percentage_ft:.2f}%\n"
        f"Field Goal Percentage 2 Pointer: {fg_percentage_2pt:.2f}%\n"
        f"Field Goal Percentage 3 Pointer: {fg_percentage_3pt:.2f}%\n"
        f"Steals: {steals}\n"
        f"Blocks: {blocks}\n"
        f"Turnovers: {turnovers}\n"
        f"Total Time Played: {total_time} minutes\n"
        f"Points per Minute: {points_per_minute:.2f}\n"
    )

    pdf.multi_cell(0, 10, text)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, download_name='report.pdf', as_attachment=True)

@app.route('/send_report', methods=['POST'])
def send_report():
    to_email = request.form.get('email')
    
    # Generate the report
    player_name = request.form.get('player_name')
    game_date = request.form.get('game_date')
    teams_playing = request.form.get('teams_playing')
    free_throws_made = int(request.form.get('free_throws_made', 0))
    free_throws_attempted = int(request.form.get('free_throws_attempted', 0))
    two_pointers_made = int(request.form.get('two_pointers_made', 0))
    two_pointers_attempted = int(request.form.get('two_pointers_attempted', 0))
    three_pointers_made = int(request.form.get('three_pointers_made', 0))
    three_pointers_attempted = int(request.form.get('three_pointers_attempted', 0))
    total_points = int(request.form.get('total_points', 0))
    steals = int(request.form.get('steals', 0))
    blocks = int(request.form.get('blocks', 0))
    turnovers = int(request.form.get('turnovers', 0))
    total_time = float(request.form.get('total_time', 0))

    fg_percentage = (total_field_goals_made / (total_field_goals_attempted or 1)) * 100
    fg_percentage_ft = (total_free_throws_made / (total_free_throws_attempted or 1)) * 100
    fg_percentage_2pt = (two_pointers_made / (two_pointers_attempted or 1)) * 100
    fg_percentage_3pt = (three_pointers_made / (three_pointers_attempted or 1)) * 100
    points_per_minute = total_points / (total_time or 1)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    text = (
        f"Basketball Game Report\n\n"
        f"Player: {player_name}\n"
        f"Game Date: {game_date}\n"
        f"Teams Playing: {teams_playing}\n\n"
        f"STATS:\n"
        f"Total Points: {total_points}\n"
        f"Field Goal Percentage: {fg_percentage:.2f}%\n"
        f"Field Goal Percentage Free Throw: {fg_percentage_ft:.2f}%\n"
        f"Field Goal Percentage 2 Pointer: {fg_percentage_2pt:.2f}%\n"
        f"Field Goal Percentage 3 Pointer: {fg_percentage_3pt:.2f}%\n"
        f"Steals: {steals}\n"
        f"Blocks: {blocks}\n"
        f"Turnovers: {turnovers}\n"
        f"Total Time Played: {total_time} minutes\n"
        f"Points per Minute: {points_per_minute:.2f}\n"
    )

    pdf.multi_cell(0, 10, text)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    send_email(to_email, pdf_output.read())

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
