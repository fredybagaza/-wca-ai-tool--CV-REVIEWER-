# importing the required modules
from pypdf import PdfReader, PdfWriter

def add_watermark(wmFile, pageObj):
    # creating pdf reader object of watermark pdf file
    reader = PdfReader(wmFile)

    # merging watermark pdf's first page with passed page object.
    pageObj.merge_page(reader.pages[0])

    # returning watermarked page object
    return pageObj

def main():
    # watermark pdf file name
    mywatermark = 'watermark.pdf'

    # original pdf file name
    origFileName = 'example.pdf'

    # new pdf file name
    newFileName = 'watermarked_example.pdf'

    # creating pdf File object of original pdf
    pdfFileObj = open(origFileName, 'rb')

    # creating a pdf Reader object
    reader = PdfReader(pdfFileObj)

    # creating a pdf writer object for new pdf
    writer = PdfWriter()

    # adding watermark to each page
    for page in range(len(reader.pages)):
        # creating watermarked page object
        wmpageObj = add_watermark(mywatermark, reader.pages[page])

        # adding watermarked page object to pdf writer
        writer.add_page(wmpageObj)

    # writing watermarked pages to new file
    with open(newFileName, 'wb') as newFile:
        writer.write(newFile)

    # closing the original pdf file object
    pdfFileObj.close()

if __name__ == "__main__":
    # calling the main function
    main()