import pytest

from seeq import spy

from ...tests import test_common
from . import test_load


def setup_module():
    test_common.login()


@pytest.mark.system8
def test_pull():
    workbook_df = spy.workbooks.search({
    })

    workbooks = spy.workbooks.pull(workbook_df)

    spy.workbooks.options.pretty_print_html = True

    spy.workbooks.save(workbooks, r'D:\Scratch\WorkbookExport')


@pytest.mark.monitors
def test_export_monitors_seeq_site():
    spy.login(url='https://monitors.seeq.site', auth_token='Yre09-GgdtOxN9wSkkbQ_A')

    search_df = spy.workbooks.search({
        'Path': 'Exxon',
        'Name': '/^Exxon Topic$/',
        'Workbook Type': 'Topic'
    }, recursive=True, content_filter='ALL')

    workbooks = spy.workbooks.pull(search_df)

    spy.workbooks.save(workbooks, r'D:\Scratch\monitors_mark', clean=True)
