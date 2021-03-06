#! /usr/bin/env python
import khmer
import screed
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genomes')
    parser.add_argument('reads')
    args = parser.parse_args()

    # build a counting label hash + readaligner.
    lh = khmer.CountingLabelHash(21, 1e7, 4)
    lh.consume_fasta_and_tag_with_labels(args.genomes)
    aligner = khmer.ReadAligner(lh.graph, 1, 1.0)

    names = []
    # (labels in 'lh' are in the order of the sequences in the file)
    for grec in screed.open(args.genomes):
        names.append(grec.name)

    print 'loaded two references:', names

    # run through all the reads, align, and use alignments to look up
    # the label.
    for record in screed.open(args.reads):
        # build alignments against cg
        _, ga, ra, truncated = aligner.align(record.sequence)

        if truncated:
            print 'NO MATCHES', record.name
        else:
            # now grab the associated labels
            labels = lh.sweep_label_neighborhood(ga)

            # print out the matches.
            matches = set([ names[i] for i in labels ])
            print record.name, 'matches to', ", ".join(matches)

if __name__ == '__main__':
    main()
