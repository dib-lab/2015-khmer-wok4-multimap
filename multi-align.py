#! /usr/bin/env python
import khmer
import screed
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genomes')
    parser.add_argument('reads')
    args = parser.parse_args()

    cg = khmer.new_counting_hash(21, 1e7, 4)
    cg.consume_fasta(args.genomes)

    names = []
    for grec in screed.open(args.genomes):
        names.append(grec.name)
    
    lh = khmer.LabelHash(21, 1e7, 4)
    lh.consume_fasta_and_tag_with_labels(args.genomes)

    print lh.n_labels()

    aligner = khmer.ReadAligner(cg, 1, 1.0)
    for record in screed.open(args.reads):
        _, ga, ra, truncated = aligner.align(record.sequence)
        labels = lh.sweep_label_neighborhood(ga)
        matches = set([ names[i] for i in labels ])
        print ", ".join(matches)

if __name__ == '__main__':
    main()
