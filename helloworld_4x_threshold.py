print("Welcome to the deblanker, prepare to be deblanked")
import csv

# this makes a funtion to do the seek and skip title
def reset_csv(csv_file):
    # the seek returns the csv reader to the begining of the file    
    csv_file.seek(0)
    # this skips the title row
    next(csv_file, None)
   
with open('deblanker_test.csv','r', encoding='utf-8-sig') as csvinput:
    with open('deblanker_output_4x.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        # calculate threshhold
        threshold=0.25

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
        all_peptides=[]
        for row in reader:
            run_orders.append(int(row[run_order_column_index]))
            all_peptides.append(row[sequence_column_index])
        max_run_order=max(run_orders)

        csvinput.seek(0)
        next(csvinput, None)

        # this loops over the samples and firstly looks at the pre-wash and counts the instances of peptides into a dictionary
        while current_run_order<=max_run_order:

            current_blank_run_order=current_run_order-1
            blank_sequence_counts={}
            for row in reader:
                if int(row[run_order_column_index])==current_blank_run_order:
                    blank_sequence_counts[row[sequence_column_index]] = blank_sequence_counts.get(row[sequence_column_index], 0) + 1
            csvinput.seek(0)
            next(csvinput, None)

            sample_sequence_counts={}
            for row in reader:
                if int(row[run_order_column_index])==current_run_order:
                    sample_sequence_counts[row[sequence_column_index]] = sample_sequence_counts.get(row[sequence_column_index], 0) + 1
            csvinput.seek(0)
            next(csvinput, None)

            for row in reader:
                # LOGIC HERE
                if int(row[run_order_column_index])==current_blank_run_order:
                    all.append(row)


                if int(row[run_order_column_index])==current_run_order:
                    row.append(sample_sequence_counts.get(row[sequence_column_index],0)*threshold>=blank_sequence_counts.get(row[sequence_column_index],0))
                    all.append(row)
            
            csvinput.seek(0)
            next(csvinput, None)
            current_run_order+=2

        writer.writerows(all)
