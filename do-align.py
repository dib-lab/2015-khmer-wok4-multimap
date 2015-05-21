#! /usr/bin/env python
import sys
import khmer
import screed
import argparse
from cPickle import load

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('index')
    parser.add_argument('reads')
    args = parser.parse_args()

    print >>sys.stderr, "Loading graph & labels"
    cg = khmer.load_counting_hash(args.index + '.graph')
    lh = khmer._LabelHash(cg)
    lh.load_labels_and_tags(args.index + '.labels')
    fp = open(args.index + '.list', 'rb')
    names = load(fp)
    fp.close()

    print 'loaded %d references' % (len(names),)
    aligner = khmer.ReadAligner(cg, 1, 1.0)

    # run through all the queries, align, and use alignments to look up
    # the label.
    for record in screed.open(args.reads):
        # build alignments against cg
        _, ga, ra, truncated = aligner.align(record.sequence)

        # now grab the tags associated with the alignment
        ga = ga.replace('-', '')
        labels = lh.sweep_label_neighborhood(ga)

        # retrieve the labels associated with the tags
        matches = set([ names[i] for i in labels ])

        # print out the matches.
        print record.name, len(matches), ", ".join(matches)

if __name__ == '__main__':
    main()
