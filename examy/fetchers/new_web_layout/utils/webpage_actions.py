import warnings

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from examy.models.ExamDescriptor import ExamDescriptor
from examy.models.Student import Student


def login(driver: WebDriver, student: Student, exam_descriptor: ExamDescriptor, **kwargs):
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support.expected_conditions import (
        presence_of_element_located, url_changes
    )
    from selenium.common.exceptions import NoSuchElementException, TimeoutException

    driver.get(exam_descriptor.login_url)

    # grade
    WebDriverWait(driver, kwargs.get("timeout1", 5)).until(
        presence_of_element_located(
            (
                "id",
                "select2-gt_ogrencino_sinifcombo-container",
            )
        )
    ).click()

    grade_selector = driver.find_element("id", "select2-gt_ogrencino_sinifcombo-results")
    grade_selector.find_element("xpath", f"//li[text()='{student.grade}']").click()

    # province
    driver.find_element(
        "id",
        "select2-gt_ogrencino_ilcombo-container"
    ).click()
    province_selector = driver.find_element("id", "select2-gt_ogrencino_ilcombo-results")
    click_list_item_by_visible_text(province_selector, student.province)

    # district
    driver.find_element("id", "select2-gt_ogrencino_ilcecombo-container").click()
    district_selector = driver.find_element("id", "select2-gt_ogrencino_ilcecombo-results")
    click_list_item_by_visible_text(district_selector, student.district)

    # school
    driver.find_element("id", "select2-gt_ogrencino_kurumcombo-container").click()
    school_selector = driver.find_element("id", "select2-gt_ogrencino_kurumcombo-results")
    click_list_item_by_visible_text(school_selector, student.school)

    # number
    number_field = driver.find_element("id", "gt_ogrencino_numaraedit")
    number_field.send_keys(str(student.number))

    # name
    for i in ("gt_ogrencino_adsoyadedit", "gt_ogrencino_adedit"):

        try:
            driver.find_element("id", i).send_keys(student.login_name)
        except NoSuchElementException:
            pass
        else:
            break

    # submit
    # driver.implicitly_wait(1)
    driver.find_element("id", "gt_ogrencino_girisbtn").click()

    # check if successful
    try:
        WebDriverWait(driver, kwargs.get("timeout2", 3)).until(
            url_changes(exam_descriptor.login_url)
        )
    except TimeoutException as e:
        from examy.models.exceptions import StudentNotFound

        raise StudentNotFound(f'Student probably did not take any exams from "{exam_descriptor.login_url}"') from e


def click_list_item_by_visible_text(parent: WebElement, text: str):
    parent.find_element("xpath", f".//li[text()='{text}']").click()


def logout(driver: WebDriver, exam_descriptor: ExamDescriptor):
    if not exam_descriptor.logout_url:
        warnings.warn(
            "requested logout but logout_url is not set in descriptor. This may be caused from a misconfiguration.",
            RuntimeWarning,
        )
        return

    driver.get(exam_descriptor.logout_url)


def get_result_page_address(driver: WebDriver, exam_descriptor: ExamDescriptor) -> str:
    # driver must be on the exam selection page
    # note that the url is specific for each student
    import lxml.html
    from examy.models.exceptions import StudentDidNotTakeExam

    source = driver.page_source
    tree = lxml.html.fromstring(source)

    link = tree.xpath(f"/html/body/section//a[text()='{exam_descriptor.exam_name}']")

    if len(link) == 0:
        raise StudentDidNotTakeExam(f"Student did not take the exam named {exam_descriptor.exam_name}")

    link = link[0]

    base_url = driver.current_url.split("?")[0]

    return base_url + link.attrib["href"]
