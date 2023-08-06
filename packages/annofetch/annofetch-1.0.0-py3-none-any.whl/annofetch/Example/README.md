This README gives a short example which illustrates a typical annofetch call.

+++ Step 1 - Input File +++
AnnoFetch always requires an input file. For example you can use the
test_accessions.txt file which contains accessions every line.
The filename or rather the path to the file is a necessary program argument
to start AnnoFetch.

++++ Step 2 - Accession Flag +++
The input file contains accessions form Embl/NCBI/DDBJ. Therefore you can
set the --accession flag to tell the program this information. If you do not set
this flag the program will ask you weather you gave accessions from Embl/NCBI/DDBJ
as input.

+++ Step 3 - Annotations +++
By default AnnoFetch only fetches a description. But there are a lot more
annotations AnnoFetch can retrieve. For example you could set the --goa,
--organism and --ec flags to get the Gene Ontology Annotations, the Organism
and the EC number for each accession.

+++ Step 4 - Program Call +++
The program call now looks like this:

  $ annofetch test_accessions.txt --accession --goa --organism --ec

+++ Step 5 - Set Email +++
If this is the first time you call AnnoFetch after installation the program
will ask you to enter an email address:

  $ annofetch test_accessions.txt --accession --goa --organism --ec
  *** There is no valid e-mail address given yet. ***
  The email address is required to request the NCBI database.
  Please enter a valid email address or type exit to quit this dialog:

Just enter a valid email address to continue.

+++ Step 6 - Fetching Annotations +++
Now you only have to wait while AnnoFetch goes through the list of given
accessions.

+++ Step 7 - Output +++
When AnnoFetch is done you will find a file named output.csv in your current
folder (where you called AnnoFetch). The input file will contain a header and
for each given accession a line with all the annotations. The corresponding
output file content for this example is shown below (between the ++++...):

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Accession,UniProt Accession,Organism,Description,EC number,GO Annotation,Notification
AAK24111.1,Q9A6F4,Caulobacter vibrioides CB15,"5,10-methylenetetrahydrofolate reductase",1.5.1.20,"GO:0004489,GO:0005829,GO:0006555,GO:0009086,GO:0055114,GO:0004489,GO:0055114,GO:0016491,GO:0035999",
AAK22122.1,Q9ABT5,Caulobacter vibrioides CB15,conserved hypothetical protein,,"GO:0016021,GO:0016020",
EU490707,B2YD27,Selenipedium aequinoctiale,"maturase K (matK) gene, partial cds; chloroplast.",,"GO:0003723,GO:0009507,GO:0006397,GO:0009507,GO:0006397,GO:0009507,GO:0009536,GO:0008033",
AAK23580.1,Q9A7W8,Caulobacter vibrioides CB15,conserved hypothetical protein,,,
CAA38846,P23389,Bos taurus (cattle),chromogranin B,,"GO:0030141,GO:0005615,GO:0030141,GO:0005576,GO:0016020,GO:0031410,GO:0030658,GO:0005576",
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
