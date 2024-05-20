from typing import Union, List, Dict, Any, Optional

from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from pretty_utils.miscellaneous.files import join_path


def read_spreadsheet(path: Union[str, tuple, list], sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
    path = join_path(path)
    spreadsheet = load_workbook(path)
    if sheet_name:
        sheet: Worksheet = spreadsheet[sheet_name]

    else:
        sheet: Worksheet = spreadsheet.active

    headers = [cell.value for cell in list(sheet.rows)[0]]
    rows = []
    for row in list(sheet.rows)[1:]:
        row = [cell.value for cell in row]
        rows.append(dict(zip(headers, row)))

    return rows
