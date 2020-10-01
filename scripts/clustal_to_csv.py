"""Go from a clustal alignment to a csv."""
import csv

from absl import app
from absl import flags

from Bio import AlignIO

FLAGS = flags.FLAGS

flags.DEFINE_string("infile", None, "")
flags.mark_flag_as_required("infile")

flags.DEFINE_string("outfile", None, "")
flags.mark_flag_as_required("outfile")


def main(_):
    alignment = AlignIO.read(FLAGS.infile, "clustal")

    with open(FLAGS.outfile, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['name', 'seq'])
        for seq in alignment:
            writer.writerow([seq.id, str(seq.seq)])


if __name__ == "__main__":
    app.run(main)
