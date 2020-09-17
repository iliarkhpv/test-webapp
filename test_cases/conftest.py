import pytest
from framework.browser.browser_factory import Browser
from framework.logger import appLogger
from testrail import *
from framework.utils.assistance import get_config_data, get_testrail_data, get_test_data
from datetime import datetime

test_data = get_test_data()
config_data = get_config_data()
testrail = get_testrail_data()
USER_ID = testrail['user_id']
TR_URL = testrail['url']
TR_LOGIN = testrail['login']
TR_PASS = testrail['pass']
TR_PROJECT = testrail['project_id']
SCREENSHOT = f"{test_data['project_name']}_screenshot.png"
PROJECT_ID = testrail['project_id']
TR_NAME = "test_run_" + str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="Chrome", type=str)


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture
def browser(request, browser_name):
    appLogger.debug('Set-up')
    driver = Browser.factory(browser_name)
    appLogger.debug('Maximize browser window')
    driver.maximize_window()
    yield driver
    appLogger.debug('Tear-down')
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def module_name(request):
    test_name = (request.node.name)
    test_id = test_name.replace(f'[{config_data["browser"]}]', '')
    global TEST_ID
    TEST_ID = test_id


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call':
        item.session.results[item] = result


def pytest_sessionfinish(session):
    for result in session.results.values():
        if result.passed:
            status_id = 1
            comment = "Passed"
        elif result.failed:
            status_id = 5
            comment = "Failed"
    send_results_to_testrail(status_id, comment)


def send_results_to_testrail(status, comment):
    client = APIClient(TR_URL)
    client.user = TR_LOGIN
    client.password = TR_PASS
    add_run = client.send_post(f'add_run/{PROJECT_ID}', data={
        "name": TR_NAME
    })
    tests = client.send_get(f'get_tests/{add_run["id"]}')
    add_res = client.send_post(f'add_result/{tests[0]["id"]}', data={
        "status_id": status,
        "comment": comment,
        "assignedto_id": USER_ID
    })
    TEST_RUN = add_res['id']
    client.send_post(f'add_attachment_to_result/{TEST_RUN}', SCREENSHOT)
