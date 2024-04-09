
import os,click
import pandas as pd

@click.command()
@click.option("--dir", default = '/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/')
def main(dir):
    print(f'The selected directory to look for data folders is: {dir}')
    list_folders = os.listdir(f'{dir}')
    df = pd.DataFrame(columns=['Filename', 'Slope', 'Intercept'])

    for folder in list_folders:
# read the log.txt file inside each folder and check if the beggining of each lines is AFE or not:
        if not os.path.isdir(f'{dir}{folder}') or "TMP" in folder:
            print('\033[91m'+'Not considering '+folder+'\033[0m') 
            continue
        else:
            print('\033[92m'+ 'Continue with '+folder+ '\033[0m')
            list_files = os.listdir(f'{dir}{folder}')
            if "log.txt" in list_files:
                file = open(f'{dir}{folder}/log.txt', 'r')
                lines = file.readlines()
                ips_chs = {}; ips_dirs = ""; channels = ""; filenames = []
                for line in lines:
                    if line.startswith(" 10."): 
                        filename = line.split(" ")[2]
                        filenames.append(filename)
                        # print(f'Filename: {filename}')
                        ips_dirs = line.split(" ")[1].split(".")[-1]
                        if ips_dirs not in ips_chs.keys():
                            ips_chs[ips_dirs] = [] 
                            # print(f'IPs: {ips_dirs}')
                        channels = filename.split(".")[0].split("_")[-1]
                        if channels not in ips_chs.values():
                            ips_chs[ips_dirs].append(channels) 
                        # afe = filename.split(".")[0].split("_")[3]
                        # if channels not in ips_chs.values():
                        #     ips_chs[ips_dirs].append(channels)    
                            # print(f'Channel: {channels}')
                        # print(f'IPS {ips_dirs}, CHS : {channels}')
                    # if line.startswith("AFE"):
                    #     afe = line.split(":")[1].strip()
                    #     print(f'Afe: {afe}')
                i = 0
                for line in lines:
                    # print(f'IPS {ips_dirs}, CHS : {channels}, {ips_chs}')
                    if line.startswith("CONVERSION FACTOR"):
                        # index = ips_chs[ips_dirs].index(channels)
                        # print(f'Index: {index}')

                        conversion_str = line.split(":")[1].strip()
                        conversion_str = conversion_str.replace("[", "").replace("]", "").replace(",", "").strip()
                        conversion = [num_str for num_str in conversion_str.split()]
                        
                        filename = filenames[i].split(":")[-1].split(".")[0]
                        apa = filename.split("_")[1]
                        afe = filename.split("_")[3]
                        chs = filename.split("_")[5]
                        slope = conversion[-2]
                        intercept = conversion[-1]

                        print(f'\nFolder: {folder}')
                        print(f'Filename: {filename}')
                        print(f'APA: {apa}')
                        print(f'AFE: {afe}')
                        print(f'CHS: {chs}')
                        print(f'Slope: {slope}')
                        print(f'Intercept: {intercept}')

                        df = pd.concat((df,pd.DataFrame({'Folder': [folder],'Filename': [filename],
                                                         'APA':[apa], 'AFE':[afe], 'CHS':[chs], 
                                                         'Slope':[slope], 'Intercept':[intercept]})), ignore_index=True)
                        # print(df)
                        df.to_csv('linear_fit_values.txt', sep='\t', index=False)
                        i += 1

if __name__ == "__main__":
    main()