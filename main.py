import argparse

from auth.google_service_auth import GoogleServiceAuth
from data_transfer.data_transfer_manager import DataTransferManager


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

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
