import os
import json

icon_folder = "icons"

icon_mapping = {
    "slide_1_executive_summary": "globe_region.png",
    "slide_2_regional_performance": "growth_chart.png",
    "slide_3_customer_experience": "customer_star.png",
    "slide_4_operational_risk": "risk_alert.png",
    "slide_5_recommended_actions": "lightbulb_action.png"
}


print("===== ICON VALIDATION =====")

all_icons_valid = True

for slide_name, icon_name in icon_mapping.items():

    icon_path = os.path.join(
        icon_folder,
        icon_name
    )

    if os.path.exists(icon_path):

        print(
            "OK:",
            slide_name,
            "->",
            icon_name
        )

    else:

        print(
            "MISSING:",
            slide_name,
            "->",
            icon_name
        )

        all_icons_valid = False


if all_icons_valid:
    print("\nAll required icons found successfully.")       
else:
    print("\nOne or more required icons are missing.")


output_path = "output/icon_mapping.json"

with open(
    output_path,
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        icon_mapping,
        json_file,
        indent=4
    )


print(
    "\nIcon mapping saved successfully:"
)

print(output_path)


