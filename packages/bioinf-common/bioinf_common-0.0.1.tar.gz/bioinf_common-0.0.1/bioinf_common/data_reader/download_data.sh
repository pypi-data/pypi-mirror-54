#!/usr/bin/env bash


target_dir=${1-data}
url_list=(
    'https://downloads.thebiogrid.org/Download/BioGRID/Release-Archive/BIOGRID-3.4.160/BIOGRID-ORGANISM-3.4.160.tab2.zip'  # BioGRID-PPI
    'ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/goa_human.gaf.gz'  # GO-Term/gene associations
    'https://stringdb-static.org/download/protein.links.detailed.v10.5/9606.protein.links.detailed.v10.5.txt.gz'  # StringDB-PPI
)

for url in ${url_list[*]}; do
    echo "Downloading $(basename $url)"
    wget --quiet -P "$target_dir" "$url"
done
