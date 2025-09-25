import os
import re

def get_article_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        if first_line.startswith('#'):
            return first_line.lstrip('# ').strip()
    return os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ').replace('-', ' ').title()

def generate_article_list(category_path, base_url):
    articles_html = []
    if os.path.exists(category_path) and os.path.isdir(category_path):
        for filename in sorted(os.listdir(category_path)):
            if filename.endswith('.md'):
                file_path = os.path.join(category_path, filename)
                title = get_article_title(file_path)
                # Construct the relative path to the .md file from the root
                # e.g., "WSL/wsl_without_MS_Store.md"
                full_md_relative_path = os.path.join(base_url, filename)
                # Link to article-viewer.html with the md file as a query parameter
                link_href = f'templates/article-viewer.html?article={full_md_relative_path}'
                articles_html.append(f'                <li class="list-group-item"><a href="{link_href}">{title}</a></li>')
    return '\n'.join(articles_html)

def update_index_html(template_path, output_path, categories_config):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for placeholder, config in categories_config.items():
        category_folder = config['folder']
        base_url = config['base_url']
        
        # Handle 'Veille' category separately due to its complex structure
        if placeholder == '<!-- ARTICLES_VEILLE -->':
            veille_content = generate_veille_content(category_folder, base_url)
            content = content.replace(placeholder, veille_content)
        else:
            articles_list = generate_article_list(category_folder, base_url)
            content = content.replace(placeholder, f'            <ul class="list-group list-group-flush">\n{articles_list}\n            </ul>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_veille_content(veille_base_path, base_url):
    veille_html = []
    sub_categories = {
        'Java': 'veille-java',
        'DevOps': 'veille-devops',
        'IA': 'veille-ia',
        'Agile': 'veille-agile',
        'MCP': 'veille-mcp',
        'A2A': 'veille-a2a'
    }

    # Generate sub-tabs navigation
    veille_html.append('            <ul class="nav nav-tabs mt-3" id="veilleTab" role="tablist">')
    for i, (sub_cat_name, sub_cat_id) in enumerate(sub_categories.items()):
        active_class = " active" if i == 0 else ""
        selected = "true" if i == 0 else "false"
        veille_html.append(f'                <li class="nav-item">')
        veille_html.append(f'                    <a class="nav-link{active_class}" id="{sub_cat_id}-tab" data-toggle="tab" href="#{sub_cat_id}" role="tab" aria-controls="{sub_cat_id}" aria-selected="{selected}">{sub_cat_name}</a>')
        veille_html.append(f'                </li>')
    veille_html.append('            </ul>')

    # Generate sub-tab content
    veille_html.append('            <div class="tab-content mt-3" id="veilleTabContent">')
    for i, (sub_cat_name, sub_cat_id) in enumerate(sub_categories.items()):
        active_class = " show active" if i == 0 else ""
        veille_html.append(f'                <div class="tab-pane fade{active_class}" id="{sub_cat_id}" role="tabpanel" aria-labelledby="{sub_cat_id}-tab">')
        veille_html.append(f'                    <h5 class="mt-4">2025</h5>') # Assuming year 2025 for now
        veille_html.append(f'                    <div class="row">')
        
        sub_cat_folder = os.path.join(veille_base_path, sub_cat_name)
        if os.path.exists(sub_cat_folder) and os.path.isdir(sub_cat_folder):
            # Group files by month (e.g., 2025-03.png, 2025-03.pdf)
            files_by_month = {}
            for filename in os.listdir(sub_cat_folder):
                match = re.match(r'(\d{4}-\d{2})\.(png|pdf|md)', filename)
                if match:
                    month_key = match.group(1)
                    file_type = match.group(2)
                    if month_key not in files_by_month:
                        files_by_month[month_key] = {}
                    files_by_month[month_key][file_type] = filename
            
            for month_key in sorted(files_by_month.keys()):
                month_files = files_by_month[month_key]
                month_name = get_month_name(month_key.split('-')[1])
                
                img_src = os.path.join(base_url, sub_cat_name, month_files.get('png', ''))
                pdf_href = os.path.join(base_url, sub_cat_name, month_files.get('pdf', ''))
                
                veille_html.append(f'                        <div class="col-md-3 mb-4">')
                veille_html.append(f'                            <div class="card h-100">')
                if img_src:
                    veille_html.append(f'                                <img src="{img_src}" class="card-img-top" alt="{sub_cat_name} {month_name} {month_key.split("-")[0]}">')
                veille_html.append(f'                                <div class="card-body">')
                veille_html.append(f'                                    <h6 class="card-title">{month_name} {month_key.split("-")[0]}</h6>')
                if pdf_href:
                    veille_html.append(f'                                    <a href="{pdf_href}" class="btn btn-primary btn-sm">Voir la veille (PDF)</a>')
                if month_files.get('md'):
                    md_file_path = os.path.join(base_url, sub_cat_name, month_files.get('md'))
                    veille_html.append(f'                                    <a href="templates/article-viewer.html?article={md_file_path}" class="btn btn-secondary btn-sm ml-2">Lire l\'article</a>')
                veille_html.append(f'                                </div>')
                veille_html.append(f'                            </div>')
                veille_html.append(f'                        </div>')
        
        veille_html.append(f'                        <!-- Ajoute d\'autres mois ici -->')
        veille_html.append(f'                    </div>')
        veille_html.append(f'                </div>')
    veille_html.append('            </div>')
    return '\n'.join(veille_html)

def get_month_name(month_num):
    months = {
        '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
        '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
        '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
    }
    return months.get(month_num, month_num)


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    template_path = os.path.join(root_dir, 'templates', 'index.html.template')
    index_html_path = os.path.join(root_dir, 'index.html')

    categories_config = {
        '<!-- ARTICLES_WSL -->': {'folder': os.path.join(root_dir, 'WSL'), 'base_url': 'WSL'},
        '<!-- ARTICLES_DOCKER -->': {'folder': os.path.join(root_dir, 'Docker'), 'base_url': 'Docker'},
        '<!-- ARTICLES_JAVA -->': {'folder': os.path.join(root_dir, 'Java'), 'base_url': 'Java'},
        '<!-- ARTICLES_MAC -->': {'folder': os.path.join(root_dir, 'Mac'), 'base_url': 'Mac'},
        '<!-- ARTICLES_DEVOPS -->': {'folder': os.path.join(root_dir, 'DevOps'), 'base_url': 'DevOps'},
        '<!-- ARTICLES_GIT -->': {'folder': os.path.join(root_dir, 'Git'), 'base_url': 'Git'},
        '<!-- ARTICLES_SALESFORCE -->': {'folder': os.path.join(root_dir, 'Salesforce'), 'base_url': 'Salesforce'},
        '<!-- ARTICLES_PROMPT_ENGINEERING -->': {'folder': os.path.join(root_dir, 'PromptEngenering'), 'base_url': 'PromptEngenering'},
        '<!-- ARTICLES_VEILLE -->': {'folder': os.path.join(root_dir, 'Veille'), 'base_url': 'Veille'},
        '<!-- ARTICLES_MCP -->': {'folder': os.path.join(root_dir, 'MCP'), 'base_url': 'MCP'},
    }

    update_index_html(template_path, index_html_path, categories_config)
    print("index.html a été mis à jour avec les articles dynamiques.")
