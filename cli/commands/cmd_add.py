import click
import random

from faker import Faker

from flowstate.app import create_app
from flowstate.extensions import db
from flowstate.blueprints.user.models import User


# Create an app context for the database connection
app = create_app()
db.app = app

# For creating admin/users
fake = Faker()


def _log_status(count, model_label):
    """ Log the output of how many records were created. """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """ Bulk insert data to a specific model. """
    with app.app_context():
        model.query.delete()
        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def users():
    """ Generate fake users. """
    random_emails = []
    data = []

    for i in range(0, 19):
        random_emails.append(fake.email())

    random_emails.append(app.config['SEED_ADMIN_EMAIL'])
    random_emails = list(set(random_emails))

    while True:
        if len(random_emails) == 0:
            break

        # set member/admin lottery
        random_percent = random.random()

        if random_percent >= 0.05:
            role = 'member'
        else:
            role = 'admin'

        email = random_emails.pop()

        # set username lottery
        random_percent = random.random()

        if random_percent >= 0.5:
            random_trail = str(int(round((random.random() * 1000))))
            username = fake.first_name() + random_trail
        else:
            username = None

        # set user parameters
        params = {
            'role': role,
            'email': email,
            'username': username,
            'password': User.encrypt_password('password'),
            'sign_in_count': random.random() * 100,
            'current_sign_in_ip': fake.ipv4(),
            'last_sign_in_ip': fake.ipv4()
        }

        # set admin parameters
        if email == app.config['SEED_ADMIN_EMAIL']:
            password = User.encrypt_password(app.config['SEED_ADMIN_PASSWORD'])

            params['role'] = 'admin'
            params['password'] = password

        data.append(params)

    return _bulk_insert(User, data, 'users')
 

@click.command()
@click.pass_context
def all(ctx):
    """ Generate all data. """
    ctx.invoke(users)

    return None


cli.add_command(users)
cli.add_command(all)