This folder contains files downloaded from the CisBP database, which contains information on transcription factors (TFs), and their motifs. The folder itself is named after the subset of data you chose to download, with the date and time it was downloaded appended at the end. Depending on what you chose to download, this directory contains a subset of the following files:


logos_all_motifs - directory containing .png images in the form of sequence logos, which visually depict the sequence binding preferences of a given TF obtained from a single experimental source.  Each file is named by its Motif_ID (see description of the text files below).


pwms_all_motifs - directory containing text files giving the frequency of each base at each position in the motif.  Each file is named by its Motif_ID (see below).


Escores/Zscores.txt - these text files are matrices providing the E- and Z-scores from each Protein Binding Microarry (PBM) assay, for all 32,896 possible 8-mers.  E-scores range from -0.5 to +0.5; 8-mers with E-scores >= 0.45 are considered "strongly bound" by the associated TF.  Z-scores can have arbitrary 
ranges, with higher scores indicating stronger binding.  See Berger et al. Nature Genetics 2006 for additional details.


TF_Information.txt, TF_Information_all_motifs.txt, TF_Information_all_motifs_plus.txt - These files contain information on the TFs.  

'TF_Information.txt' contains, for each TF, all directly determined motifs (see below). If a TF does not have a directly determined motif, this file will also include its best inferred motif.  'Best' is defined as the motif(s) obtained from the most similar TF (based on the %ID in the amino acids of its TF) that has a directly determined motif.

'TF_Information_all_motifs.txt' is a superset of 'TF_Information.txt'.  It also includes any motif that can be inferred for a given TF, given the TF family-specific threshold.  For example, if a TF has a directly determined motif, and two TFs with motifs with 90% and 80% identical DBDs to it, TF_Information.txt will only include the direct motif, but
TF_Information_all_motifs.txt will include all three motifs.  Likewise, if a TF does not have a direct motif, but has two TFs with 90% and 80% identical DBDs to it, TF_Information.txt will only include the motif from the 90% indentical TF, while TF_Information_all_motifs.txt would include both.

'TF_Information_all_motifs_plus.txt' is a superset of the other two files.  It contains all motifs for a given TF, which includes all direct motifs, and all inferred motifs above the threshold.

The files have identical formats. Each file contains one row per TF.  TFs with multiple motifs have one line per motif. The columns in the file are as follows:

TF_ID: Internal CisBP ID for the TF.  Each gene has a unique TF_ID.

Family_ID: Internal CisBP ID for the TF family.  A family is the unique set of DNA binding domains (DBDs) present in the protein.

TSource_ID: Internal CisBP ID for the source of the TF (i.e. where its genome sequence was obtained).

Motif_ID: Internal CisBP ID for the associated motif.

MSource_ID: Internal CisBP ID for the source of the motif (i.e. which database or study it came from)

DBID: External ID of the RBP (e.g., Ensembl ID)

TF_Name: Name of the TF

TF_Species: Species of the TF

TF_Status: Motif status of the TF. 'D' stands for directly determined motif.  'I' indicates that the motif is inferred from another TF, based on DBD similarity (see Weirauch et al. 2013 for details). 'N' means no motif is available.

Family_Name: Name of the TF's family

DBDs: The unique set of DBDs (Pfam names) present in the TF

DBD_Count: Number of unique DBDs in the TF

Cutoff: Cutoff used to infer motifs for the TF family

DBID: Motif ID from the associated database or study

Motif_Type: Experimental assay used to determine the motif

MSource_Identifier: ID for the source of the motif (i.e., its project name)

MSource_Type: Internal CisBP ID for the motif category

MSource_Author: First author for the source of the motif

MSource_Year: Year of publication of the motif source

PMID: Pubmed ID of the motif source

MSource_Version: Version of the source (i.e. database build)

TFSource_Name: Source of the TF (i.e. where did the genome build come from?)

TFSource_URL: URL of the TF source

TFSource_Year: Year the genome data was downloaded

TFSource_Month: Month the genome data was downloaded

TFSource_Day: Day the genome data was downloaded

Questions can be directed to Matt Weirauch: mattweirauch@gmail.com
