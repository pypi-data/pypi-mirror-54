from pytest_docker_fixtures import images


images.configure(
    'cockroach',
    'cockroachdb/cockroach', 'v2.0.5')


pytest_plugins = [
    'aiohttp.pytest_plugin',
    'guillotina.tests.fixtures',
    'guillotina_linkintegrity.tests.fixtures'
]
