import os,click,uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

@click.command()
@click.option("--dir", default = '/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/ivcurves/')
def main(dir):
    print(f'The selected directory to look for data folders is: {dir}')
    list_folders = os.listdir(f'{dir}')
    for folder in list_folders:
        if not os.path.isdir(f'{dir}{folder}') or "TMP" in folder:
            print('\033[91m'+'Not considering '+folder+'\033[0m') 
            continue
        else:
            print('\033[92m'+ 'Generating quality_checks.pdf in '+folder+ '\033[0m')
            pdf_pages = PdfPages(f'{dir}/{folder}/quality_checks.pdf')
            list_subfolders = [f for f in os.listdir(f'{dir}{folder}') if os.path.isdir(f'{dir}{folder}/{f}')]
            for subfolder in list_subfolders:
                root_files = [f for f in os.listdir(f'{dir}{folder}/{subfolder}') if f.endswith('.root')]
                ip = subfolder.split("_")[-1].split(".")[-1]
                for r,root_file in enumerate(root_files):
                    file = uproot.open(f'{dir}{folder}/{subfolder}/{root_file}')
                    bias_v = file['tree/bias/bias_v']
                    bias_dac = file['tree/bias/bias_dac']
                    trim = file['tree/iv_trim/trim']
                    current = file['tree/iv_trim/current']

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 6))

                    ax1.scatter(bias_dac.array(),bias_v.array())
                    ax1.set_title(f'ip_{ip}_{root_file.replace(".root","")}')
                    ax1.set_xlabel('Bias DAC')
                    ax1.set_ylabel('Bias Voltage [V]')
                    ax1.grid(True)
                    # TODO: add diferent ylim for hpk and fbk types

                    ax2.scatter(trim.array(),current.array())
                    ax2.set_title(f'ip_{ip}_{root_file.replace(".root","")}')
                    ax2.set_xlabel('Trim')
                    ax2.set_ylabel('Current [A]')
                    ax2.set_ylim((-10,230))
                    ax2.grid(True)

                    plt.tight_layout()
                    pdf_pages.savefig(fig)

                    plt.close(fig)

        pdf_pages.close()

if __name__ == "__main__":
    main()