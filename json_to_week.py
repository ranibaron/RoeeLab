import glob
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# set pandas to show all columns on print
pd.set_option('display.max_columns', None)

# file management and naming
file_time = '_' + str(datetime.datetime.now())[:-7].replace(' ', '_').replace(':', '-')
data_folder = '..\\data_IDF\\shlomiIDF\\'
output_file = data_folder + 'Sleep\\full_week' + file_time + '.png'

# set week start and end
start_week = pd.to_datetime('2020-07-19 00:00:00', format='%Y-%m-%d %H:%M:%S')
end_week = pd.to_datetime('2020-07-25 23:59:59', format='%Y-%m-%d %H:%M:%S')
week = pd.date_range(start_week, end_week - datetime.timedelta(minutes=1), freq='60s')
# print(week)

# set excluded fitbits
excluded = ['sub006', 'sub030']
fig, ax = plt.subplots(1, 1)

for file in sorted(glob.glob(data_folder + '\\*\\*\\*\\*\\sleep*.json')):
    # skip excluded subjects
    subject = file.split('\\')[4]
    if subject in excluded:
        continue

    # read json file and format sleep times table
    sleep_data = pd.read_json(file, convert_dates=['startTime', 'endTime'])[['startTime', 'endTime']][::-1].reset_index(drop=True)
    data = {'time': week, 'subject': subject}
    df = pd.DataFrame(data, columns=['time', 'subject'])

    for i, sleep_segment in sleep_data.iterrows():
        # Bool of values in segment
        on_range = (df['time'] >= sleep_segment['startTime']) & (df['time'] <= sleep_segment['endTime'])

        # Use bool to plot the lines in this segment
        ax.plot(df['time'][on_range], df['subject'][on_range], c='C0', label='Subject')

# add midnight lines to plot
for time in week:
    if time.hour == 0 and time.minute == 0 and time.second == 0:
        plt.axvline(time, linewidth=.5, color='r')

# format plot
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
plt.savefig(output_file, dpi=600, facecolor='w', edgecolor='w', orientation='landscape', format=None,
            transparent=True, bbox_inches=None, pad_inches=0.1, metadata=None)
plt.show()
