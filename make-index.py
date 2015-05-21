#! /usr/bin/env python
import khmer
import screed
import argparse
from cPickle import dump

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genomes')
    parser.add_argument('prefix')
    parser.add_argument('-k', type=int, dest='ksize', default=32)
    parser.add_argument('-x', type=float, dest='tablesize', default=1e7)
    parser.add_argument('-N', type=int, dest='n_tables', default=4)
    parser.add_argument('--nodegraph', action='store_true',
                        dest='nodegraph', default=False)
    args = parser.parse_args()

    # build a label hash + readaligner.
    if args.nodegraph:
        lh = khmer.LabelHash(args.ksize, args.tablesize, args.n_tables)
    else:
        lh = khmer.CountingLabelHash(args.ksize, args.tablesize, args.n_tables)

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
