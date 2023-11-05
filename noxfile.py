import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.install('-r', 'requirements/dev.txt')
    session.run('coverage',  'run',  '-m', 'pytest')
    session.run('coverage', 'xml', '-o', 'coverage.xml')
