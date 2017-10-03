from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import csv
import time

# convert to html
def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def getresult(theinfo):
    if theinfo:
        theinfo = theinfo.group(0)
    else:
        theinfo = ''
    return theinfo

#code to extract table and write to csv
def createDirectory(instring, outpath, split_program_pattern):
    i = 1
    with open(outpath, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',' , quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write the header row
        filewriter.writerow(['Name', 'Address','Date First/ Last Seen', 'SSN', 'DOB', 'Phone'])

        # cycle through the programs
        for programinfo in re.finditer(split_program_pattern, instring,  re.DOTALL):
            print i
            i=i+1

            # pull out the pieces
            Name = getresult(re.search('Name.*?<br></span></div>', programinfo.group(0)))

            print (re.search('Name.*?<br></span></div>', programinfo.group(0)))
           # Name = re.escape(Name) #odd characters in the name

            # pending format for 'address'

           #  address  =getresult(re.search('Address\n<br></span></div><div style="position:absolute; border: textbox 1px solid;'
           #                                ' writing-mode:lr-tb;' \
           #           ' left:225px; top:1075px; width:71px; height:15px;">' \
           #           '<span style="font-family: Helvetica; font-size:8px">(.*?)<br></span></div>', programinfo.group(0)))
           #  #if address: address = re.escape(address)
           #
           #  #Date seen
           #  DateFirstLastSeen = getresult(re.search('<span style="font-family: Helvetica-Bold;'
           #                                          ' font-size:8px">Date First/Last Seen </span>(.*?)<br></span></div>' , programinfo.group(0)))
           #
           #  #if DateFirstLastSeen: DateFirstLastSeen = re.DateFirstLastSeen(DateFirstLastSeen)
           #  # SSN
           #
           #  SSN = getresult(re.search('<span style="font-family: Helvetica-Bold;'
           #                            ' font-size:8px">SSN\n<br></span></div>'
           #                            '<div style="position:absolute; border: textbox 1px solid; '
           #                            'writing-mode:lr-tb; left:85px; top:1118px; width:46px; height:8px;">'
           #                            '<span style="font-family: Helvetica; font-size:8px">(.*?)<br></span></div>',
           #                                          programinfo.group(0)))
           #  #if SSN: SSN = re.SSN(SSN)
           #
           #  # DOB
           #  DOB = getresult(re.search('Date of Birth\n<br></span></div>'
           #                            '<div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:336px; '
           #                            'top:1118px; width:21px; height:8px;"><span style="font-family: Helvetica-Bold; '
           #                            'font-size:8px">(.*?)<br></span>',
           #                            programinfo.group(0)))
           #
           #  #if DOB: DOB = re.DOB(DOB)
           #  #Phone
           #  Phone =  getresult(re.search('Phone\n<br></span></div><div style="position:absolute; border: textbox 1px solid;'
           #                               ' writing-mode:lr-tb; left:24px; top:1222px; width:49px; height:8px;">'
           #                               '<span style="font-family: Helvetica-Bold; font-size:8px"(.*?)<br></span>',
           #                            programinfo.group(0)))
           #
           #  #if Phone: Phone = re.escape(Phone)
           #  #Record Source
           #  RecordSource = getresult(
           #      re.search('Record Source\n<br></span></div><div style="position:absolute; border: textbox 1px solid;'
           #                ' writing-mode:lr-tb; left:85px; top:4669px; width:30px; height:8px;">'
           #                '<span style="font-family: Helvetica; font-size:8px">(.*?)<br></span>',
           #                programinfo.group(0)))
           #
           # # if RecordSource: RecordSource = re.escape(RecordSource)
           #
           #  # since we escaped the program name we need to unescape
           #  #if 'Name' in locals():  Name = re.sub(r'\\(.)', r'\1', Name)
           #
           #  # since we escaped the address we need to unescape
           #  #if 'address' in locals():
           #   #   address = re.sub(r'\\(.)', r'\1', address)
           #  #else:
           #   #   address = ''
           #
           #
           #  # write then delete the elements
           #  finline = [Name,address,DateFirstLastSeen, SSN ,DOB, Phone, RecordSource]
            finline = [Name]
            del Name
            filewriter.writerow(finline)
            # del Name,address,DateFirstLastSeen, SSN ,DOB, Phone, RecordSource


path ='PackageARequest_8976_62405_20170501_100950.pdf'
outpath = 'test.csv'


time1 = time.time()
alltext = convert_pdf_to_html(path)
time2 = time.time()
print (time2-time1)




pattern = '(?<=contact information would have been considered current for you.\n<br></span></div>)(.*?)(?=Address Characteristics\n<br></span>)'
createDirectory(alltext, outpath, pattern)