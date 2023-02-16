from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def send_registration_mail(email, logo_url, update_team_url):
    # print()
    html = f'''
    <html>
    <div style="
                font-family: system-ui;
                background: #FDFBE1;
                padding: 25px;
                margin: 50px;
                text-align: center;
                line-height: 1.5;
                "
                >
        <img width="50" src="{logo_url}" alt="">
        <h2>All Done!!</h2>
        <p>You have successfully registered to the National Level Sports SUMMIT'23. <br> Welcome to the battlefield!</p>
        <p>You can modify your team using this button-
        </p>
        <a target="_blank" href="{update_team_url}" style="background: #0A9B81; color: white;padding: 10px 25px;
        border-radius: 5px;
        text-decoration: none;">Modify Team</a>
        <p>Please <b>DO NOT SHARE</b> this link to anyone outside your team.</p>
    </div>
</html>
    '''

    # Custom function to reduce rules
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=email,
        subject='Registration | Summit 2023',
        html_content=html)
    try:
        sg = SendGridAPIClient(env('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def failed_registration_email(email, logo_url, update_team_url):
    html = f'''
    <html>
    <div style="
                font-family: system-ui;
                background: #FDFBE1;
                padding: 25px;
                margin: 50px;
                text-align: center;
                line-height: 1.5;
                "
                >
        <img width="50" src="{logo_url}" alt="">
        <h2>Registration failed!</h2>
        <p>Unfortunately, your registration for the event has failed.</p>
        <p>Please get in touch with our support team via our contact us page.</p>
        <p>Don't worry though, your team details are saved with us. You can visit this link
            and try your payment again-
        </p>
        <a target="_blank" href="{update_team_url}" style="background: #0A9B81; color: white;padding: 10px 25px;
        border-radius: 5px;
        text-decoration: none;">Modify Team</a>
        <p>Please <b>DO NOT SHARE</b> this link to anyone outside your team.</p>
    </div>
</html>
    '''

    # Custom function to reduce rules
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=email,
        subject='Registration | Summit 2023',
        html_content=html)
    try:
        sg = SendGridAPIClient(env('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)