import os
import atexit

from pytz import utc
from datetime import date
from app import create_app
from app import scheduler

from app.short_link.utils import clear_expired_links

app = create_app(os.getenv('FLASK_ENV') or 'test')
app.app_context().push()

scheduler.add_job(
    id='Delete expired links',
    func=clear_expired_links,
    trigger="interval",
    start_date=date.today(),
    days=1,
    timezone=utc)

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)
    atexit.register(lambda: scheduler.shutdown())
