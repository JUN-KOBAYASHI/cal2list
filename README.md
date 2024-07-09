# Yearly Calendar and Event List Generator

This script reads an iCal file and generates a yearly calendar as a PDF file. It also outputs an event list as a CSV file.

## Requirements

- Python 3.x
- Required Python libraries: `icalendar`, `pandas`, `matplotlib`, `japanize_matplotlib`
  
You can install the required libraries using pip:

```sh
pip install icalendar pandas matplotlib japanize_matplotlib
```

## Usage

To run the script, use the following command:
```sh
python script_name.py /path/to/your/ical/file.ical /path/to/output/calendar.pdf 2024
```

Replace script_name.py with the name of the script file. The parameters are as follows:

- /path/to/your/ical/file.ical: Path to the iCal file containing the events.
- /path/to/output/calendar.pdf: Path to the output PDF file where the yearly calendar will be saved. The event list will also be saved as a CSV file with the same name but with a .csv extension.
- 2024: The year for which the calendar will be generated.

output: calendar.pdf , calendar.csv

## License

This project is licensed under the MIT License.


  
