import singlebar
import xlsreader


def main(only_create_anim=False):
    reader = xlsreader.XlsReader(name=r'data.xlsx')
    chart_keys, chart_labels, chart_values = reader.read()
    bar_chart = singlebar.SingleBar(chart_keys, chart_labels, chart_values, alpha_ani=True, pos_ani=True)
    if only_create_anim:
        for idx in range(len(chart_keys)):
            bar_chart.gen_bar_chart(chart_idx=idx, save_file=True, show_chart=False)
    else:
        bar_chart.gen_bar_chart(chart_idx=0, save_file=False, show_chart=True)


if __name__ == '__main__':
    main(only_create_anim=False)
