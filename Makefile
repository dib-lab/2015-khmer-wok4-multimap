NULLGRAPH=../nullgraph

all: fake rna rseq.labelcount ecoli

clean:
	-rm -f genome-?.fa reads-?.fa *.graph *.labels *.list 

fake: reads-a.fa reads-b.fa
	./make-index.py genomes.fa genomes
	./do-align.py genomes reads-a.fa
	./do-align.py genomes reads-b.fa

genomes.fa:
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 1 --name='genomeA' > genome-a.fa
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 2 --name='genomeB' > genome-b.fa
	cat genome-a.fa genome-b.fa > genomes.fa

reads-a.fa: genomes.fa
	$(NULLGRAPH)/make-reads.py -r 100 -C 10 -S 1 genome-a.fa | head -6 > reads-a.fa

reads-b.fa: genomes.fa
	$(NULLGRAPH)/make-reads.py -r 100 -C 10 -S 1 genome-b.fa | head -6 > reads-b.fa

rna.graph: rna.fa
	./make-index.py -k 21 -x 8e7 -N 4 rna.fa rna

rna: rna.graph
	./do-align.py rna rna-reads.fq

rseq.labelcount: rna.graph
	python ./do-counting.py rna rseq-mapped.fq.gz > rseq.labelcount

bacteria.graph: bacteria.fa.gz
	./make-index.py -k 21 -x 1e7 -N 4 bacteria.fa.gz bacteria

ecoli: bacteria.graph
	./do-align.py bacteria ecoli-p12b-reads.fa
