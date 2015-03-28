#! /usr/bin/env python
import khmer
import screed
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genomes')
    parser.add_argument('reads')
    args = parser.parse_args()

    # build a countgraph to align to.
    cg = khmer.new_counting_hash(21, 1e7, 4)
    cg.consume_fasta(args.genomes)
    aligner = khmer.ReadAligner(cg, 1, 1.0)

    names = []
    for grec in screed.open(args.genomes):
        names.append(grec.name)

    print 'loaded two references:', names

    # generate a separate LabelHash that (once we have aligned) will
    # give us the identities of the sequences to which we align.
    lh = khmer.LabelHash(21, 1e7, 4)
    lh.consume_fasta_and_tag_with_labels(args.genomes)

    # run through all the reads, align to cg, take alignments, and look
    # up the labels.
    for record in screed.open(args.reads):
        # build alignments against cg
        _, ga, ra, truncated = aligner.align(record.sequence)

        # now grab the associated labels
        labels = lh.sweep_label_neighborhood(ga)

        # print out the matches.
        matches = set([ names[i] for i in labels ])
        print ", ".join(matches)

if __name__ == '__main__':
    main()
