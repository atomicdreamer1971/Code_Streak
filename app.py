import os
import schedule
import time
import json
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# 🔴 REPLACE THESE
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "atomicdreamer1971@gmail.com"


def send_email(to_email, subject, content):
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def load_tasks():
    with open("tasks.json", "r") as file:
        return json.load(file)


def create_jobs():
    tasks = load_tasks()

    for task in tasks:
        for t in task["times"]:

            def job(task=task, t=t):
                now = datetime.now().strftime("%H:%M")

                print(f"\n[{now}] Triggered for scheduled time {t}")
                print(f"Task: {task['task']}")
                
                for user in task["users"]:
                    now = datetime.now().strftime("%H:%M")

                    message = f"""
                    <h2>Reminder: {task['task']}</h2>

                    <p>Hi {user['name']},</p>

                    <p>This is your scheduled reminder to complete your task.</p>

                    <p><b>Task:</b> {task['task']}</p>
                    <p><b>Time:</b> {now}</p>

                    <p>Stay consistent 🚀</p>
                    """

                    success = send_email(
                        user["email"],
                        f"Reminder: {task['task']}",
                        message
                    )

                    if success:
                        print(f"✓ Sent to {user['email']} at {now}")
                    else:
                        print(f"❌ Failed for {user['email']}")

            schedule.every().day.at(t).do(job)


# 🔴 Start scheduler
create_jobs()

print("🚀 Scheduler started... Waiting for tasks...")

while True:
    schedule.run_pending()
    time.sleep(1)