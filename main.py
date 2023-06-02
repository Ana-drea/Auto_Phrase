import argparse

from ProjectClass import Project
from tools import update_token,get_baseurl

print("base url: "+get_baseurl())
update_token()

parser = argparse.ArgumentParser()
parser.add_argument('--format', type=str, default="MXLF")
parser.add_argument('--target', type=str, default="C:\\")
parser.add_argument('--id', type=str, required=True, default=None)
args = parser.parse_args()
file_format = args.format
target_folder = args.target
project_id=args.id

p = Project(project_id)
if file_format not in ("MXLF","DOCX","TMX","XLIFF"):
    file_format = "MXLF"
# p.get_bilingual_files(file_format)[0].response.text
p.get_bilingual_files(file_format,target_folder)



# download_bilingual_file("Y0K7MFt1qdz9eAPQHfZbB1")

