from PyPDF2 import PdfMerger

def combine_pdfs(input_paths, output_path):
    """
    Combine multiple PDF files into a single PDF
    
    Args:
        input_paths (list): List of paths to PDF files to combine
        output_path (str): Path where the combined PDF will be saved
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        merger = PdfMerger()
        for path in input_paths:
            merger.append(path)
        merger.write(output_path)
        merger.close()
        return True
    except Exception as e:
        print(f"Error combining PDFs: {e}")
        raise