import icalendar
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import japanize_matplotlib
import calendar
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os

# Function to read iCal file
def read_ical(file_path):
    with open(file_path, 'rb') as f:
        gcal = icalendar.Calendar.from_ical(f.read())
    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            event = {}
            event['summary'] = str(component.get('summary'))
            dtstart = component.get('dtstart').dt
            if isinstance(dtstart, datetime):
                dtstart = dtstart.date()  # Convert datetime.datetime to datetime.date
            event['dtstart'] = dtstart
            events.append(event)
    return events

# Function to truncate title to specified length
def truncate_title(title, max_length=30):
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title

# Function to create yearly calendar
def create_yearly_calendar(events, year, output_file):
    # Filter events for the specified year
    events = [event for event in events if event['dtstart'].year == year]
    
    with PdfPages(output_file) as pdf:
        fig, axs = plt.subplots(3, 4, figsize=(20, 15))
        fig.suptitle(f'{year} Calendar', fontsize=20)

        max_events_per_day = max(len([event for event in events if event['dtstart'] == datetime(year, month, day).date()]) for month in range(1, 13) for day in range(1, 32) if calendar.monthrange(year, month)[1] >= day)
        
        for month in range(1, 13):
            ax = axs[(month-1)//4, (month-1)%4]
            cal = calendar.monthcalendar(year, month)
            ax.set_title(calendar.month_name[month], fontsize=15)
            ax.axis('off')
            table_data = [['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']]
            for week in cal:
                row = []
                for day in week:
                    if day == 0:
                        row.append('')
                    else:
                        day_events = [event['summary'] for event in events if event['dtstart'] == datetime(year, month, day).date()]
                        num_events = len(day_events)
                        if num_events:
                            color_intensity = int(255 - (num_events / max_events_per_day) * 200)
                            color_hex = f'#{color_intensity:02x}cccc'
                            row.append(f'{day}\n')
                        else:
                            row.append(day)
                table_data.append(row)
            table = ax.table(cellText=table_data, cellLoc='center', loc='center', colWidths=[0.1]*7)
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 2)
            for i in range(len(table_data)):
                for j in range(len(table_data[0])):
                    cell = table[(i, j)]
                    if i == 0:
                        cell.set_fontsize(12)
                        cell.set_text_props(weight='bold')
                    if '\n' in str(cell.get_text().get_text()):
                        num_events = len([event['summary'] for event in events if event['dtstart'] == datetime(year, month, int(cell.get_text().get_text().split('\n')[0])).date()])
                        color_intensity = int(255 - (num_events / max_events_per_day) * 200)
                        color_hex = f'#{color_intensity:02x}cccc'
                        cell.set_facecolor(color_hex)

        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

        # Add event list pages
        event_data = sorted(events, key=lambda x: x['dtstart'])
        rows_per_page = 40
        pages = [event_data[i:i + rows_per_page] for i in range(0, len(event_data), rows_per_page)]

        for page in pages:
            fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 size
            ax.axis('off')
            table_data = [['Date', 'Event']]
            for event in page:
                truncated_summary = truncate_title(event['summary'])
                table_data.append([event['dtstart'].strftime('%Y-%m-%d'), truncated_summary])
            table = ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center', colWidths=[0.3, 0.7])
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 2)
            pdf.savefig(fig)
            plt.close()

    # CSV output
    csv_file = os.path.splitext(output_file)[0] + ".csv"
    csv_data = [{'Date': event['dtstart'].strftime('%Y-%m-%d'), 'Event': event['summary']} for event in event_data]
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Read an iCal file and create a yearly calendar')
    parser.add_argument('ical_file', type=str, help='Path to the iCal file')
    parser.add_argument('output_file', type=str, help='Path to the output PDF file')
    parser.add_argument('year', type=int, help='Year for the calendar')
    
    args = parser.parse_args()
    
    events = read_ical(args.ical_file)
    create_yearly_calendar(events, args.year, args.output_file)
