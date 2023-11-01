import nox


@nox.session(python=['3.11', '3.12'])
def tests(session):
    session.install('-r', 'requirements/base.txt')
    session.run('pytest')
