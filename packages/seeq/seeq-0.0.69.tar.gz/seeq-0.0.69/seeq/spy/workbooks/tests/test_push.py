import json
import os
import pytest
import shutil
import tempfile

from seeq import spy
from seeq.sdk import *

from ... import _common
from ...tests import test_common
from . import test_load


def setup_module():
    test_common.login()


def _get_exports_folder():
    return os.path.join(os.path.dirname(__file__), 'Exports')


def _get_full_path_of_export(subfolder):
    return os.path.join(_get_exports_folder(), subfolder)


def _load_and_push(subfolder):
    workbooks = spy.workbooks.load(_get_full_path_of_export(subfolder))
    return _push(workbooks)


def _push(workbooks):
    push_df = spy.workbooks.push(workbooks)
    return push_df.iloc[0]['Pushed Workbook ID']


@pytest.mark.export
def test_export_example_and_test_data():
    # Use this function to re-create the Example Export and test-related exports.
    # First copy the contents of "crab/sdk/pypi/spy-example-and-test-data-folder.zip" into "crab/sq-run-data-dir"
    # and start Seeq Server by doing "sq run" from crab.
    #
    # You MUST log in as "mark.derbecker@seeq.com" with password "SeeQ2013!". (If you don't log in as
    # mark.derbecker@seeq.com, then some of the ACL tests may get screwed up.)
    #
    # If you add workbooks, make sure to share them with Everyone because the tests will log in as Agent API Key.
    #
    # When finished, change the sdk-system-tests Run Configuration in IntelliJ to have an "-m export" flag so that only
    # this test gets executed. It will copy everything into the right spot.
    #
    # Then make sure to zip up the contents of "crab/sq-run-data-dir" and replace
    # "crab/sdk/pypi/spy-example-and-test-data-folder.zip" and commit it to the repo.

    search_df = spy.workbooks.search({
        'Path': 'Example Export'
    }, content_filter='ALL')

    spy.workbooks.options.pretty_print_html = True

    workbooks = spy.workbooks.pull(search_df)
    spy.workbooks.save(workbooks, test_load.get_example_export_path(), clean=True)

    search_df = spy.workbooks.search({}, content_filter='ALL')

    workbooks = spy.workbooks.pull(search_df)
    spy.workbooks.save(workbooks, _get_exports_folder(), clean=True)

    _delete_max_capsule_duration_on_bad_metric()

    search_df = spy.workbooks.search({
        'Path': 'ACL Test Folder'
    }, content_filter='ALL')

    workbooks = spy.workbooks.pull(search_df)

    spy.workbooks.save(workbooks, _get_exports_folder())


def _delete_max_capsule_duration_on_bad_metric():
    with open(os.path.join(_get_exports_folder(),
                           'Bad Metric (0459C5F0-E5BD-491A-8DB7-BA4329E585E8)', 'Items.json'), 'r') as f:
        bad_metrics_items_json = json.load(f)

    del bad_metrics_items_json['1541C121-A38E-41C3-BFFA-AB01D0D0F30C']["Formula Parameters"][
        "Measured Item Maximum Duration"]

    del bad_metrics_items_json['1AA91F16-D476-4AF8-81AB-A2120FDA68E5']["Formula Parameters"][
        "Bounding Condition Maximum Duration"]

    with open(os.path.join(_get_exports_folder(),
                           'Bad Metric (0459C5F0-E5BD-491A-8DB7-BA4329E585E8)', 'Items.json'), 'w') as f:
        json.dump(bad_metrics_items_json, f, indent=4)


@pytest.mark.system
def test_example_export():
    workbooks = test_load.load_example_export()

    # Make sure the Topic is processed first, so that we test the logic that ensures all Topic dependencies are
    # pushed before the Topic is pushed. (Otherwise the IDs in the Topic will not be properly replaced.)
    reordered_workbooks = list()
    reordered_workbooks.extend(filter(lambda w: w['Workbook Type'] == 'Topic', workbooks))
    reordered_workbooks.extend(filter(lambda w: w['Workbook Type'] == 'Analysis', workbooks))

    status_df = spy.workbooks.push(reordered_workbooks)

    analysis_result = status_df.loc['D833DC83-9A38-48DE-BF45-EB787E9E8375']['Result']

    assert 'Success' in analysis_result


