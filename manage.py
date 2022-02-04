import os
import atexit

from pytz import utc
from datetime import date
from flask_script import Manager

from app import create_app, db, scheduler
from app.short_link.utils import clear_expired_links
from commands.seed_command import SeedCommand


env = os.getenv("FLASK_ENV") or 'test'
print(f"Active environment: * {env} *")
app = create_app(env)

manager = Manager(app)
app.app_context().push()
manager.add_command("seed_db", SeedCommand)


@manager.command
def run():
    app.app_context().push()

    scheduler.add_job(
        id='Delete expired links',
        func=clear_expired_links,
        trigger="interval",
        start_date=date.today(),
        days=1,
        timezone=utc)
    scheduler.start()
    app.run(host='0.0.0.0', port=5555)
    atexit.register(lambda: scheduler.shutdown())


@manager.command
def init_db():
    print("Creating all resources.")
    db.create_all()


@manager.command
def drop_all():
    if input("drop all tables? (y/N)\n").lower() == "y":
        print("Dropping tables...")
        db.drop_all()


if __name__ == "__main__":
    manager.run()
