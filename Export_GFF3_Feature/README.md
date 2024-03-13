**Summary**

The export_gff3_feature project finds and exports features within the S. cerevisiae annotation gff3 file.

**Project Description**

export_gff3_feature aims to search and output sequences within the Saccharomyces_cerevisiae_S288C.annotation.gff FASTA file. The program accepts four command line arguments and uses regex to find and match particular text substrings. The search algorithm first locates the particular chromosome required, determines which direction to read the DNA sequence, and then finds the particular input and outputs it. 

**Skills Learned**

-Pattern matching functions within regex library
-Understanding command line arguments
-Utilizing different data storage types (lists, dictionaries)

**Libraries Required**

-re
-sys
