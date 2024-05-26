import lxml.html

from examy.models.ExamDescriptor import ExamDescriptor
from examy.models.ExamReport import ExamReport
from examy.models.Student import Student


def process_result_html(root: lxml.html.HtmlElement, student: Student, exam_descriptor: ExamDescriptor) -> ExamReport:
    from examy.utils import turkish_str_to_float
    from examy.models.Ranking import Ranking
    from examy.models.TestResult import TestResult

    root = root.xpath("/html/body/section")[0]

    score = turkish_str_to_float(root.xpath("./div[1]/div[3]/div/div/div/div[2]")[0].text_content())
    ranks_and_attendances = []
    for i in range(2, 7):
        for j in (5, 6):
            ranks_and_attendances.append(
                int(root.xpath(f"./div[1]/div[{j}]/div/div/div/div[{i}]")[0].text_content().split("%")[0].rstrip())
            )

    ranks = Ranking(*ranks_and_attendances)

    test_results = []
    for test_d in exam_descriptor.tests:
        example_element = root.xpath(f'.//*[@title = "{test_d.name} soru sayısı"]')
        if not example_element:
            test_results.append(TestResult(0, 0, 0, test_d))
            continue

        example_element = example_element[0]
        test_root = example_element.xpath("./../../..")[0]

        net = turkish_str_to_float(test_root.xpath("./div[5]/div/div/*[last()]")[0].text_content())
        true = int(test_root.xpath("./div[2]/div/div/*[last()]")[0].text_content())
        false = int(test_root.xpath("./div[3]/div/div/*[last()]")[0].text_content())

        test_results.append(TestResult(net, true, false, test_d))

    report = ExamReport(
        exam_descriptor,
        score,
        test_results,
        ranks,
    )

    return student.add_report(report)
