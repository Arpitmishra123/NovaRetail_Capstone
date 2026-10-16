import pandas as pd
import json

file_path = "assets/novaretail_dataset.xlsx"

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

print("All three datasets loaded successfully.")

quarters = regional_data["Quarter"].dropna().unique().tolist()
quarters = sorted(quarters)

print("\nAvailable Quarters:")
print(quarters)

latest_quarter = quarters[-1]
previous_quarter = quarters[-2]

print("\nLatest Quarter:", latest_quarter)
print("Previous Quarter:", previous_quarter)

latest_regional = regional_data[
    regional_data["Quarter"] == latest_quarter
]

previous_regional = regional_data[
    regional_data["Quarter"] == previous_quarter
]

latest_total_revenue = latest_regional["Revenue_USD_M"].sum()

previous_total_revenue = previous_regional["Revenue_USD_M"].sum()

qoq_revenue_growth = (
    (latest_total_revenue - previous_total_revenue)
    / previous_total_revenue
) * 100


print("\n===== OVERALL REVENUE PERFORMANCE =====")

print(
    "Latest Quarter Total Revenue:",
    latest_total_revenue,
    "USD M"
)

print(
    "Previous Quarter Total Revenue:",
    previous_total_revenue,
    "USD M"
)

print(
    "QoQ Revenue Growth:",
    round(qoq_revenue_growth, 2),
    "%"
)

revenue_pivot = regional_data.pivot(
    index="Region",
    columns="Quarter",
    values="Revenue_USD_M"
)

revenue_pivot["QoQ_Growth_pct"] = (
    (
        revenue_pivot[latest_quarter]
        - revenue_pivot[previous_quarter]
    )
    / revenue_pivot[previous_quarter]
) * 100


print("\n===== REGION-WISE REVENUE =====")

print(
    revenue_pivot[
        [
            previous_quarter,
            latest_quarter,
            "QoQ_Growth_pct"
        ]
    ].round(2)
)

best_growth_region = revenue_pivot[
    "QoQ_Growth_pct"
].idxmax()

best_growth_value = revenue_pivot.loc[
    best_growth_region,
    "QoQ_Growth_pct"
]

weakest_growth_region = revenue_pivot[
    "QoQ_Growth_pct"
].idxmin()

weakest_growth_value = revenue_pivot.loc[
    weakest_growth_region,
    "QoQ_Growth_pct"
]


print("\n===== GROWTH HIGHLIGHTS =====")

print(
    "Best Growth Region:",
    best_growth_region,
    round(best_growth_value, 2),
    "%"
)

print(
    "Weakest Growth Region:",
    weakest_growth_region,
    round(weakest_growth_value, 2),
    "%"
)

latest_customer = customer_data[
    customer_data["Quarter"] == latest_quarter
]

print("\n===== CUSTOMER EXPERIENCE =====")

customer_summary = latest_customer[
    [
        "Region",
        "NPS",
        "CSAT_pct",
        "Avg_Delivery_Days",
        "Support_Tickets_K"
    ]
]

print(customer_summary)


highest_nps_row = latest_customer.loc[
    latest_customer["NPS"].idxmax()
]

lowest_nps_row = latest_customer.loc[
    latest_customer["NPS"].idxmin()
]


print("\nHighest NPS Region:")
print(
    highest_nps_row["Region"],
    highest_nps_row["NPS"]
)


print("\nLowest NPS Region:")
print(
    lowest_nps_row["Region"],
    lowest_nps_row["NPS"]
)

average_nps = latest_customer["NPS"].mean()

print(
    "\nAverage Regional NPS:",
    round(average_nps, 2)
)


latest_risk = risk_data[
    risk_data["Quarter"] == latest_quarter
]

print("\n===== OPERATIONAL RISK =====")

risk_summary = latest_risk[
    [
        "Region",
        "Stockout_Rate_pct",
        "Return_Processing_Days",
        "Warehouse_Capacity_Util_pct",
        "Fraud_Incidents"
    ]
]

