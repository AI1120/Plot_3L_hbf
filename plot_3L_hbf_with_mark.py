import os
import pandas as pd
import numpy as np
from PIL import Image
import img2pdf
import ecgplotlibOLD as epl

def read_file(filePath):
    df_tmp_data = pd.read_csv(filePath, sep="\s+", header=None, index_col=None)
    if len(df_tmp_data.columns) == 4:
        df_tmp_data = df_tmp_data[[df_tmp_data.columns[1], df_tmp_data.columns[2], df_tmp_data.columns[3]]]
    elif len(df_tmp_data.columns) == 13:
        df_tmp_data = df_tmp_data[[df_tmp_data.columns[1], df_tmp_data.columns[6], df_tmp_data.columns[9]]]
    return df_tmp_data


def save_image_as_pdf(image_path, pdf_path):
    image = Image.open(image_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, 'wb')
    file.write(pdf_bytes)
    image.close()
    file.close()

# Directory containing the .txt and .hbf files
folder_path = '208_files' # Replace with your 3L dataset path
output_path = f'{folder_path}_pdf' # Replace with your output path

if not os.path.exists(output_path):
    os.makedirs(output_path)

col_names = ['A', 'B', 'C']

# List all files in the folder
files = os.listdir(folder_path)

# Filter for .txt and .hbf files
file_extensions = ['.txt', '.hbf']

flag = 0
for file in files:
    if any(file.endswith(ext) for ext in file_extensions):
        file_path = os.path.join(folder_path, file)
        df = read_file(file_path)
        df = np.array(df)
        df = df.T / 34.9525 / 120 # Change the scale factor here
        
        save_filename = file.split('.')[0] + '.pdf'
        output_file = os.path.join(output_path, save_filename)
        epl.plot(df, sample_rate=500, title=file, lead_index=col_names, filename=output_file)
        flag += 1
        print(f"[{flag}/{len(files)}]: Saved {output_file}")
        


