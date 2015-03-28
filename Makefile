NULLGRAPH=../nullgraph

all: genomes.fa reads-a.fa reads-b.fa

do:
	multi-align.py genomes.fa reads-a.fa
	multi-align.py genomes.fa reads-b.fa

genomes.fa:
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 1 --name='genomeA' > genome-a.fa
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 2 --name='genomeB' > genome-b.fa
	cat genome-a.fa genome-b.fa > genomes.fa

reads-a.fa: genome-a.fa
	$(NULLGRAPH)/make-reads.py -r 100 -e 0.00 -C 10 -S 1 genome-a.fa | head -6 > reads-a.fa

reads-b.fa: genome-b.fa
	$(NULLGRAPH)/make-reads.py -r 100 -e 0.00 -C 10 -S 1 genome-b.fa | head -6 > reads-b.fa
