import click
from flask.cli import with_appcontext, AppGroup

from packages.database_connecter import db
from models.target_do import TargetDO

target_cli = AppGroup("target", help="Run commands for users")


@target_cli.command("create")
@click.argument("title")
@click.argument("image_url")
@click.argument("description")
@click.argument("summary")
@click.argument("key_point_list")
@click.argument("email")
@click.option("--extras", default=None)
@with_appcontext
def create_target(title: str, image_url: str, description: str, summary: str, key_point_list: str, email: str, extras):
    """Create a user by passing the name and email"""
    click.echo(f"extras passed are: {extras}")
    click.echo("Creating a new target")
    target = TargetDO(title=title, image_url=image_url, description=description, summary=summary,
                      key_point_list=key_point_list, email=email)
    db.session.add(target)
    db.session.commit()
    click.echo(f"""User:
                   title:{title},
                   image_url:{image_url},
                   description:{description},
                   summary:{summary},
                   key_point_list:{key_point_list},
                   email:{email}
                has been created""")

# how to use this command:
# input command:
# flask
#
# to check the Group Command name target
# after that ,you can input command:
# flask target
#
# to check  which children command include in target group.
# ok. you can use one of children command like that:
# flask target create "GoDot" "image_url" "a open game engine" "a game engine can use to replace unity" "1.how to learn" "sghdjs@gamil.com"
