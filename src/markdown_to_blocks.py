def markdown_to_blocks(markdown_text):
    """
    converts markdown to a list of blocks
    like headers, paragraphs, etc. 
    """
    blocks = []
    current_paragraph = []

    lines = markdown_text.split('\n')
    for line in lines:
        line = line.rstrip()

        if line == "":
            if current_paragraph:
                block = "\n".join(current_paragraph).strip()
                blocks.append(block)
                current_paragraph = []
        else:
            current_paragraph.append(line.strip())
    
    # Handle the final block if it doesn't end with a blank line
    if current_paragraph:
        block = "\n".join(current_paragraph).strip()
        blocks.append(block)
    
    return blocks