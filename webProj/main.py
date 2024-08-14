from flask import Flask, render_template, abort
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
import logging
import os

app = Flask(__name__)

# Base directory for the content files
CONTENT_DIR = os.path.abspath('content')
OBSIDIAN_DIR = os.path.abspath('/home/kadien/Documents/obsidian/Learning')

# Logger junk
logging.basicConfig(level=logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
app.logger.addHandler(console_handler)

file_handler_verbose = logging.FileHandler('main_verbose.log')
file_handler_verbose.setLevel(logging.INFO)

file_handler_error = logging.FileHandler('main_error.log')
file_handler_error.setLevel(logging.ERROR)

app.logger.addHandler(file_handler_verbose)
app.logger.addHandler(file_handler_error)

werkLog = logging.getLogger('werkzeug')
werkLog.setLevel(logging.INFO)
werkLog.addHandler(file_handler_verbose)
werkLog.addHandler(file_handler_error)

def safe_join(directory, path):
    """
    Safely join `directory` and `path` to prevent directory traversal.
    """
    # Clean the path to remove any potential directory traversal characters
    path = os.path.normpath(path)

    # Ensure the path is within the directory
    full_path = os.path.abspath(os.path.join(directory, path))
    if os.path.commonpath([full_path, directory]) == directory:
        return full_path
    else:
        abort(403)  # Forbidden


def generate_navigation():
    """
    Generate a nested dictionary representing the directory structure of the CONTENT_DIR.
    """
    nav_items = {}

    for root, dirs, files in os.walk(CONTENT_DIR):
        # Create a relative path for the root directory
        rel_dir = os.path.relpath(root, CONTENT_DIR)

        # Get the reference to the current directory in the navigation structure
        current_dir = nav_items
        if rel_dir != '.':
            for part in rel_dir.split(os.sep):
                current_dir = current_dir.setdefault(part, {})

        # Add files to the current directory's dictionary
        for file in files:
            if file.endswith('.md'):
                # Create a URL-friendly name without the .md extension
                file_name = file.replace('.md', '')
                # Store the full relative path as the value, not just the file name
                current_dir[file_name] = os.path.join(rel_dir, file_name).replace("\\", "/")

        # Add exampleDir to navigation if it exists
        if os.path.exists(OBSIDIAN_DIR):
            for root, dirs, files in os.walk(OBSIDIAN_DIR):
                rel_dir = os.path.relpath(root, OBSIDIAN_DIR)
                current_dir = nav_items
                if rel_dir != '.':
                    for part in rel_dir.split(os.sep):
                        current_dir = current_dir.setdefault(part, {})

                for file in files:
                    if file.endswith('.md'):
                        file_name = file.replace('.md', '')
                        current_dir[file_name] = os.path.join('obsidian', rel_dir, file_name).replace("\\", "/")

    return nav_items



@app.route('/', defaults={'filename': 'home'})
@app.route('/<path:filename>')
def serve_content(filename):

    if filename.startswith('obsidian/'):
        base_dir = OBSIDIAN_DIR
        relative_filename = filename[len('obsidian/'):]
    else:
        base_dir = CONTENT_DIR
        relative_filename = filename

    # Construct the full filepath
    filepath = safe_join(base_dir, f"{relative_filename}.md")

    if os.path.exists(filepath):

        with open(filepath, 'r') as file:
            raw_content = file.read()

        # content = markdown.markdown(
        #     raw_content,
        #     extensions=['extra', 'fenced_code', 'codehilite', 'sane_lists']
        # )

        # Use markdown-it-py with tasklists and strikethrough plugins
        md = MarkdownIt().use(tasklists_plugin)
        md.enable("strikethrough")
        content = md.render(raw_content)

        # Generate navigation items
        nav_items = generate_navigation()
        # Render the content.html template with navigation and file content
        return render_template('content.html', nav_items=nav_items, content=content, img_count=len(os.listdir('static/imgs')))
    else:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
