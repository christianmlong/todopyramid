from datetime import datetime
from datetime import timedelta
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    TodoItem,
    TodoUser,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print(('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)))
    sys.exit(1)


def create_dummy_content(user_id):
    """Create some tasks by default to show off the site
    """
    task = TodoItem(
        user=user_id,
        task='Find a shrubbery',
        tags=['quest', 'ni', 'knight'],
        due_date=datetime.utcnow() + timedelta(days=60),
    )
    DBSession.add(task)
    task = TodoItem(
        user=user_id,
        task='Search for the holy grail',
        tags=['quest'],
        due_date=datetime.utcnow() - timedelta(days=1),
    )
    DBSession.add(task)
    task = TodoItem(
        user=user_id,
        task='Recruit Knights of the Round Table',
        tags=['quest', 'knight', 'discuss'],
        due_date=datetime.utcnow() + timedelta(minutes=45),
    )
    DBSession.add(task)
    task = TodoItem(
        user=user_id,
        task='Build a Trojan Rabbit',
        tags=['quest', 'rabbit'],
        due_date=datetime.utcnow() + timedelta(days=1),
    )
    DBSession.add(task)
    task = TodoItem(
        user=user_id,
        task='Talk to Tim the Enchanter',
        tags=['quest', 'discuss'],
        due_date=datetime.utcnow() + timedelta(days=90),
    )
    DBSession.add(task)
    task = TodoItem(
        user=user_id,
        task='Defeat the Rabbit of Caerbannog',
        tags=['quest', 'rabbit'],
        due_date=None,
    )
    DBSession.add(task)
    task = TodoItem(
        user=user_id,
        task='Cross the Bridge of Death',
        tags=['quest'],
        due_date=None,
    )
    DBSession.add(task)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        user = TodoUser(
            email='king.arthur@example.com',
            first_name='Arthur',
            last_name='Pendragon',
        )
        DBSession.add(user)
        create_dummy_content('king.arthur@example.com')
