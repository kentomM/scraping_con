import csv

def create_file(path, header):
    with open(path, "w") as file:
        writer_file = csv.writer(file)
        writer_file.writerow(header)

def write_row(path, vendor):
    values = [
        vendor["license_number"],
        vendor["license_validity_period"],
        vendor["corporate_individual_classification"],
        vendor["business_name"],
        vendor["business_name_kana"],
        vendor["representative_name"],
        vendor["representative_name_kana"],
        vendor["postal"],
        vendor["prefecture"],
        vendor["city"],
        vendor["address"],
        vendor["phone_number"],
        vendor["capital_amount"],
        vendor["capital_amount_yen"],
        vendor["other_business_involvement"]
    ]
    
    construction_type = [vendor[f"construction_type_{i}"] for i in range(29)]
    
    values += construction_type
    
    with open(path, "a") as file:
        writer_file = csv.writer(file)
        writer_file.writerow(values)