@pytest.mark.system
def test_workbook_paths():
    workbooks = test_load.load_example_export()

    # This call will put the folder of workbooks ('Example Export') in a top-level 'Use Full Path Folder'
    status_df = spy.workbooks.push(workbooks, path='Use Full Path Folder', use_full_path=True)
    analysis_result = status_df.loc['D833DC83-9A38-48DE-BF45-EB787E9E8375']['Result']
    assert 'Success' in analysis_result

    workbooks_df = spy.workbooks.search({
        'Path': 'Use Full Path Folder >> Example Export'
    })
    assert len(workbooks_df) == 2

    # This call will effectively move the folder of workbooks ('Example Export') to the root and clean out the 'Use
    # Full Path Folder'
    status_df = spy.workbooks.push(workbooks, use_full_path=True)
    analysis_result = status_df.loc['D833DC83-9A38-48DE-BF45-EB787E9E8375']['Result']
    assert 'Success' in analysis_result

    workbooks_df = spy.workbooks.search({
        'Path': 'Use Full Path Folder'
    })
    assert len(workbooks_df) == 0

    workbooks_df = spy.workbooks.search({
        'Path': 'Example Export'
    })
    assert len(workbooks_df) == 2

    # This call will move the workbooks out of the 'Example Export' folder and into the root, because the 'Search
    # Folder ID' property in the workbook gives them a no-op "relative path" such that they will be put in the folder
    # specified in the spy.workbooks.push(path='<path>') argument. Since no path argument is specified here,
    # they will be put in the root.
    status_df = spy.workbooks.push(workbooks)
    analysis_result = status_df.loc['D833DC83-9A38-48DE-BF45-EB787E9E8375']['Result']
    assert 'Success' in analysis_result

    workbooks_df = spy.workbooks.search({
        'Path': 'Example Export'
    })
    assert len(workbooks_df) == 0

    workbooks_df = spy.workbooks.search({
        'Name': '/Example (?:Analysis|Topic)/'
    })
    assert len(workbooks_df) == 2

    # Remove the "Search Folder ID" so that the workbooks have an "absolute path"
    for workbook in workbooks:
        del workbook['Search Folder ID']

    # This call will once again put the workbooks in the 'Example Export' folder, using the "absolute path" mentioned
    # above.
    status_df = spy.workbooks.push(workbooks)
    analysis_result = status_df.loc['D833DC83-9A38-48DE-BF45-EB787E9E8375']['Result']
    assert 'Success' in analysis_result

    workbooks_df = spy.workbooks.search({
        'Path': 'Example Export'
    })
    assert len(workbooks_df) == 2

    workbooks_df = spy.workbooks.search({
        'Name': '/Example (?:Analysis|Topic)/'
    })
    assert len(workbooks_df) == 0


@pytest.mark.system
def test_worksheet_order():
    workbooks = spy.workbooks.load(_get_full_path_of_export('Worksheet Order (2BBDCFA7-D25C-4278-922E-D99C8DBF6582)'))

    spy.workbooks.push(workbooks)
    workbook_item = spy.workbooks.Workbook.find_item('2BBDCFA7-D25C-4278-922E-D99C8DBF6582')

    worksheet_1 = spy.workbooks.Workbook.find_item('686B7041-D922-4256-979A-3B9BB8915E88')
    worksheet_2 = spy.workbooks.Workbook.find_item('31AF5986-00F9-4B77-B02B-BFC3603DA26B')
    worksheet_3 = spy.workbooks.Workbook.find_item('2BEC414E-2F58-45A0-83A6-AAB098812D38')

    pushed_worksheets = [
        worksheet_1.id,
        worksheet_2.id,
        worksheet_3.id
    ]

    workbooks_api = WorkbooksApi(test_common.get_client())
    worksheet_output_list = workbooks_api.get_worksheets(workbook_id=workbook_item.id)  # type: WorksheetOutputListV1
    assert len(worksheet_output_list.worksheets) == 3
    assert [w.id for w in worksheet_output_list.worksheets] == pushed_worksheets

    workbooks[0].worksheets = list(reversed(workbooks[0].worksheets))
    spy.workbooks.push(workbooks)
    worksheet_output_list = workbooks_api.get_worksheets(workbook_id=workbook_item.id)  # type: WorksheetOutputListV1
    assert len(worksheet_output_list.worksheets) == 3
    assert [w.id for w in worksheet_output_list.worksheets] == list(reversed(pushed_worksheets))

    workbooks[0].worksheets = list(filter(lambda w: w.id != '2BEC414E-2F58-45A0-83A6-AAB098812D38',
                                          reversed(workbooks[0].worksheets)))
    pushed_worksheets.remove(worksheet_3.id)
    spy.workbooks.push(workbooks)
    worksheet_output_list = workbooks_api.get_worksheets(workbook_id=workbook_item.id)  # type: WorksheetOutputListV1
    assert len(worksheet_output_list.worksheets) == 2
    assert [w.id for w in worksheet_output_list.worksheets] == pushed_worksheets


