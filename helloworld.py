print("Hello World! Welcome to Python Examples.")
import csv
# with open('deblanker_test.csv','r+') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#             line_count += 1
#     print(f'Processed {line_count} lines.')

# 10_05_2023: remember that it doesn't know whether an entry in a csv is an integer or a string, so it treats them all as strings
    
with open('deblanker_test.csv','r', encoding='utf-8-sig') as csvinput:
    with open('deblanker_output.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

# this section adds the 'Passes threshold' column header
        all = []
        first_row = next(reader)
        first_row.append('Passes threshold')
        all.append(first_row)
        sequence_column_index=first_row.index("Sequence")
        run_order_column_index=first_row.index("Run order")
        current_run_order=2
        max_run_order=0
# this section gets the maximum run order number in the csv
        run_orders=[]
        for row in reader:
            print(row)
            run_orders.append(int(row[run_order_column_index]))
        max_run_order=max(run_orders)


        while current_run_order<=max_run_order:
            current_blank_run_order=current_run_order-1
            blank_sequence_counts={}
            for row in reader:
                if int(row[run_order_column_index])==current_blank_run_order:
                    blank_sequence_counts[row[sequence_column_index]] = blank_sequence_counts.get(row[sequence_column_index], 0) + 1
            print(blank_sequence_counts)
            current_run_order+=2

        for row in reader:
            row.append(row[0])
            all.append(row)

        writer.writerows(all)
