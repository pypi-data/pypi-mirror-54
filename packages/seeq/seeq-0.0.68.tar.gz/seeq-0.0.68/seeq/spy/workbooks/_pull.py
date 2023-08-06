from .. import _common
from ._workbook import *
from ... import spy
from .._common import Status


def pull(workbooks_df, *, include_referenced_workbooks=True, errors='raise', quiet=False, status=None):
    status = Status.validate(status, quiet)
    _common.validate_errors_arg(errors)

    if len(workbooks_df) == 0:
        status.update('workbooks_df is empty', Status.SUCCESS)
        return list()

    for required_column in ['ID', 'Type', 'Workbook Type']:
        if required_column not in workbooks_df.columns:
            raise RuntimeError('"%s" column must be included in workbooks_df' % required_column)

    status_columns = list()

    for col in ['ID', 'Name', 'Workbook Type']:
        if col in workbooks_df:
            status_columns.append(col)

    workbooks_df = workbooks_df[workbooks_df['Type'] != 'Folder']

    status.df = workbooks_df[status_columns].copy().reset_index(drop=True)
    status.df['Count'] = 0
    status.df['Time'] = 0
    status.df['Result'] = 'Queued'
    status_columns.extend(['Count', 'Time', 'Result'])

    status.update('Pulling workbooks', Status.RUNNING)

    results = list()
    analyses_to_pull = dict()
    referencing_search_folder_id = dict()

    # First we iterate through all the Topics and scrape all the Analyses and specific worksheet/worksteps to pull
    for index, row in workbooks_df.iterrows():
        item_id = _common.get(row, 'ID')

        try:
            if _common.get(row, 'Workbook Type') == 'Analysis':
                if item_id not in analyses_to_pull:
                    analyses_to_pull[item_id] = set()

                continue

            timer = _common.timer_start()
            status.df.at[status.df['ID'] == item_id, 'Result'] = 'Pulling'

            workbook = Workbook.pull(item_id, status=status)  # type: Workbook

            if include_referenced_workbooks and _common.get(row, 'Workbook Type') == 'Topic':
                def _add_if_necessary(_workbook_id, _workstep_tuples):
                    if _workbook_id not in analyses_to_pull:
                        analyses_to_pull[_workbook_id] = set()
                        if len(status.df[status.df['ID'] == _workbook_id]) == 0:
                            to_add_df = spy.workbooks.search({'ID': _workbook_id}, quiet=True)
                            if len(to_add_df) == 1:
                                to_add_df['Count'] = 0
                                to_add_df['Time'] = 0
                                to_add_df['Result'] = 'Queued'
                                status.df.loc[len(status.df)] = to_add_df.iloc[0][status_columns]

                    analyses_to_pull[_workbook_id].update(_workstep_tuples)
                    referencing_search_folder_id[_workbook_id] = _common.get(row, 'Search Folder ID')

                for workbook_id, workstep_tuples in workbook.referenced_workbooks.items():
                    _add_if_necessary(workbook_id, workstep_tuples)

                for workbook_id, workstep_tuples in workbook.find_workbook_links().items():
                    _add_if_necessary(workbook_id, workstep_tuples)

            if _common.present(row, 'Search Folder ID'):
                workbook['Search Folder ID'] = _common.get(row, 'Search Folder ID')

            results.append(workbook)

            status.df.at[status.df['ID'] == item_id, 'Time'] = _common.timer_elapsed(timer)
            status.df.at[status.df['ID'] == item_id, 'Result'] = 'Success'

        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                status.df['Result'] = 'Canceled'
                status.update('Pull canceled', Status.CANCELED)
                return None

            if errors == 'raise':
                raise

            status.df.at[status.df['ID'] == item_id, 'Result'] = _common.format_exception(e)

    # Now iterate through the Analyses
    for workbook_id, workstep_tuples in analyses_to_pull.items():
        timer = _common.timer_start()

        try:
            workbook = Workbook.pull(workbook_id, status=status, extra_workstep_tuples=workstep_tuples)

            workbook_row = workbooks_df[workbooks_df['ID'] == workbook_id]
            if len(workbook_row) == 1 and 'Search Folder ID' in workbook_row.columns:
                workbook['Search Folder ID'] = workbook_row.iloc[0]['Search Folder ID']
            elif workbook_id in referencing_search_folder_id and referencing_search_folder_id[workbook_id] is not None:
                # If the workbook was pulled only as a result of being referenced by something else (like a Topic),
                # we don't have a specific Search Folder ID to use. So just use the search folder ID of the referencing
                # item. (Note: If it's referenced by multiple things, then "last one wins".)
                workbook['Search Folder ID'] = referencing_search_folder_id[workbook_id]

            results.append(workbook)

            status.df.at[status.df['ID'] == workbook_id, 'Time'] = _common.timer_elapsed(timer)
            status.df.at[status.df['ID'] == workbook_id, 'Result'] = 'Success'

        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                status.df['Result'] = 'Canceled'
                status.update('Pull canceled', Status.CANCELED)
                return None

            if errors == 'raise':
                raise

            status.df.at[status.df['ID'] == workbook_id, 'Result'] = _common.format_exception(e)

    status.update('Pull successful', Status.SUCCESS)

    return results