@pytest.mark.system
def test_missing_worksteps():
    with tempfile.TemporaryDirectory() as temp_folder:
        missing_worksteps_folder = os.path.join(temp_folder, 'Missing Worksteps')
        shutil.copytree(test_load.get_example_export_path(), missing_worksteps_folder)

        # Removing this workstep will cause an error because it is referenced in the Example Topic document
        os.remove(os.path.join(
            missing_worksteps_folder,
            'Example Analysis (D833DC83-9A38-48DE-BF45-EB787E9E8375)',
            'Worksheet_1F02C6C7-5009-4A13-9343-CDDEBB6AF7E6_Workstep_221933FE-7956-4888-A3C9-AF1F3971EBA5.json'))

        # Removing this workstep will cause an error because it is referenced in an Example Analysis journal
        os.remove(os.path.join(
            missing_worksteps_folder,
            'Example Analysis (D833DC83-9A38-48DE-BF45-EB787E9E8375)',
            'Worksheet_10198C29-C93C-4055-B313-3388227D0621_Workstep_FD90346A-BF72-4319-9134-3922A012C0DB.json'))

        workbooks = spy.workbooks.load(missing_worksteps_folder)

        push_df = spy.workbooks.push(workbooks, errors='catalog')

        topic_row = push_df[push_df['Name'] == 'Example Topic'].iloc[0]
        analysis_row = push_df[push_df['Name'] == 'Example Analysis'].iloc[0]

        assert '221933FE-7956-4888-A3C9-AF1F3971EBA5' in topic_row['Result']
        assert 'FD90346A-BF72-4319-9134-3922A012C0DB' in analysis_row.loc['Result']


@pytest.mark.system
def test_bad_metric():
    pushed_workbook_id = _load_and_push('Bad Metric (0459C5F0-E5BD-491A-8DB7-BA4329E585E8)')

    metrics_api = MetricsApi(test_common.get_client())

    # To see the code that this exercises, search for test_bad_metric in _workbook.py
    metric_item = spy.workbooks.Workbook.find_item('1AA91F16-D476-4AF8-81AB-A2120FDA68E5',
                                                   workbook_id=pushed_workbook_id)
    threshold_metric_output = metrics_api.get_metric(id=metric_item.id)  # type: ThresholdMetricOutputV1
    assert threshold_metric_output.bounding_condition_maximum_duration.value == 40
    assert threshold_metric_output.bounding_condition_maximum_duration.uom == 'h'

    metric_item = spy.workbooks.Workbook.find_item('1541C121-A38E-41C3-BFFA-AB01D0D0F30C',
                                                   workbook_id=pushed_workbook_id)
    threshold_metric_output = metrics_api.get_metric(id=metric_item.id)  # type: ThresholdMetricOutputV1
    assert threshold_metric_output.measured_item_maximum_duration.value == 40
    assert threshold_metric_output.measured_item_maximum_duration.uom == 'h'


