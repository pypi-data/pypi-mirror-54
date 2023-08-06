#!/usr/bin/env python
import glob
import argparse
import subprocess


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to directory with BAM files")
ap.add_argument("-r", "--reference", required=True, help="Path to reference genome")
ap.add_argument("-t", "--table", required=True, help="Path to result score table after detectFIO.py")
ap.add_argument("-i", "--inputTable", required=True, help="Path to table giving paths to the VCF files in column 1 "
                                                          "and paths to the corresponding BAM files in column 2")
#ap.add_argument("-s", "--samples", required=True, help="Path to directory with samples BAM files")
ap.add_argument("-c", "--control", required=True, help="Path to control BAM file")
ap.add_argument("-o", "--outputDirectory", required=True, help="Path to directory for IGV Snapshots")
args = vars(ap.parse_args())

refFile = args["reference"]
filterTable = args["table"]
bamFolder = args["directory"]
sessionDir = args["outputDirectory"]
#samplesDir = args["samples"]
inputTable = args["inputTable"]
control = args["control"]

#samples = glob.glob(samplesDir + "*.bam")

samples = list()
with open (inputTable, "r") as table:
    for line in table:
        samples.append(line.split("\t")[1].strip())


pathNameList = list()
with open(filterTable, "r") as nameFile:
    # skip header
    nameFile.readline()
    for line in nameFile:
        name = line.split("\t")[0]
        pathNameList.append((bamFolder + name, name))

for path, name in pathNameList:
    locus = name.split(".", 1)[1].replace(".bam", "")
    locus = locus.replace("bam.", "")
    #print(locus)
    sessionPath = sessionDir + locus + ".xml"
    CMPath = path
    
    # create index file for all CM so that they can be opened in the IGV Session later on
    proc = subprocess.run(["samtools", "index", CMPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    session = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    session += '<Session genome="' + refFile + '" hasGeneTrack="false" hasSequenceTrack="true" locus="' + locus + '" path="' + sessionPath + '" version="8">\n'
    session += '    <Resources>\n        <Resource path="' + CMPath + '"/>\n'
    session += '        <Resource path="' + control + '"/>\n'
    for sample in samples:
        session += '        <Resource path="' + sample + '"/>\n'

    session += '    </Resources>\n    <HiddenAttributes>\n        <Attribute name="DATA FILE"/>\n' \
               '        <Attribute name="DATA TYPE"/>\n        <Attribute name="NAME"/>\n' \
               '    </HiddenAttributes>\n</Session>'

    with open(sessionPath, "w") as out:
        out.write(session)

