from datetime import datetime
from flask_script import Command

from app import db
from app.short_link import Link


def seed_smth():
    entities = [
        {
            "link_id": "1",
            "original_link": "http://alanpryorjr.com/2019-05-20-flask-api-example/",
            "short_id": "value1",
            "expires_at": datetime(2022, 6, 17),
         },

        {
            "link_id": "2",
            "original_link": "http://rozklad.kpi.ua",
            "short_id": "value2",
            "expires_at": datetime(2022, 3, 12),
        },

        {
            "link_id": "3",
            "original_link": "https://stackoverflow.com",
            "short_id": "value3",
            "expires_at": datetime(2022, 2, 9),
        },
    ]

    db.session.bulk_insert_mappings(Link, entities)


class SeedCommand(Command):
    """Seed the DB."""

    def run(self):
        print("Dropping tables...")
        db.drop_all()
        db.create_all()
        seed_smth()
        db.session.commit()
        print("DB successfully seeded.")
