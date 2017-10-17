#!/usr/bin/env python
import os
from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models.user import Role, User

COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage
    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()

app = create_app(os.getenv("FLASK_CONFIG") or "default")

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("server", Server(host="0.0.0.0", port=8080))
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role)


@manager.command
def test(coverage=False):
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        import sys
        os.environ["FLASK_COVERAGE"] = "1"
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print("HTML version: file://%s/index.html" % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                      restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


# @manager.command
# def deploy():
#     """Run deployment tasks."""
#     from flask_migrate import upgrade
#     from app.models.user import Role, User
#
#     # migrate database to latest revision
#     upgrade()
#
#     # create user roles
#     Role.insert_roles()
#
#     # create self-follows for all users
#     User.add_self_follows()


if __name__ == "__main__":
    manager.run()