import lxml.html

from examy.models.fetcher import ExamFetcher
from examy.models.Student import Student
from examy.models.ExamDescriptor import ExamDescriptor
from examy.utils import province_codes


class KissNewTypeFetcher(ExamFetcher):
    result_page_layout = "new"
    fetcher_codename = "kiss"

    def __init__(self):
        super().__init__()

        import requests
        self.session = requests.session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0'}

    @ExamFetcher.check_fetch_arguments
    def fetch(self, student, exam_descriptor, *args, **kwargs):
        from examy.fetchers.new_web_layout.utils.webpage_actions import get_result_location_from_source
        from examy.fetchers.new_web_layout.utils.process_html import process_result_html

        
        province_code = kwargs.get("province_code", province_codes[student.province])

        district_code = kwargs.get("district_code", self.get_district_code(province_code, student, exam_descriptor))
        school_code = kwargs.get("school_code", self.get_school_code(district_code, student, exam_descriptor))


        data = f"""--formsplit
Content-Disposition: form-data; name="giristuru"

1
--formsplit
Content-Disposition: form-data; name="sinif"

{student.grade.split('.')[0]}
--formsplit
Content-Disposition: form-data; name="ilkodu"

{province_code}
--formsplit
Content-Disposition: form-data; name="ilcekodu"

{district_code}
--formsplit
Content-Disposition: form-data; name="kurumkodu"

{school_code}
--formsplit
Content-Disposition: form-data; name="ogrno"

{student.number}
--formsplit
Content-Disposition: form-data; name="adsoyad"

{student.name}
--formsplit--
""" 
        self.session.cookies.clear()

        response = self.session.post(
                f'{exam_descriptor.login_url}/ajax/ogrencigirisarama.php',
                headers={'Content-Type': 'multipart/form-data; boundary=formsplit'},
                data=data)

        dummy_url_base = f"{exam_descriptor.login_url}/ogrenci/"
        response = self.session.get(dummy_url_base, params={'pg': 'sinavsonuclari'})

        address = dummy_url_base + get_result_location_from_source(response.text, exam_descriptor)

        response = self.session.get(address, allow_redirects=False)

        root = lxml.html.fromstring(response.content)

        result = process_result_html(root, student, exam_descriptor)

        return result

    def get_district_code(self, province_code: str, student: Student, exam_descriptor: ExamDescriptor) -> str:
        district_data = self.session.get(f'{exam_descriptor.login_url}/ajax/ilceler.php?ilkodu={province_code}').json()
        for district in district_data:
            if district["ilceadi"] == student.district:
                return district["ilcekodu"]
        raise ValueError(f"District {student.district} not found")

    def get_school_code(self, district_code: str, student: Student, exam_descriptor: ExamDescriptor) -> str:
        school_data = self.session.get(f'{exam_descriptor.login_url}/ajax/kurumlar.php?ilcekodu={district_code}').json()
        for school in school_data:
            if school["kurum"] == student.school:
                return school["kurumkodu"]
        raise ValueError(f"School {student.school} not found")
