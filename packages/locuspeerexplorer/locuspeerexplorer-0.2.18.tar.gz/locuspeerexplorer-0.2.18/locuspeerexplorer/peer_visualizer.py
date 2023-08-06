import pandas as pd
import seaborn as sn
import datetime

import os
import matplotlib
import matplotlib.pyplot as plt
from . import peer_explorer, peer_finder

dirname, filename = os.path.split(os.path.abspath(__file__))
matplotlib.use("MacOSX", warn=False, force=True)


def _code2name(df_data, area):
    name = list(df_data[df_data["AREA"] == area].AREA_NAME)[0]
    if ',' in name:
        area = name.split(",")[0]
        state = name.split(",")[1]
        area = area.split("-")[0]
        state = state.split("-")[0]
        name = area.strip() + " (" + state.strip() + ")"
    return name


def _fm_string(fm):
    fm = fm.split("-")[0]
    fm = " ".join([x.capitalize() for x in fm.split("_")])
    return fm


def _time_string():
    now = datetime.datetime.now()
    return "_".join([str(x) for x in [now.month, now.day, now.hour, now.minute]])


def add_mean_row(df_data, subset_area=None, col_dim="AREA"):
    df_data = df_data.set_index(col_dim).T
    df_data["mean"] = df_data.mean(axis=1)
    df_data = (df_data.T).reset_index()
    return df_data


def bar_all_fm(df_data, area, peers, cols,
               limit_fms=10, save_fig=True, show=False):
    plt.clf()
    cols = cols[:limit_fms]
    for i, c in enumerate(cols):
        if 'LQ' in c:
            cols[i] = c.split('-')[0]+'-PC_EMPL'
    df_data = df_data.dropna(subset=cols, how="any")
    name = _code2name(df_data, area)
    fm = [_fm_string(col) for col in cols]

    def group(x):
        if x in peers:
            return 'Peer group average'
        elif x == area:
            return name
        else:
            return 'All other average'
    df_data["Peer"] = df_data['AREA'].apply(group)
    df_data["NAME"] = df_data["AREA_NAME"].apply(lambda x: x.split(",")[0][:12])
    df_peers = df_data[df_data["AREA"].isin(peers)]
    df_others = df_data[~df_data["AREA"].isin(peers)]

    # sn.set(rc={'figure.figsize':(30,8.27)})
    df_data = df_data.groupby('Peer')[cols].mean()
    df_data = df_data.stack().reset_index()
    df_data.columns = ['Areas', 'FM', 'Concentration']
    df_data['Concentration'] = df_data['Concentration'].apply(lambda x: 100*x)
    df_data['FM'] = df_data['FM'].apply(_fm_string)

    fig = sn.barplot(x='FM', y='Concentration', data=df_data, hue='Areas',
                     hue_order=[name, 'Peer group average', 'All other average'],
                     palette="viridis")
    fig.set_ylabel('Concentration of FM (in %)')
    fig.set_xticklabels(labels=df_data['FM'], rotation=20,
                        horizontalalignment='right', fontsize='medium')
    plt.tight_layout()
    plt.show()


def duo_fm_viz(df_data, area, peers, col, save_fig=True, show=False):
    plt.clf()

    if 'LQ' in col:
        col = col.split('-')[0]+'-PC_EMPL'

    df_data = df_data.dropna(subset=[col], how="any")
    if not os.path.exists(os.path.join(dirname, "../results/")):
        os.mkdir(os.path.join(dirname, "../results/"))
    name = _code2name(df_data, area)
    fm = _fm_string(col)
    df_data[col] = df_data[col].apply(lambda x: 100*x)
    df_data["Peer"] = df_data.apply(
        lambda x: "Peers" if (x.AREA) in peers else "Others", axis=1
    )

    fig, axes = plt.subplots(figsize=(10, 10), ncols=2)
    df_data["NAME"] = df_data["AREA_NAME"].apply(lambda x: x[:15])
    subdata = df_data[df_data["AREA"].isin(peers)]
    subdata.sort_values(by=col, inplace=True)
    y = df_data[col].median()
    q1 = df_data[col].quantile(0.25)
    q3 = df_data[col].quantile(0.75)
    sn.barplot(x=col, y="NAME", palette=sn.color_palette("Blues",
                                                         n_colors=len(peers)+1),
               data=subdata,
               ax=axes[0])
    axes[0].axvline(x=y, c="#ef8d22ff", label='National Median')
    axes[0].axvline(x=q1, ls="--", lw=0.5, c="#ef8d22ff", label='1st quantile')
    axes[0].axvline(x=q3, ls="--", lw=0.5, c="#ef8d22ff", label='3rd quantile')
    axes[0].set_xlabel(f"")
    axes[0].set_ylabel(f"")

    axes[0].text(1.01*q1, 0, "1st quantile", rotation=90,
                 color='#ef8d22ff', va='top',
                 fontsize='large',
                 fontweight='bold')
    axes[0].text(1.01*q3, 0, "3rd quantile", rotation=90,
                 color='#ef8d22ff', va='top',
                 fontsize='large',
                 fontweight='bold')
    axes[0].text(1.01*y, 0, "National median", rotation=90,
                 color='#ef8d22ff', va='top',
                 fontsize='large',
                 fontweight='bold')

    # for tick in axes[0][0].get_xticklabels():
    #     tick.set_rotation(30)
    bin = df_data[col].std()/3
    sn.kdeplot(
        list(df_data[col]),
        # color="blue",
        bw=bin,
        shade=True,
        ax=axes[1],
        color='#ef8d22ff',
        label=f'National distribution'
    )
    for i, p in enumerate(list(subdata['AREA'])):
        val = df_data[df_data['AREA'] == p][col].iloc[0]
        axes[1].axvline(x=val, lw=1,
                        c=sn.color_palette("Blues",
                                           n_colors=subdata.shape[0]).as_hex()[i],
                        )

    axes[1].set_ylabel("% of all areas")
    axes[1].set_xlabel(f"")
    plt.legend(loc='upper right')
    plt.xlabel(f"Concentration of {fm} (in %)")

    fig.suptitle(f"{name} and its peers for the {fm} FM", fontsize=16)
    plt.tight_layout(rect=[0, 0.1, 1, 0.90])
    if save_fig:
        time = _time_string()
        plt.savefig(os.path.join(dirname, f"../results/quadrant_area_{col}.png"))
        print(
            f'File saved in {os.path.join(dirname, f"../results/quadrant_area_{col}.png")}'
        )
    if show:
        plt.show()


if __name__ == "__main__":
    dirname, filename = os.path.split(os.path.abspath(__file__))
    df_data = pd.read_csv(
        os.path.join(dirname, "../data/processed/metrics_outcomes.csv")
    )
    df_data = df_data[df_data["YEAR"] == 2016]
    peers, fms = peer_finder.get_top_n_fms_peers(
        df_data, area=35620, year=2016, n_peers=5, n_fms=5
    )
    area = 35620
    bar_all_fm(df_data, area, peers, fms)
    # barplot_me_vs_peers(df_data, [35620] + peers, col=fms[1])
    # boxplot_peers_vs_nat(df_data, [35620] + peers, col=fms[1])
    # hist_peers_vs_nat(df_data, [35620] + peers, col=fms[1])
    duo_fm_viz(df_data, area, [35620] + peers, col=fms[3], show=True)
