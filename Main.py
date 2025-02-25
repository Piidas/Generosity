import logging
import os
import sys

from ConfigHandler import ConfigHandler
from src.BookingStatementHandler import BookingStatementHandler
from src.ImportHandler import ImportHandler

# Clear any existing logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler that writes to an absolute path
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Main.log")
fh = logging.FileHandler(log_file, mode='w')
fh.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(file_formatter)
logger.addHandler(fh)

# Also add a console handler so you can see logs in the PyCharm console
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(console_formatter)
logger.addHandler(ch)

logging.debug("Logging is now configured.")

# logging.basicConfig(level=logging.DEBUG, filename='Main.log')
# logging.basicConfig(level=logging.ERROR)

# Get the Instances
imp = ImportHandler()
config = ConfigHandler()

# Importieren des Kapitalflussberichts - aktuell nur manuell
print(os.getcwd())
import_filename = config.get_statement_of_funds_name()
open_position_filename = config.get_file_open_positions_name()
print(import_filename)
imp.import_ib_xml_manual(import_filename)

for key in config.get_ib_accounts():
    imp.import_open_position(key, "Backup_OpenPositions.xlsx")

for key in open_position_filename:
    imp.import_open_position(key, open_position_filename[key])

# Erstellen der Buchungssätze
accounts_to_process = config.get_ib_accounts()
account_mapping = config.get_ib_to_accounting_map()
start_date = config.get_start_date()
end_date = config.get_end_date()
bookings = BookingStatementHandler(accounts_to_process, account_mapping, start_date, end_date)

accounts_to_combine = config.get_ib_acc_combination()
bookings.generate_booking_journal(accounts_to_combine)
