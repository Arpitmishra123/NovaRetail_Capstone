import pandas as pd

file_path = "assets/novaretail_dataset.xlsx"

excel_file = pd.ExcelFile(file_path)

print("Excel Sheet Names:")
print(excel_file.sheet_names)

# Read all three sheets

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


print("\n--- REGIONAL PERFORMANCE ---")
print(regional_data)


print("\n--- CUSTOMER EXPERIENCE ---")
print(customer_data)


print("\n--- OPERATIONAL RISK ---")
print(risk_data)

print("\n===== DATASET SUMMARY =====")

print("\nRegional Performance:")
print("Rows and Columns:", regional_data.shape)
print("Columns:", regional_data.columns.tolist())

print("\nCustomer Experience:")
print("Rows and Columns:", customer_data.shape)
print("Columns:", customer_data.columns.tolist())

print("\nOperational Risk:")
print("Rows and Columns:", risk_data.shape)
print("Columns:", risk_data.columns.tolist())