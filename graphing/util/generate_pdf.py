import subprocess

#Need to install library: https://graphviz.readthedocs.io/en/stable/#installation

def pdfView(fileName : str, fileOut : str):
    subprocess.run(["dot", "-Tpdf", fileName, "-o", fileOut]) #creates single page pdf graph
   
def ottawaView(fileName : str, fileOut : str):
    # subprocess.run(["dot", "-Gcharset=latin1", "-Tps2", fileName, "-o", "{}.ps".format(fileName) ,"|", "ps2pdf", "{}.ps".format(fileName)]) #creates single page pdf graph
    subprocess.run(["dot", "-Gcharset=latin1", "-Tpdf", fileName, "-o", fileOut])