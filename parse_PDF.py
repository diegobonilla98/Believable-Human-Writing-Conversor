import PyPDF2

pdf = open('C:\\Users\\diego\\Desktop\\UV\\año III\\SEM\\AC7.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)

for page in range(pdf_reader.numPages):
    pageObj = pdf_reader.getPage(page)
    text = pageObj.extractText()
    print(text)