@pytest.mark.system
def test_ancillaries():
    pushed_workbook_id = _load_and_push('Ancillaries (54C62C9E-629B-4A76-B8D6-5348D7D59D5F)')

    items_api = ItemsApi(test_common.get_client())

    item_search_list = items_api.search_items(
        types=['StoredSignal'],
        filters=['Data ID == Area A_Wet Bulb.sim.ts.csv'],
        scope=pushed_workbook_id,
        limit=1)  # type: ItemSearchPreviewPaginatedListV1

    assert len(item_search_list.items) == 1

    item_output = items_api.get_item_and_all_properties(id=item_search_list.items[0].id)  # type: ItemOutputV1

    wet_bulb_upper = spy.workbooks.Workbook.find_item('C33AB410-7B16-41FA-A374-BEB63900A857',
                                                      workbook_id=pushed_workbook_id)
    wet_bulb_lower = spy.workbooks.Workbook.find_item('67796251-BE83-4047-975E-89D5D5858814',
                                                      workbook_id=pushed_workbook_id)

    assert len(item_output.ancillaries) == 1
    assert len(item_output.ancillaries[0].items) == 2
    for ancillary_item in item_output.ancillaries[0].items:  # type: ItemAncillaryOutputV1
        if ancillary_item.name == 'Wet Bulb Warning Upper':
            assert ancillary_item.id == wet_bulb_upper.id
        if ancillary_item.name == 'Wet Bulb Warning Lower':
            assert ancillary_item.id == wet_bulb_lower.id

    item_search_list = items_api.search_items(
        types=['StoredSignal'],
        filters=['Data ID == Area A_Relative Humidity.sim.ts.csv'],
        scope=pushed_workbook_id,
        limit=1)  # type: ItemSearchPreviewPaginatedListV1

    assert len(item_search_list.items) == 1

    item_output = items_api.get_item_and_all_properties(id=item_search_list.items[0].id)  # type: ItemOutputV1

    humid_upper = spy.workbooks.Workbook.find_item('C2334AD9-4152-4CAA-BCA6-728A56E47F16',
                                                   workbook_id=pushed_workbook_id)
    humid_lower = spy.workbooks.Workbook.find_item('A33334D3-6E92-40F2-80E3-95B18D08FAF2',
                                                   workbook_id=pushed_workbook_id)

    # Because Relative Humidity is not present on any worksheets, the ancillary will not have been pushed. The
    # upper/lower boundary signals will have been pushed though.
    assert len(item_output.ancillaries) == 0
    assert humid_upper is not None
    assert humid_lower is not None


@pytest.mark.system
def test_archived_worksheets():
    workbooks = list()
    workbooks.extend(spy.workbooks.load(_get_full_path_of_export(
        'Archived Worksheet - Topic (F662395E-FEBB-4772-8B3B-B2D7EB7C0C3B)')))
    workbooks.extend(spy.workbooks.load(_get_full_path_of_export(
        'Archived Worksheet - Analysis (DDB5F823-3B6A-42DC-9C44-566466C2BA82)')))

    push_df = spy.workbooks.push(workbooks)

    pushed_workbook_id = push_df.iloc[0]['Pushed Workbook ID']

    archived_worksheet = spy.workbooks.Workbook.find_item('C28D3F17-C7BB-43B7-B670-41550D623CDF',
                                                          workbook_id=pushed_workbook_id)

    items_api = ItemsApi(test_common.get_client())
    assert items_api.get_property(id=archived_worksheet.id, property_name='Archived').value


@pytest.mark.system
def test_topic_links():
    # Log in slightly differently so that the URLs change
    test_common.login('http://127.0.0.1:34216')

    workbooks = list()
    workbooks.extend(spy.workbooks.load(_get_full_path_of_export(
        'Referenced By Link - Topic (1D589AC0-CA54-448D-AC3F-B3C317F7C195)')))
    workbooks.extend(spy.workbooks.load(_get_full_path_of_export(
        'Referenced By Link - Analysis (3C71C580-F1FA-47DF-B953-4646D0B1F98F)')))

    push_df = spy.workbooks.push(workbooks)

    pushed_workbook_id = push_df.iloc[0]['Pushed Workbook ID']

    document_worksheet = spy.workbooks.Workbook.find_item('4D0F99FD-8778-470B-9295-1776D587047E',
                                                          workbook_id=pushed_workbook_id)

    annotations_api = AnnotationsApi(test_common.get_client())

    annotations = annotations_api.get_annotations(
        annotates=[document_worksheet.id])  # type: AnnotationListOutputV1

    report_annotations = [a for a in annotations.items if a.type == 'Report']
    assert len(report_annotations) == 1

    annotation_output = annotations_api.get_annotation(id=report_annotations[0].id)  # AnnotationOutputV1

    assert annotation_output.document.find('http://localhost') == -1

    test_common.login()


