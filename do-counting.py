#! /usr/bin/env python
import sys
import khmer
import screed
import argparse
from cPickle import load
import random

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

    print >>sys.stderr, 'loaded %d references' % (len(names),)
    aligner = khmer.ReadAligner(cg, 1, 1.0)

    counts = {}
    for k in names:
        counts[k] = 0

    # run through all the queries, align, and use alignments to look up
    # the label.
    for n, record in enumerate(screed.open(args.reads)):
        if n % 1000 == 0:
            print >>sys.stderr, '...', n

        # build alignments against cg
        _, ga, ra, truncated = aligner.align(record.sequence)

        # now grab the tags associated with the alignment
        ga = ga.replace('-', '')
        tags = lh.sweep_tag_neighborhood(ga)

        all_sets = []
        for tag in tags:
            labels = set(lh.get_tag_labels(tag))
            all_sets.append(labels)

        if not all_sets: continue

        intersect = all_sets[0]
        for x in all_sets[1:]:
            intersect.intersection_update(x)

        if not intersect:                  # ignore confused reads
            continue

        # retrieve the labels associated with the tags
        matches = list(set([ names[i] for i in intersect ]))

        hit = random.choice(matches)
        counts[hit] += 1

    for k, v in counts.iteritems():
        if v:
            print k, v


if __name__ == '__main__':
    main()
