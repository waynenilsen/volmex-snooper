
from plotnine import *
import pandas
import numpy
import datetime
import mizani.breaks

def get_data():
    data = pandas.read_csv('data.csv')
    data['asof'] = data['asof'].apply(numpy.datetime64)
    return data

def get_label(field):
    return {
        'asof': 'Time',
        'total_diff': '250 - Long - Short',
        'index_diff': 'Long - Index'
    }[field]


def format_date(breaks):
    """
    Function to format the date
    """
    res = []
    for x in breaks:
        if x.hour == 0:
            fmt = '%a'
        elif x.hour % 12 == 0:
            fmt = '%H'
        else:
            fmt = ''

        res.append(datetime.date.strftime(x, fmt))

    return res

def custom_date_breaks(width):
    """
    Create a function that calculates date breaks

    It delegates the work to `date_breaks`
    """
    def filter_func(limits):
        breaks = mizani.breaks.date_breaks(width)(limits)
        # filter
        return [x for x in breaks if x.hour % 12 == 0]

    return filter_func

def plot(data, field):
    print(
        ggplot(data, aes('asof', field, color='asset'))
        + scale_x_datetime(
            breaks=custom_date_breaks('1 hour'),
            labels=format_date)
        + geom_line()
        + theme_bw()
        + theme(subplots_adjust={'right': 0.85})
        + xlab(get_label('asof'))
        + ylab(get_label(field))
        + ggtitle(get_label(field) + ' vs ' + get_label('asof'))
    )

def main():
    data = get_data()
    data['total_diff'] = 250-data['long']-data['short']
    data['index_diff'] = data['long'] - data['index']
    plot(data, 'total_diff')
    plot(data, 'index_diff')

if __name__ == '__main__':
    main()