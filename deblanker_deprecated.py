print("Welcome to the deblanker")
import csv
import math
# this makes a funtion to do the seek and skip title
def reset_csv(csv_file):
    # the seek returns the csv reader to the begining of the file    
    csv_file.seek(0)
    # this skips the title row
    next(csv_file, None)
   
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
        all_peptides=[]
        for row in reader:
            run_orders.append(int(row[run_order_column_index]))
            all_peptides.append(row[sequence_column_index])
        max_run_order=max(run_orders)

        csvinput.seek(0)
        next(csvinput, None)

        # creating blank dictionary structure
        unique_peptides = list(set(all_peptides))

        master_peptide_values={
            peptide:{
                'mean':0,
                'run_counts':{},
                'standard_deviation':0
                } 
                for peptide in unique_peptides}
        # fill in in run count
        for row in reader:
            master_peptide_values[row[sequence_column_index]]['run_counts'][row[run_order_column_index]]=master_peptide_values[row[sequence_column_index]]['run_counts'].get(row[run_order_column_index], 0) + 1
        csvinput.seek(0)
        next(csvinput, None)
        # working out averages
        for peptide in unique_peptides:
            run_counts_arr=list(master_peptide_values[peptide]['run_counts'].values())
            master_peptide_values[peptide]['mean']=sum(run_counts_arr)/max_run_order
            mean=master_peptide_values[peptide]['mean']
            # working out standard deviation
            sum_of_run_counts_minus_mean_squared=0
            for count in run_counts_arr:
                sum_of_run_counts_minus_mean_squared+=(count-mean)**2
            number_of_zero_value_peptide_counts=max_run_order-len(run_counts_arr)
            sum_of_run_counts_minus_mean_squared+= mean**2*number_of_zero_value_peptide_counts
            master_peptide_values[peptide]['standard_deviation']=math.sqrt(sum_of_run_counts_minus_mean_squared/max_run_order)
        for row in reader:
            # this leaves wash rows without a true or false value
            if int(row[run_order_column_index])%2 != 0:
                all.append(row)
            else:
                current_blank_peptide_count=master_peptide_values[row[sequence_column_index]]['run_counts'].get(str(int(row[run_order_column_index])-1),0)
                current_rows_run_peptide_count=master_peptide_values[row[sequence_column_index]]['run_counts'].get(row[run_order_column_index],0)
                current_rows_peptide_stdev=master_peptide_values[row[sequence_column_index]]['standard_deviation']
                current_rows_peptide_mean=master_peptide_values[row[sequence_column_index]]['mean']
                current_rows_peptide_mean_plus_2xstdev=current_rows_peptide_mean+current_rows_peptide_stdev*2
                print(current_rows_peptide_mean_plus_2xstdev)
                # blank_count_plus_2x_stdev=current_blank_peptide_count+current_rows_peptide_stdev*2
                # the following line allows sample to pass if their value=0 in blank and >0 in sample
                zero_blank_allowed=  current_rows_run_peptide_count > 0 and current_blank_peptide_count == 0
                row.append(current_rows_run_peptide_count>current_rows_peptide_mean_plus_2xstdev or zero_blank_allowed)
                all.append(row)
        csvinput.seek(0)
        next(csvinput, None)
        writer.writerows(all)
print("deblanking completed, thanks for banking with deblanking")
