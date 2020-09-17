from framework.pageobject.pages import WebAppMainPage, ProjectPage, RunPage
from framework.logger import appLogger
from framework.utils.APIutils import *
from framework.utils.assistance import *
from framework.utils.DButils import update_test_in_database, get_attachment_to_test


VARIANT = test_data['variant']
URL = config_data['url']
LOGIN = test_data['login']
PASS = test_data['password']
PROJECT_NEX = test_data['project_nex']
PROJ_NEX_ID = test_data['project_nex_id']
NEW_PROJ = test_data['project_name']
SID = generate_integer()
TEST_NAME = test_data['test_name']
TEST_METHOD = test_data['test_method']
MACHINE = config_data['machine']
LOGFILE = config_data['log']
SCREENSHOT = f'{NEW_PROJ}_screenshot.png'


def test_web_app(browser):
    appLogger.debug('Get token')
    token = get_token(VARIANT)
    appLogger.debug('Check token was generated')
    assert token, 'Token was not generated'

    appLogger.debug('Opening browser')
    app_page = WebAppMainPage(browser)
    appLogger.debug('Go to site')
    app_page.complete_basic_auth_with_token(URL, LOGIN, PASS)
    appLogger.debug('Add cookies')
    app_page.add_cookie('token', token)
    appLogger.debug('Refresh page')
    app_page.refresh_page()
    app_page_new = WebAppMainPage(browser)
    app_page_new.go_to_site(URL)
    version = strip_span_content(app_page_new.get_variant())
    appLogger.debug('Assert correct version was opened')
    assert version == VARIANT, 'Wrong variant was opened'

    appLogger.debug(f'Open {PROJECT_NEX} project')
    app_page.open_project(PROJECT_NEX)
    appLogger.debug(f'Get all tests from {PROJECT_NEX} project')
    tests = get_project_test(PROJ_NEX_ID)
    appLogger.debug('Assert test on 1st page sorted and equal for api test request')
    project_page = ProjectPage(browser)
    appLogger.debug('Get all tests data')
    test_start_time = project_page.get_tests_start_time()
    all_tests_starts = [time['startTime'] for time in tests]
    assert test_start_time == sorted(test_start_time, reverse=True), 'Data is unsorted by descending'
    appLogger.debug('Assert tests start time on page are in list of all tests starts')
    assert sorted(list(set(test_start_time) & set(all_tests_starts)), reverse=True) == test_start_time, \
        'Visible part of tests starts are not in all tests start list'
    appLogger.debug('Click home button')
    project_page.click_home_button()

    path = app_page.find_script()
    close_popup = get_script_content(path, LOGIN, PASS)
    appLogger.debug('Add new project')
    app_page.add_project()
    app_page.switch_to_iframe()
    appLogger.debug('Add new project name')
    app_page.put_project_name(NEW_PROJ)
    appLogger.debug('Save new project')
    app_page.submit_creation()
    appLogger.debug('Assert successful save')
    assert app_page.find_alert_success_field(), 'Project was not saved'
    appLogger.debug('Switch window back to mainpage')
    app_page.switch_to_mainpage()
    appLogger.debug('Close window with ClosePopUp()')
    app_page.execute_script(close_popup)
    appLogger.debug('Assert window was closed')
    assert app_page.check_frame_visible(), 'Window was not closed'
    appLogger.debug('Refresh page')
    app_page.refresh_page()
    appLogger.debug('Check project created')
    assert app_page.find_project(NEW_PROJ), 'Project was not created'

    appLogger.debug(f'Got to {NEW_PROJ} project')
    app_page.open_project(NEW_PROJ)
    appLogger.debug('Take page screenshot')
    screenshot = project_page.take_screenshot(NEW_PROJ)
    screen_shot_base64 = encode_file_to_base64(screenshot)
    appLogger.debug('Add new test')
    test_id = post_test(SID, NEW_PROJ, TEST_NAME, TEST_METHOD, MACHINE)
    appLogger.debug('Upload screenshot and logfile to DB')
    update_test_in_database(test_id, screen_shot_base64, LOGFILE)
    appLogger.debug('Enter into test')
    project_page.get_test(TEST_NAME)
    appLogger.debug('Assert test data are correct')
    test_page = RunPage(browser)
    assert test_page.find_test_field(TEST_NAME), 'Test name incorrect'
    assert test_page.find_test_field(TEST_METHOD), 'Test method incorrect'
    assert test_page.find_test_field(NEW_PROJ), 'Project name incorrect'
    assert test_page.find_test_field(TEST_METHOD), 'Test method incorrect'
    assert get_attachment_to_test(test_id) == screen_shot_base64, 'Screenshots are not equal'
