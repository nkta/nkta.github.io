import re
import sys

def create_toc(md_file_path):
    try:
        with open(md_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        toc = []
        for line in lines:
            if line.startswith('#'):
                level = line.count('#')
                title = line.strip('#').strip()
                anchor = re.sub('[^0-9a-zA-ZÀ-ÿ]+', '-', title).lower()
                toc.append('  ' * (level - 1) + f'- [{title}](#{anchor})')

        toc_str = '\n'.join(toc)
        return toc_str
    except Exception as e:
        return str(e)

# L'argument du fichier Markdown est passé en ligne de commande
if len(sys.argv) > 1:
    md_file = sys.argv[1]
    toc = create_toc(md_file)
    print(toc)
else:
    print("Veuillez fournir un chemin de fichier en argument.")

