from __future__ import print_function
from openpyxl.workbook import Workbook
import pandas as pd
#from convergence1 import Convergence1
import interface
import argparse


def main(out_path, analytical=None):
    #create empty data frame to add analysis parameters (GCI, p, asymp. Range,...) later
    df = pd.DataFrame({'fine_grid_size':[],'middle_grid_size':[],'coarse_grid_size':[],'GCI_fine':[],'p':[],'asymp_ratio':[]})

    #returns a 2d-list (4x120) containing tuples of the format (grid size, value) of
    # all possible gridsize combinations and measurement points
    combList = interface.assemble_cominations()

    c_rows = len(combList)
    c_columns = len(combList[0])

    for i in range (c_rows) :


# springt führt nur 5 cyklen durch
# Warum wird im ersten Durchlauf Meshnummern 1,2,9 vewendent ansatt 1,2,3
        for j in range (c_columns) :
            print("Beginn Round", (i+1)*j)

            grids = [(combList [i][j][0][0], combList[i][j][0][1]),
                     (combList[i][j][1][0], combList[i][j][1][1]),
                     (combList[i][j][2][0], combList[i][j][2][1])]

            print(grids)

            convergence = interface.Convergence1()
            convergence.add_grids(grids)

            print(convergence)  # doctest:+ELLIPSIS

            fine_grid_size = grids[0][0]
            middle_grid_size = grids[1][0]
            coarse_grid_size = grids[2][0]


            gci_fine_fine = convergence[0].fine.gci_fine
            p = convergence[0].fine.p
            asymp_ratio = convergence[0].asymptotic_ratio


            to_append = [fine_grid_size, middle_grid_size, coarse_grid_size, gci_fine_fine, p, asymp_ratio]
            df_length = len(df)
            df.loc[df_length] = to_append

            # Write the report
            with open(out_path, 'w') as f:
                f.write(str(convergence))

            print("End Round", (i+1)*j)

    # datatoexel = pd.ExcelWriter(r"C:\Users\Jose Matthias\Desktop\Uni\Bachelorarbeit_Inhalt\Simulations\convergence_analysis_results.xlsx")
    df.to_excel(r"C:\Users\Jose Matthias\Desktop\Uni\Bachelorarbeit_Inhalt\Simulations\convergence_analysis_results.xlsx")

def cl_interface():


    # Prepare command line parser
    desStr = "Perform grid convergence study on input file."

    parser = argparse.ArgumentParser(description=desStr)

    parser.add_argument("-o", "--out",
                        type=str,
                        help=("output file path"),
                        default='verify_report.txt')

    parser.add_argument("-a", "--analytical",
                        type=str,
                        help=("Expected analytical value"))

    args = parser.parse_args()

    out_path = args.out
    analytical = args.analytical

    main(out_path, analytical)

    return

cl_interface()