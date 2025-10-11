import os
import shutil
from datetime import datetime
from Gen_Content.generate_page import generate_pages_recursive

def copy_static_to_public():
    """
    Recursively copies all contents from static directory to public directory.
    Deletes existing contents of public directory first.
    Logs all operations to log.txt in the workspace root.
    """
    # Get the workspace root (parent of src directory)
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_path = os.path.join(workspace_root, "static")
    public_path = os.path.join(workspace_root, "public")
    log_path = os.path.join(workspace_root, "log.txt")
    
    # Initialize log file
    with open(log_path, "w") as log_file:
        log_file.write(f"Static to Public Copy Operation - {datetime.now()}\n")
        log_file.write("=" * 50 + "\n\n")
    
    def log_message(message):
        """Helper function to write messages to log file"""
        with open(log_path, "a") as log_file:
            log_file.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        print(message)  # Also print to console
    
    try:
        # Check if static directory exists
        if not os.path.exists(static_path):
            log_message(f"ERROR: Static directory does not exist at {static_path}")
            return False
        
        log_message(f"Starting copy operation from {static_path} to {public_path}")
        
        # Delete contents of public directory if it exists
        if os.path.exists(public_path):
            log_message("Deleting existing contents of public directory...")
            for item in os.listdir(public_path):
                item_path = os.path.join(public_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    log_message(f"Deleted directory: {item}")
                else:
                    os.remove(item_path)
                    log_message(f"Deleted file: {item}")
        else:
            # Create public directory if it doesn't exist
            os.makedirs(public_path)
            log_message("Created public directory")
        
        # Recursively copy static contents to public
        def copy_recursive(src_dir, dest_dir, relative_path=""):
            """Recursively copy directory contents"""
            for item in os.listdir(src_dir):
                src_item = os.path.join(src_dir, item)
                dest_item = os.path.join(dest_dir, item)
                relative_item = os.path.join(relative_path, item) if relative_path else item
                
                if os.path.isdir(src_item):
                    # Create directory in destination
                    os.makedirs(dest_item, exist_ok=True)
                    log_message(f"Created directory: {relative_item}")
                    
                    # Recursively copy directory contents
                    copy_recursive(src_item, dest_item, relative_item)
                else:
                    # Copy file
                    shutil.copy2(src_item, dest_item)
                    file_size = os.path.getsize(src_item)
                    log_message(f"Copied file: {relative_item} ({file_size} bytes)")
        
        # Start the recursive copy
        copy_recursive(static_path, public_path)

        # Generate pages recursively from content directory
        content_path = os.path.join(workspace_root, "content")
        template_path = os.path.join(workspace_root, "template.html")
        generate_pages_recursive(content_path, template_path, public_path)
        
        log_message("Page generation completed successfully!")
        log_message("Copy operation completed successfully!")
        return True
        
    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        return False

def main():
    """Main function to run the copy operation"""
    success = copy_static_to_public()
    if success:
        print("Static files copied to public directory successfully!")
    else:
        print("Error occurred during copy operation. Check log.txt for details.")

if __name__ == "__main__":
    main()
