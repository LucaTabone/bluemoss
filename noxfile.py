import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.install('-r', 'requirements/base.txt')
    session.run('pytest')
