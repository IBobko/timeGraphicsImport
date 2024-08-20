import argparse

from auth.google_service_auth import GoogleServiceAuth
from data_transfer.data_transfer_manager import DataTransferManager
from data_transfer.google_drive_handler import GoogleDriveHandler
from utils import clean_filename


def run_import(args):
    auth = GoogleServiceAuth()
    manager = DataTransferManager(excel_file_path=args.excel_file_path, spreadsheet_id=args.spreadsheet_id, auth=auth)
    manager.clear_google_sheets_range('Sheet1!A4:L')
    manager.transfer_events_to_sheets()
    manager.transfer_periods_to_sheets()


def run_compare(args):
    print("compare")
    DataTransferManager.compare_excel_files(args.excel_file_path1, args.excel_file_path2, 'Events')
    DataTransferManager.compare_excel_files(args.excel_file_path1, args.excel_file_path2, 'Periods')


def run_create_sheet(args):
    auth = GoogleServiceAuth()
    manager = GoogleDriveHandler(auth=auth)
    clean_name = clean_filename(args.filename)
    file_name = f"{clean_name}Time.Graphics"
    existing_file_id = manager.find_file_by_name(file_name)
    mime_type = 'application/vnd.google-apps.spreadsheet'
    if existing_file_id:
        print(f"File already exists with ID: {existing_file_id}")
    else:
        sheet_id = manager.create_file(file_name, mime_type)
        manager.share_file(file_id=sheet_id, user_email="iibobko@gmail.com", role="writer")
        print(f"Sheet created with ID: {sheet_id}")


def run_delete_sheet(args):
    auth = GoogleServiceAuth()
    manager = GoogleDriveHandler(auth=auth)
    manager.delete_file(args.file_id)


def main():
    parser = argparse.ArgumentParser(description="Excel and Google Sheets data management.")
    subparsers = parser.add_subparsers(title='commands', help='command help')

    import_parser = subparsers.add_parser('import', help='Import data to Google Sheets')
    import_parser.add_argument("--excel_file_path", required=True)
    import_parser.add_argument("--spreadsheet_id", required=True)
    import_parser.set_defaults(func=run_import)

    compare_parser = subparsers.add_parser('compare', help='Compare two Excel files')
    compare_parser.add_argument("--excel_file_path1", required=True)
    compare_parser.add_argument("--excel_file_path2", required=True)
    compare_parser.set_defaults(func=run_compare)

    # New create_sheet command
    create_sheet_parser = subparsers.add_parser('createSheet', help='Create a new sheet in Google Drive')
    create_sheet_parser.add_argument("--filename", required=True, help="local file name")
    create_sheet_parser.set_defaults(func=run_create_sheet)

    # New create_sheet command
    create_sheet_parser = subparsers.add_parser('deleteSheet', help='Delete a sheet in Google Drive')
    create_sheet_parser.add_argument("--file_id", required=True, help="file id")
    create_sheet_parser.set_defaults(func=run_delete_sheet)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