@pytest.mark.system
def test_replace_acl():
    workbooks = spy.workbooks.load(_get_full_path_of_export(
        'ACL Test (FF092494-FB04-4578-A12E-249417D93125)'))

    # First we'll push with acls='replace,loose', which will work but won't push all the ACLs
    push_df = spy.workbooks.push(workbooks, use_full_path=True, acls='replace,loose')
    assert len(push_df) == 1
    assert push_df.iloc[0]['Result'] == 'Success'

    acl_test_workbook = spy.workbooks.Workbook.find_item('FF092494-FB04-4578-A12E-249417D93125')
    acl_test_folder = spy.workbooks.Workbook.find_item('6C513058-C1DA-4603-9498-75492B9BC119')

    items_api = ItemsApi(test_common.get_client())

    acl_output = items_api.get_access_control(id=acl_test_workbook.id)  # type: AclOutputV1
    assert len(acl_output.acl) == 1
    assert acl_output.acl[0].access_level == 'VIEW'
    assert acl_output.acl[0].identity.name == 'Everyone'
    assert acl_output.acl[0].identity.type == 'UserGroup'

    acl_output = items_api.get_access_control(id=acl_test_folder.id)  # type: AclOutputV1
    assert len(acl_output.acl) == 1
    assert acl_output.acl[0].access_level == 'VIEW'
    assert acl_output.acl[0].identity.name == 'Everyone'
    assert acl_output.acl[0].identity.type == 'UserGroup'

    # Next we'll push with acls='add,loose' and confirm that duplicate ACLs are not created
    push_df = spy.workbooks.push(workbooks, use_full_path=True, acls='add,loose')
    assert len(push_df) == 1
    assert push_df.iloc[0]['Result'] == 'Success'

    acl_output = items_api.get_access_control(id=acl_test_workbook.id)  # type: AclOutputV1
    assert len(acl_output.acl) == 1
    assert acl_output.acl[0].access_level == 'VIEW'
    assert acl_output.acl[0].identity.name == 'Everyone'
    assert acl_output.acl[0].identity.type == 'UserGroup'

    acl_output = items_api.get_access_control(id=acl_test_folder.id)  # type: AclOutputV1
    assert len(acl_output.acl) == 1
    assert acl_output.acl[0].access_level == 'VIEW'
    assert acl_output.acl[0].identity.name == 'Everyone'
    assert acl_output.acl[0].identity.type == 'UserGroup'

    with pytest.raises(_common.DependencyNotFound):
        # Now we'll try acls='replace,strict' which won't work because we don't know how to map the "Just Mark" group
        # or the "mark.derbecker@seeq.com" user
        spy.workbooks.push(workbooks, use_full_path=True, acls='replace,strict')

    # Now we'll try acls='replace,strict' again but this time provide a map that will convert the group and user to
    # the built-in Everyone and Agent API Key
    with tempfile.TemporaryDirectory() as temp:
        datasource_map = {
            "Datasource Class": "Auth",
            "Datasource ID": "Seeq",
            "Datasource Name": "Seeq",
            "RegEx-Based Maps": [
                {
                    "Old": {
                        "Type": "User",
                    },
                    "New": {
                        "Type": "User",
                        "Datasource Class": "Auth",
                        "Datasource ID": "Seeq",
                        "Username": "agent_api_key"
                    }
                },
                {
                    "Old": {
                        "Type": "UserGroup",
                    },
                    "New": {
                        "Type": "UserGroup",
                        "Datasource Class": "Auth",
                        "Datasource ID": "Seeq",
                        "Name": "Everyone"
                    }
                }
            ]
        }

        with open(os.path.join(temp, 'Datasource_Map_Auth_Seeq_Seeq.json'), 'w') as f:
            json.dump(datasource_map, f)

        spy.workbooks.push(workbooks, use_full_path=True, acls='replace,strict', datasource_map_folder=temp)

    push_df = spy.workbooks.push(workbooks, use_full_path=True, acls='replace,loose')
    assert len(push_df) == 1
    assert push_df.iloc[0]['Result'] == 'Success'

    acl_output = items_api.get_access_control(id=acl_test_workbook.id)  # type: AclOutputV1
    assert len(acl_output.acl) == 2
    assert acl_output.acl[0].access_level == 'VIEW'
    assert acl_output.acl[0].identity.name == 'Everyone'
    assert acl_output.acl[0].identity.type == 'UserGroup'
    assert acl_output.acl[1].access_level == 'FULL_CONTROL'
    assert acl_output.acl[1].identity.name == 'Agent API Key'
    assert acl_output.acl[1].identity.type == 'User'

    acl_output = items_api.get_access_control(id=acl_test_folder.id)  # type: AclOutputV1
    assert len(acl_output.acl) == 2
    assert acl_output.acl[0].access_level == 'VIEW'
    assert acl_output.acl[0].identity.name == 'Everyone'
    assert acl_output.acl[0].identity.type == 'UserGroup'
    assert acl_output.acl[1].access_level == 'FULL_CONTROL'
    assert acl_output.acl[1].identity.name == 'Everyone'
    assert acl_output.acl[1].identity.type == 'UserGroup'
