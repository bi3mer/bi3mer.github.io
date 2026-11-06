+++
date = '2018-07-29T14:53:17-05:00'
draft = false
title = 'Redacting PDFs'
+++
One day at work, I walked by someone who was going through a large set of PDFs and for everyone he put a block box over the name field. He mentioned it would take him several hours to accomplish this extremely menial task. Naturally, I found myself attracted to the problem due to my love of automation. I decided then and there I would write a small script that he could use to redact large set of similarly formatted PDFs.

# Ease of Use
When going about this problem, I knew the most important part in the design would be ease of use. It couldn’t be a programmer’s tool with command line arguments and a readme file to boot. The most I could ask of this person was to open a terminal and type `python redact.py`. To address this problem there has to be GUI elements that allow the user to use familiar tools to define how and where the redaction takes place.

To address the problem of selecting pdfs, I decided to use [TKinter](https://wiki.python.org/moin/TkInter), an easy to use tool that allows us to open a file explorer to select files or directories (this tool also does much more). With TKinter we have the first ease of use problem solved by making it so command line arguments won’t be needed to define where the program should find the pdfs, but we don’t have an easy way to choose where in a pdf a redaction should take place.

In my google searches I found many potential solutions, but none of them seemed reliable. One interesting approach was decoding pdfs into parsable fields, but past experience has shown me how unreliable parsing a pdf can be. I thought about allowing the user to define coordinates for where a black box should go to hide text. This was suboptimal, though, because it required multiple tests for the user to get the coordinates exactly right. After a bit more searching, I realized I could merge two pdfs. The first pdf would be the one we want to redact and the second would contain the black boxes that redacted the fields.

With both problems solved, in theory, I had an easy program flow:

1. Ask the user for the directory where the pdfs are located
2. Ask the user for the directory where all the redcated pfs should be located (you should never modify original files that are of any import)
3. Ask the user for the pdf that only contains the redactions and is otherwise blank
4. Redact the pdfs and put them in the outupt directory

# Merging a PDF
Merging a pdf is pretty simple thanks to [PyPDF2](https://pypi.org/project/PyPDF2/). We can use there `PdfFileReader` to read in pdfs from file paths. We get these paths with TKinter seen in the code at the bottom of the page. We will also need to create a new pdf with there `PdfFileWriter` that we can write to while merging two pdfs.

```python
def redact(original_file_location, blocker_file_location):
    output   = PdfFileWriter()
    original = PdfFileReader(file(original_file_location, "rb"))
    blocker  = PdfFileReader(file(blocker_file_location, "rb"))

    if original.getNumPages() != blocker.getNumPages():
        print "original has", original.getNumPages(), "pages while the blocker has", blocker.getNumPages(), "which is invalid."
        return

    for page in xrange(original.getNumPages()):
        output_page = original.getPage(page)
        output_page.mergePage(blocker.getPage(page))

        output.addPage(output_page)

    return output
```

After that, we need to make sure the user hasn’t made any errors in selecting the redacting pdf or the directory. To do so, we check every pdf and the number of pages they have. If the page count does not match, then we cannot redact the pdf. An error is logged and the attempt to merge the two pdfs is dropped.

With the error check done, we simply loop through every page in the pdf and call the `mergePage` function. We add the output into the `PdfFileWriter` and we have successfully merged the two pdfs.

```python
output = redact(os.path.join(input_directory, file), blocking_file)
output_file = os.path.join(output_directory, file)

with open(output_file, 'wb') as f:
    output.write(f)
```

After calling the redact function, we can write the file to the output directory without any extra work having to be done thanks to the convenience of the `PdfFileWriter`.

# Error and Conclusion
At this point in the process, I was pretty stoked and ran the program and saw no errors. So I ran it on the real pdfs and showed off the results. The one I was helping, however, had other plans and opened the first redacted pdf with Adobe. He clicked on the black box that had redacted the participants name and, much to my horror, dragged the black box away to reveal the name of the participant. As mentioned before, I had kept the originals so there wasn’t any real issue with this, but it was disappointing.

```python
output = redact(os.path.join(input_directory, file), blocking_file)
output_file = os.path.join(output_directory, file)
temp_output_file = output_file + "_temp"

with open(temp_output_file, 'wb') as f:
    output.write(f)

os.system("pdf2ps " + temp_output_file + " - | " + "ps2pdf - " + output_file)
os.remove(temp_output_file)
```

It turns out that pdfs can have layers and when I merged the pdfs I simply wrote another layer on top of the original layer. My redaction was purely visual. I had to find a way to strip a pdf of it’s layers. I spent longer than I should have looking for a clean way to do this but couldn’t find anything. Eventually, I settled on writing a temp pdf in the output directory. After, I used a os.system to use [PS2PDF](https://web.mit.edu/ghostscript/www/Ps2pdf.htm) which would remove the layers while keeping the original result. This last step drastically slowed down the redaction process, but after that it worked exactly as intended and saved a ton of time.

```python
from PyPDF2 import PdfFileWriter, PdfFileReader
import Tkinter, tkFileDialog, tkMessageBox
import pypdftk
import os

def redact(original_file_location, blocker_file_location):
    output   = PdfFileWriter()
    original = PdfFileReader(file(original_file_location, "rb"))
    blocker  = PdfFileReader(file(blocker_file_location, "rb"))

    if original.getNumPages() != blocker.getNumPages():
        print "original has", original.getNumPages(), "pages while the blocker has", blocker.getNumPages(), "which is invalid."
        return

    for page in xrange(original.getNumPages()):
        output_page = original.getPage(page)
        output_page.mergePage(blocker.getPage(page))

        output.addPage(output_page)

    return output

def redact_files_in_directory(input_directory, output_directory, blocking_file):
    files = os.listdir(input_directory)
    length = len(files)

    for i in range(length):
        file = files[i]
        if os.path.isfile(file):
            print file, "is not a file and cannot be converted"
            continue
        elif file.endswith('.pdf') == False:
            print file, 'does not have the ".pdf" file extension and cannot be converted'
            continue

        output = redact(os.path.join(input_directory, file), blocking_file)
        output_file = os.path.join(output_directory, file)
        temp_output_file = output_file + "_temp"

        with open(temp_output_file, 'wb') as f:
            output.write(f)
        
        print "(" + str(i) + "/" + str(length - 1) + "): ", file
        os.system("pdf2ps " + temp_output_file + " - | " + "ps2pdf - " + output_file)
        os.remove(temp_output_file)

    # only works on mac
    os.system('say "your program has finished"')

def get_new_directory_path(window_title, window_message):
    tkMessageBox.showinfo(window_title, window_message)
    return tkFileDialog.askdirectory()

def get_new_file_path(window_title, window_message):
    tkMessageBox.showinfo(window_title, window_message)
    return tkFileDialog.askopenfilename()

if __name__ == '__main__':
    input_directory = get_new_directory_path(
        "Input Directory",
        "Select input directory path with files to be redacted.")

    output_directory = get_new_directory_path(
        "Output Directory", 
        "Select output directory path.")

    blocking_file = get_new_file_path(
        "Blocking File",
        "Select pdf to block all pdf files in input directory " + input_directory)

    if blocking_file.endswith('.pdf') == False:
        print "blocking files must be a pdf file where the extension is '.pdf'"
    else:
        redact_files_in_directory(input_directory, output_directory, blocking_file)
```