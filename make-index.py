#! /usr/bin/env python
import khmer
import screed
import argparse
from cPickle import dump

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genomes')
    parser.add_argument('prefix')
    args = parser.parse_args()

    # build a counting label hash + readaligner.
    lh = khmer.CountingLabelHash(21, 1e7, 4)
    lh.consume_fasta_and_tag_with_labels(args.genomes)

    names = []
    # (labels in 'lh' are in the order of the sequences in the file)
    for grec in screed.open(args.genomes):
        names.append(grec.name)

    print 'loaded %d references' % (len(names),)

    print 'saving index to %s.graph/labels/list' % (args.prefix,)

    lh.graph.save(args.prefix + '.graph')
    lh.save_labels_and_tags(args.prefix + '.labels')

    fp = open(args.prefix + '.list', 'wb')
    dump(names, fp)

if __name__ == '__main__':
    main()
