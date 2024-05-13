import csv

def exchangeReport(rejectedList):
    fields = ["Order Id", "Rejection Reason"]

    rows = rejectedList
 
    filename = "output_exchange_report.csv"
 
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
    
        csvwriter.writerow(fields)
    
        csvwriter.writerows(rows)