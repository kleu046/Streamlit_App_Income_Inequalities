import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from css_style import get_style
from my_colors import MyColors
from text import get_explaintext, get_mytext


def set_plt_rcParams(plt):
    plt.rcParams.update(
        {
            # "font.family": "Helvetica Neue",
            "font.size": 10,
            "font.weight": "light",
            "axes.labelweight": "light",
            "axes.titlesize": 11,
            "axes.titleweight": "light",
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "figure.facecolor": MyColors.background,
            "axes.facecolor": MyColors.plot_background,
            "grid.color": MyColors.grid,
            "lines.color": MyColors.line,
            "lines.markerfacecolor": MyColors.marker,
        }
    )


def style_ax(ax: "matplotlib.axes.Axes") -> None:
    for s in ax.spines.keys():
        ax.spines[s].set_color(MyColors.axis_color)
    ax.tick_params(
        axis="x", which="major", length=3, width=2, color=MyColors.axis_color
    )
    ax.tick_params(
        axis="y", which="major", length=3, width=2, color=MyColors.axis_color
    )

    for label in ax.get_xticklabels():
        label.set_color(MyColors.axis_color)

    for label in ax.get_yticklabels():
        label.set_color(MyColors.axis_color)

    ax.grid(True, axis="x", linestyle="--", color="gray", alpha=0.3)


