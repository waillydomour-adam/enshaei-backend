import PyPDF2

input_file = 'Prompt Engineering هندسة الموجهات.pdf'
parts = 3

with open(input_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    total_pages = len(reader.pages)
    pages_per_part = total_pages // parts

    for i in range(parts):
        writer = PyPDF2.PdfWriter()
        start = i * pages_per_part
        end = total_pages if i == parts - 1 else (i + 1) * pages_per_part
        
        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])
        
        output_name = f"Prompt_Part_{i+1}.pdf"
        with open(output_name, 'wb') as out:
            writer.write(out)
        print(f"Done: {output_name}")