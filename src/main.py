import datetime
import os
import sys
import shutil
from pathlib import Path
from Gen_Content.generate_page import generate_page

def copy_static_to_docs():
    """
    Copies all contents from static directory to docs directory.
    Deletes existing contents of docs directory first.
    Logs all operations to log.txt in the workspace root.
    """
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path = os.path.join(workspace_root, "static")
    docs_path = os.path.join(workspace_root, "docs")
    log_path = os.path.join(workspace_root, "log.txt")
    
    with open(log_path, "w") as log_file:
        log_file.write(f"Build Operation - {datetime.datetime.now()}\n")
        log_file.write("=" * 50 + "\n\n")
    
    def log_message(message):
        with open(log_path, "a") as log_file:
            log_file.write(f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}\n")
        print(message)
    
    try:
        if not os.path.exists(static_path):
            log_message(f"ERROR: Static directory does not exist at {static_path}")
            return False
        
        log_message(f"Starting build from {static_path} to {docs_path}")
        
        # Delete and recreate docs directory
        if os.path.exists(docs_path):
            log_message("Deleting existing docs directory...")
            shutil.rmtree(docs_path)
        
        os.makedirs(docs_path)
        log_message("Created fresh docs directory")
        
        # Copy static files
        def copy_recursive(src_dir, dest_dir, relative_path=""):
            for item in os.listdir(src_dir):
                src_item = os.path.join(src_dir, item)
                dest_item = os.path.join(dest_dir, item)
                relative_item = os.path.join(relative_path, item) if relative_path else item
                
                if os.path.isdir(src_item):
                    os.makedirs(dest_item, exist_ok=True)
                    log_message(f"Created directory: {relative_item}")
                    copy_recursive(src_item, dest_item, relative_item)
                else:
                    shutil.copy2(src_item, dest_item)
                    file_size = os.path.getsize(src_item)
                    log_message(f"Copied file: {relative_item} ({file_size} bytes)")
        
        copy_recursive(static_path, docs_path)
        
        # Generate resume page
        content_path = os.path.join(workspace_root, "content", "resume.md")
        template_path = os.path.join(workspace_root, "template.html")
        output_path = os.path.join(docs_path, "index.html")
        
        if not os.path.exists(content_path):
            log_message(f"ERROR: Resume content not found at {content_path}")
            return False
        
        log_message("Generating resume page...")
        generate_page(content_path, template_path, output_path)
        log_message(f"Generated: index.html")
        
        log_message("Build completed successfully!")
        return True
        
    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        import traceback
        log_message(traceback.format_exc())
        return False

def copy_static_assets(static_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in static_dir.iterdir():
        dst = output_dir / item.name
        if item.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(item, dst)
        else:
            shutil.copy2(item, dst)

def main():
    """Main build function"""
    success = copy_static_to_docs()
    if success:
        print("\n✓ Resume site built successfully!")
        print("✓ Open docs/index.html to preview")
    else:
        print("\n✗ Build failed. Check log.txt for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "docs"
    static_dir = project_root / "static"

    copy_static_assets(static_dir, docs_dir)