def plot(
    data: pd.DataFrame, gini_type_eq: str, country: str, country2: str
) -> "matplotlib.figure.Figure":
    if gini_type_eq not in ("gini_mi_eq", "gini_dhi_eq"):
        raise ValueError("gini_type_eq must be either 'gini_mi_eq' or 'gini_dhi_eq'")

    set_plt_rcParams(plt)

    min_year, max_year = data.Year.min(), data.Year.max()
    year_list = np.arange(min_year, max_year + 1, 1).tolist()

    # Aggregate global median data
    df = (
        data[["Year", gini_type_eq]]
        .groupby("Year")
        .median()
        .reset_index()
        .sort_values("Year")
    )

    fig, ax = plt.subplots(
        3,
        1,
        figsize=(10, 8),
        gridspec_kw={"height_ratios": [3, 1, 1]},
        sharex=True,
    )
    fig.tight_layout(pad=3)
    fig.patch.set_facecolor("#FFFFFF")

    main_color = "#6590EB"  # blue for global & first country
    secondary_color = "#F77474"  # red for second country

    # ---- Bottom subplot: Global Median ----
    ax[2].plot(
        df["Year"].astype(int),
        df[gini_type_eq],
        ls="-",
        marker="o",
        markerfacecolor="#7A7A7A",
        color="#383838",
        linewidth=1.3,
        markersize=4,
        alpha=0.9,
    )

    # ---- Top subplot: Country Gini ----
    mask1 = data["Entity"] == country
    mask2 = data["Entity"] == country2

    # First country
    if country:
        ax[0].plot(
            data[mask1]["Year"].astype(int),
            data[mask1][gini_type_eq],
            ls="-",
            marker="o",
            markersize=8,
            markerfacecolor="none",
            markeredgecolor=main_color,
            markeredgewidth=1,
            color=main_color,
            linewidth=1,
            alpha=0.9,
            label=country,
        )

    # Second country
    if country2:
        ax[0].plot(
            data[mask2]["Year"].astype(int),
            data[mask2][gini_type_eq],
            ls="-",
            marker="o",
            markersize=8,
            markerfacecolor="none",
            markeredgecolor=secondary_color,
            markeredgewidth=1,
            color=secondary_color,
            linewidth=1,
            alpha=0.9,
            label=country2,
        )

    # ---- Middle subplot: Delta vs Global Median ----
    delta1 = data[mask1].merge(df, on="Year", how="left")
    ax[1].axhline(y=0, color="#9CA3AF", linestyle="--", linewidth=1)

    bar_width = 0.4

    delta2 = data[mask2].merge(df, on="Year", how="left")
    if country2 and country:
        x = delta1["Year"].astype(int)
        ax[1].bar(
            x - bar_width / 2,
            height=delta1[f"{gini_type_eq}_x"] - delta1[f"{gini_type_eq}_y"],
            width=bar_width,
            color=main_color,
            alpha=0.7,
            label=country,
        )

        x = delta2["Year"].astype(int)
        ax[1].bar(
            x + bar_width / 2,
            height=delta2[f"{gini_type_eq}_x"] - delta2[f"{gini_type_eq}_y"],
            width=bar_width,
            color=secondary_color,
            alpha=0.7,
            label=country2,
        )
    elif country:
        ax[1].bar(
            delta1["Year"].astype(int) - bar_width / 2,
            height=delta1[f"{gini_type_eq}_x"] - delta1[f"{gini_type_eq}_y"],
            width=bar_width,
            color=main_color,
            alpha=0.7,
            label=country,
        )
    elif country2:
        ax[1].bar(
            delta2["Year"].astype(int) - bar_width / 2,
            height=delta2[f"{gini_type_eq}_x"] - delta2[f"{gini_type_eq}_y"],
            width=bar_width,
            color=secondary_color,
            alpha=0.7,
            label=country2,
        )

    # styling
    ax[2].spines["right"].set_visible(False)
    ax[2].spines["top"].set_visible(False)
    ax[1].spines["right"].set_visible(False)
    ax[1].spines["top"].set_visible(False)
    ax[1].spines["bottom"].set_visible(False)
    ax[0].spines["bottom"].set_visible(False)
    ax[0].spines["top"].set_visible(False)
    ax[0].spines["right"].set_visible(False)

    ax[2].set_xticks(year_list[::10])
    ax[2].set_xlim(min_year, max_year)

    style_ax(ax[2])
    style_ax(ax[1])
    style_ax(ax[0])

    if country or country2:
        ax[0].legend(ncol=2)
        ax[1].legend(ncol=2)

    ax[2].set_title(
        "   Global Median Gini (Of Available Data)",
        loc="left",
        fontsize=12,
        fontweight="light",
        color=MyColors.axis_color,
    )

    ax[0].set_title(
        "   Country Gini Trends",
        loc="left",
        fontsize=12,
        fontweight="light",
        color=MyColors.axis_color,
    )

    ax[1].set_title(
        "   Gap vs Global Median",
        loc="left",
        fontsize=12,
        fontweight="light",
        color=MyColors.axis_color,
    )

    plt.subplots_adjust(hspace=0.5)

    return fig


st.set_page_config(layout="wide")

st.markdown(get_style(), unsafe_allow_html=True)


data = pd.read_csv("income_inequality_processed.csv").sort_values(["Entity", "Year"])


most_recent_by_country = (
    data[["Year", "Entity"]]
    .groupby(["Entity"])
    .max()
    .reset_index()
    .merge(data, on=["Year", "Entity"], how="left")
)


gini_type = st.sidebar.selectbox(
    "Select Gini Coefficient Type",
    ["Before Tax", "After Tax"],
    # format_func=lambda x: "Before Tax" if x == "gini_mi_eq" else "After Tax"
)

country = st.sidebar.selectbox(
    "Select Country",
    data.Entity.unique().tolist(),
    index=data.Entity.unique().tolist().index("United Kingdom"),
)

country2 = st.sidebar.selectbox(
    "Select Another Country For Comparison",
    data.Entity.unique().tolist(),
    index=data.Entity.unique().tolist().index("United States"),
)

gini_type_eq = "gini_mi_eq" if gini_type == "Before Tax" else "gini_dhi_eq"


st.pyplot(plot(data, gini_type_eq, country, country2))

st.write(get_explaintext(), unsafe_allow_html=True)

st.write("")
st.write("")

st.write(get_mytext(), unsafe_allow_html=True)