print(risk_summary)


highest_stockout_row = latest_risk.loc[
    latest_risk["Stockout_Rate_pct"].idxmax()
]

print("\nHighest Stockout Region:")

print(
    highest_stockout_row["Region"],
    highest_stockout_row["Stockout_Rate_pct"],
    "%"
)


highest_capacity_row = latest_risk.loc[
    latest_risk[
        "Warehouse_Capacity_Util_pct"
    ].idxmax()
]

print("\nHighest Warehouse Capacity Utilization:")

print(
    highest_capacity_row["Region"],
    highest_capacity_row[
        "Warehouse_Capacity_Util_pct"
    ],
    "%"
)

highest_fraud_row = latest_risk.loc[
    latest_risk["Fraud_Incidents"].idxmax()
]

print("\nHighest Fraud Incidents:")

print(
    highest_fraud_row["Region"],
    highest_fraud_row["Fraud_Incidents"]
)


print("\n")
print("=" * 50)
print("NOVARETAIL AUTOMATED BUSINESS SUMMARY")
print("=" * 50)

print("Review Quarter:", latest_quarter)

print(
    "Total Revenue:",
    latest_total_revenue,
    "USD M"
)

print(
    "QoQ Revenue Growth:",
    round(qoq_revenue_growth, 2),
    "%"
)

print(
    "Best Growth Region:",
    best_growth_region
)

print(
    "Weakest Growth Region:",
    weakest_growth_region
)

print(
    "Highest NPS Region:",
    highest_nps_row["Region"]
)

print(
    "Lowest NPS Region:",
    lowest_nps_row["Region"]
)

print(
    "Highest Stockout Region:",
    highest_stockout_row["Region"]
)

print(
    "Highest Capacity Utilization:",
    highest_capacity_row["Region"]
)

print(
    "Highest Fraud Incidents:",
    highest_fraud_row["Region"]
)


analysis_results = {
    "review_quarter": latest_quarter,

    "overall_performance": {
        "total_revenue_usd_m": float(latest_total_revenue),
        "previous_revenue_usd_m": float(previous_total_revenue),
        "qoq_revenue_growth_pct": round(float(qoq_revenue_growth), 2)
    },

    "regional_performance": {
        "best_growth_region": str(best_growth_region),
        "best_growth_pct": round(float(best_growth_value), 2),

        "weakest_growth_region": str(weakest_growth_region),
        "weakest_growth_pct": round(float(weakest_growth_value), 2)
    },

    "customer_experience": {
        "average_nps": round(float(average_nps), 2),

        "highest_nps_region": str(
            highest_nps_row["Region"]
        ),

        "highest_nps": int(
            highest_nps_row["NPS"]
        ),

        "lowest_nps_region": str(
            lowest_nps_row["Region"]
        ),

        "lowest_nps": int(
            lowest_nps_row["NPS"]
        )
    },

    "operational_risk": {
        "highest_stockout_region": str(
            highest_stockout_row["Region"]
        ),

        "highest_stockout_pct": float(
            highest_stockout_row["Stockout_Rate_pct"]
        ),

        "highest_capacity_region": str(
            highest_capacity_row["Region"]
        ),

        "highest_capacity_pct": float(
            highest_capacity_row[
                "Warehouse_Capacity_Util_pct"
            ]
        ),

        "highest_fraud_region": str(
            highest_fraud_row["Region"]
        ),

        "highest_fraud_incidents": int(
            highest_fraud_row["Fraud_Incidents"]
        )
    }
}

print("\n")
print("=" * 50)
print("STRUCTURED ANALYSIS RESULTS")
print("=" * 50)

print(
    json.dumps(
        analysis_results,
        indent=4
    )
)

output_path = "output/analysis_results.json"

with open(
    output_path,
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        analysis_results,
        json_file,
        indent=4
    )

print(
    "\nAnalysis JSON saved successfully:"
)

print(output_path)

