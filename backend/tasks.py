from celery import shared_task
import csv
import os
from io import StringIO
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import User, Booking, db
import datetime


EXPORTS_FOLDER = "exports"


@shared_task(ignore_result=False)
def generate_theatre_csv(theatre, shows):
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(
        [
            "Theatre Name",
            "Address",
            "Capacity",
            "Show Name",
            "Show Rating",
            "Show Tags",
            "Show Price",
            "Show Time",
        ]
    )

    for show in shows:
        csv_writer.writerow(
            [
                theatre["name"],
                theatre["address"],
                theatre["capacity"],
                show["name"],
                show["rating"],
                show["tags"],
                show["price"],
                show["time"],
            ]
        )

    csv_data_string = csv_data.getvalue()

    if not os.path.exists(EXPORTS_FOLDER):
        os.makedirs(EXPORTS_FOLDER)

    file_path = os.path.join(EXPORTS_FOLDER, f"theatre_{theatre['id']}_data.csv")
    with open(file_path, "w") as csv_file:
        csv_file.write(csv_data_string)

    return file_path


@shared_task(ignore_result=False)
def send_reminder_emails():
    users_to_remind = get_user_to_email()

    for user in users_to_remind:
        send_email_to_user(user)

    return f"{len(users_to_remind)} reminder emails sent"


def send_email_to_user(user):
    smtp_server = "localhost"
    smtp_port = 1025
    sender_email = "raj.73.tiw@gmail.com"
    recipient_email = user["email"]
    html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #C9E4F7;
                        }}
                        .header {{
                            background-color: #007bff;
                            color: #fff;
                            padding: 20px;
                            text-align: center;
                        }}
                        
                        .content {{
                            padding: 20px;

                        }}
                        .btn{{
                         margin-left:47%
                        }}
                        .button{{
                            border-radius:3px;
                            border:none;
                            background-color:#F7B400;
                            display: inline-block;
                            padding: 10px 20px;
                            color: #fff;
                            text-decoration: none;
                        }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>Exciting Shows Just For You!</h1>
                    </div>
                    <div class="content">
                        <h4>Dear {user['user_name']},</h4>
                        <p>Long time no see !</p>
                        <p>Book latest show tickets at minimal cost !</p>
                    </div>
                    <div class=btn>
                    <a class='button' href="http://localhost:5173/">Book Now !</a>
                    </div>
                </body>
                </html>
                """

    subject = "Reminder: Exciting Shows Just For You !"

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)


def get_user_to_email():
    user_list = []
    users = User.query.all()
    for user in users:
        if not user.bookings or user.bookings[
            -1
        ].show_schedule.show_time < datetime.utcnow() - timedelta(days=1):
            if not user.is_admin:
                user_list.append(user.to_dict())
    return user_list


def generate_report_data(user):
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    bookings_data = []
    bookings = user.bookings
    monthly_booking = [
        book
        for book in bookings
        if book.show_schedule.show_time.month == current_month
        and book.show_schedule.show_time.year == current_year
    ]
    total_money = 0
    for book in monthly_booking:
        booking_data = {
            "theatre_name": book.theatre.name,
            "theatre_address": book.theatre.address,
            "show_name": book.show.name,
            "show_rating": book.show.rating,
            "show_price": book.show_schedule.price,
            "show_time": book.show_schedule.show_time,
        }
        total_money += int(book.show_schedule.price)
        bookings_data.append(booking_data)
    return bookings_data, total_money


def send_report(user):
    smtp_server = "localhost"
    smtp_port = 1025
    sender_email = "raj.73.tiw@gmail.com"
    recipient_email = user.email

    bookings, total_money_spent = generate_report_data(user)
    total_bookings = len(bookings)

    html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css" integrity="sha384-b6lVK+yci+bfDmaY1u0zE8YYJt0TZxLEAFyYSLHId4xoVvsrQu3INevFKo+Xir8e" crossorigin="anonymous">
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #C9E4F7;
                        }}
                        .header {{
                            background-color: #007bff;
                            color: #fff;
                            padding: 20px;
                            text-align: center;
                        }}
                        .info {{
                            padding: 10%;
                            margin: 5%;
                            background-color: #01756C;
                            min-height: 150px;
                            width: 100%;
                            border-radius: 0.5rem;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            
                        }}
                        
                        .btn{{
                         margin-left:47%
                        }}
                        .button{{
                            border-radius:3px;
                            border:none;
                            background-color:#F7B400;
                            display: inline-block;
                            padding: 10px 20px;
                            color: #fff;
                            text-decoration: none;
                        }}
                        .col-5 {{
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            padding: 2%;
                            margin: auto;
                        }}

                        .row {{
                            margin: 0%;
                        }}
                        .list {{
                            max-width: 100vw;
                            padding: 5%;
                        }}
                        p {{
                            font-size: 40px;
                            margin-bottom: 0%;
                            color: #aeda84;
                        }}
                        .content {{
                            padding: 20px;
                        }}

                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>Your Entertainment Booking Report</h1>
                    </div>
                    <div class="row">
                        <div class="col-5">
                            <div class="info" >
                            <h4>Total Bookings</h4>
                            <p><i class="bi bi-film me-3" style="color: rgb(228, 210, 47);"></i>{total_bookings}</p>
                            </div>        
                        </div>
                        <div class="col-5">
                            <div class="info" >
                            <h4>Total Spendings</h4>
                            <p><i class="bi bi-currency-dollar me-3" style="color: #7BF700; "></i>{total_money_spent}
                            </p>
                            </div>        
                        </div>
                    </div>
                    <div class="list">
                        <h2 class="text-center mb-4"> Your Bookings</h2>
                        <table class="table table-warming table-striped">
                            <thead>
                            <tr >
                                <th scope="col" style="font-weight: 900;">Show Name</th>
                                <th scope="col" style="font-weight: 900;">Theatre Name</th>
                                <th scope="col" style="font-weight: 900;">Show Price</th>
                                <th scope="col" style="font-weight: 900;">Show Rating</th>
                                <th scope="col" style="font-weight: 900;">Address</th>
                                <th scope="col" style="font-weight: 900;">Time</th>
                            </tr>
                            </thead>
                            <tbody>
                                {''.join([
                                    f'<tr><td>{book["show_name"]}</td><td>{book["theatre_name"]}</td><td>₹ &nbsp;   {book["show_price"]}</td><td>{book["show_rating"]}</td><td>{book["theatre_address"]}</td><td>{book["show_time"]}</td></tr>'
                                    for book in bookings
                                ])}
                            </tbody>
                        </table>

                        </div>

                        <div class="content">
                        <h5>Thank you for choosing us for your entertainment needs!</h5>
                        <h5>Best regards,<br>Your Entertainment Team</h5>
                        </div>
                        <div class=btn>
                            <a class='button' href="http://localhost:5173/">Book Now !</a>
                        </div>
                    </div>
                </body>
                </html>
              """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg[
        "Subject"
    ] = f"{user.user_name}'s Monthly Progress Report - {datetime.datetime.now().month}-{datetime.datetime.now().year}"
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)


@shared_task(ignore_result=False)
def send_entertainment_report():
    users_to_remind = User.query.all()
    for user in users_to_remind:
        if not user.is_admin:
            send_report(user)

    return f"{len(users_to_remind)-1} reminder emails sent"
