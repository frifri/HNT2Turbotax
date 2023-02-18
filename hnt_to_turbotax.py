import csv

# Map of old column names to new column names
column_map = {
    "date": "Date",
    "type": "Type",
    "transaction_hash": "Transaction Hash",
    "hnt_amount": "Received Amount",
    "usd_amount": "Market Value",
}

# Open the input file for reading
with open('helium_raw.csv', 'r') as input_file:

    # Create a reader object for the input file
    reader = csv.DictReader(input_file)

    # Open the output file for writing
    with open('hnt_turbotax.csv', 'w', newline='') as output_file:
        headers = list(column_map.values())
        headers.append("Market Value Currency")
        headers.append("Received Asset")

        # Create a writer object for the output file
        writer = csv.DictWriter(output_file, fieldnames=headers)

        # Write the header row in the output file
        writer.writeheader()

        # Loop through each row in the input file
        for row in reader:
            # Select only the columns we're interested in and rename them
            selected_row = {column_map[key]: row[key] for key in column_map.keys()}

            if row['type'] == "subnetwork_rewards_v1":
                continue

            if row['hnt_amount'] == "0":
                continue

            if row['type'] == "rewards_v1":
                selected_row['Type'] = "Mining"
                selected_row["Received Asset"] = "HNT"

            if row['type'] == "payment_v2":
                selected_row['Type'] = "Sale"

            selected_row["Received Amount"] = "{:.8f}".format(float(selected_row["Received Amount"]))
            selected_row["Market Value Currency"] = "USD"

            # Write the selected row to the output file
            writer.writerow(selected_row)
