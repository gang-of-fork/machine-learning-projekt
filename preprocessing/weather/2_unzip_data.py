#Script to unzip weatherdata that was downloaded from DWD Website

import os
import zipfile

def unzipWeatherdata(input_dir):
    base_path = os.path.join(os.path.dirname(__file__), "datasets", "wetter", input_dir)
    output_path = os.path.join(os.path.dirname(__file__), "datasets", "wetter_entpackt", input_dir)

    listed_dir = os.listdir(base_path)

    for i, zip_file in enumerate(listed_dir):
        if ".zip" in zip_file:
            print("Unzipping " + zip_file)

            try:
                with zipfile.ZipFile(os.path.join(base_path, zip_file),"r") as zip_ref:
                    zip_ref.extractall(os.path.join(output_path, zip_file.replace(".zip", "")))
            except:
                print("Error: " + zip_file)

            print("Unzipped " + str(i) + " of " + str(len(listed_dir)))

    print("---- finished ----")

if __name__ == "__main__":
    unzipWeatherdata("temperatur")
    unzipWeatherdata("niederschlag")