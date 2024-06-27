import streamlit as st
# import PyPDF2
import pypdf
import pytesseract
# from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
import io
import os

# Function to convert PDF to searchable PDF
def make_pdf_searchable(pdf_file):
	# images = convert_from_path(pdf_file)
	pdf_bytes = pdf_file.read()
	images = convert_from_bytes(pdf_bytes)
	# pdf_writer = PyPDF2.PdfFileWriter()
	pdf_writer = pypdf.PdfWriter()

	for image in images:
		page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
		# pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
		pdf = pypdf.PdfReader(io.BytesIO(page))
		# pdf_writer.addPage(pdf.getPage(0))
		# pdf_writer.add_page(pdf.getPage(0))
		# pdf_writer.add_page(pdf.pages(0))
		pdf_writer.add_page(pdf.pages[0])

	searchable_pdf = io.BytesIO()
	pdf_writer.write(searchable_pdf)
	searchable_pdf.seek(0)

	return searchable_pdf

# Streamlit app
st.title("Make PDFs Searchable")
st.text("Upload your pdfs and download the searchable versions after the processing is done. The processing will take a while though, so best to keep this page open to the side, continue with your other work and download the files once they're done.")

uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

if uploaded_files:
	searchable_pdfs = []
	with st.spinner('Processing...'):
		for uploaded_file in uploaded_files:
			searchable_pdf = make_pdf_searchable(uploaded_file)
			searchable_pdfs.append((uploaded_file.name, searchable_pdf))
	
	st.success('Done!')

	for file_name, searchable_pdf in searchable_pdfs:
		# Add ' SEARCHABLE' suffix before the file extension
		name, ext = os.path.splitext(file_name)
		searchable_file_name = f"{name} SEARCHABLE{ext}"
		
		st.download_button(
			label=f"Download {searchable_file_name}",
			data=searchable_pdf,
			file_name=searchable_file_name,
			mime="application/pdf"
		)
