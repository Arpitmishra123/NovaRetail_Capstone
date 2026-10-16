import os
import pandas as pd
import matplotlib.pyplot as plt

file_path = "assets/novaretail_dataset.xlsx"
output_folder = "charts"

os.makedirs(output_folder, exist_ok=True)

regional_data = pd.read_excel(
    file_path,
    sheet_name="Regional_Performance"
)

customer_data = pd.read_excel(
    file_path,
    sheet_name="Customer_Experience"
)

risk_data = pd.read_excel(
    file_path,
    sheet_name="Operational_Risk"
)

print("Datasets loaded successfully.")


region_colors = {
    "North America": "#1F4E79",
    "Europe": "#70AD47",
    "APAC": "#5B9BD5",
    "Latin America": "#C0504D"
}

# ========================================
# CHART 1: REGIONAL REVENUE TREND
# ========================================

plt.figure(figsize=(10, 5.5))

for region in regional_data["Region"].unique():

    region_df = regional_data[
        regional_data["Region"] == region
    ]

    plt.plot(
        region_df["Quarter"],
        region_df["Revenue_USD_M"],
        marker="o",
        linewidth=2.5,
        markersize=7,
        label=region,
        color=region_colors.get(region)
    )

plt.title(
    "Quarterly Revenue Trend by Region",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Quarter")
plt.ylabel("Revenue (USD M)")

plt.legend(
    frameon=False,
    ncol=2
)

plt.grid(
    axis="y",
    alpha=0.25
)

plt.tight_layout()

revenue_chart_path = os.path.join(
    output_folder,
    "slide_2_revenue.png"
)

plt.savefig(
    revenue_chart_path,
    dpi=200,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

print(
    "Revenue chart created:",
    revenue_chart_path
)


# ========================================
# CHART 2: NPS TREND
# ========================================

plt.figure(figsize=(10, 5.5))

for region in customer_data["Region"].unique():

    region_df = customer_data[
        customer_data["Region"] == region
    ]

    plt.plot(
        region_df["Quarter"],
        region_df["NPS"],
        marker="o",
        linewidth=2.5,
        markersize=7,
        label=region,
        color=region_colors.get(region)
    )

plt.title(
    "Net Promoter Score Trend by Region",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Quarter")
plt.ylabel("NPS")

plt.legend(
    frameon=False,
    ncol=2
)

plt.grid(
    axis="y",
    alpha=0.25
)

plt.tight_layout()

nps_chart_path = os.path.join(
    output_folder,
    "slide_3_nps.png"
)

plt.savefig(
    nps_chart_path,
    dpi=200,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

print(
    "NPS chart created:",
    nps_chart_path
)


# ========================================
# CHART 3: STOCKOUT RISK
# ========================================

quarters = sorted(
    risk_data["Quarter"].dropna().unique()
)

latest_quarter = quarters[-1]

latest_risk = risk_data[
    risk_data["Quarter"] == latest_quarter
].copy()


bar_colors = [
    region_colors.get(region, "#808080")
    for region in latest_risk["Region"]
]


plt.figure(figsize=(10, 5.5))

bars = plt.bar(
    latest_risk["Region"],
    latest_risk["Stockout_Rate_pct"],
    color=bar_colors
)

plt.title(
    f"Stockout Rate by Region - {latest_quarter}",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Region")
plt.ylabel("Stockout Rate (%)")

plt.grid(
    axis="y",
    alpha=0.25
)

plt.tight_layout()


for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10
    )


    risk_chart_path = os.path.join(
    output_folder,
    "slide_4_stockout.png"
)

plt.savefig(
    risk_chart_path,
    dpi=200,
    bbox_inches="tight",
    facecolor="white"
)

plt.close()

print(
    "Stockout chart created:",
    risk_chart_path
)