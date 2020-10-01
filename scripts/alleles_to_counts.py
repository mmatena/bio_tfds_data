"""Count the number of datapoints for which each MHC allele appears.

The operator (<,>,=) is also used to separate groupings.
"""
import collections
import csv

from absl import app
from absl import flags

import tensorflow as tf

from bio_tfds.mhc import mhcflurry

FLAGS = flags.FLAGS

flags.DEFINE_string("outfile", None, "")
flags.mark_flag_as_required("outfile")

flags.DEFINE_string("data_dir", 'None', "")


def get_dataset():
    dsb = mhcflurry.MhcBindingAffinity(
        data_dir=None if FLAGS.data_dir == "None" else FLAGS.data_dir,
        normalize_measurement=True,
        include_inequalities=True,
    )
    return dsb.as_dataset(split="train")


def main(_):
    ds = get_dataset()
    ds = ds.map(lambda x: (x['mhc_allele'], x['measurement_inequality']))
    counter = collections.Counter(ds.as_numpy_iterator())
    with open(FLAGS.outfile, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for (allele, inequality), count in counter.most_common():
            writer.writerow([tf.compat.as_str(allele), mhcflurry.MEASUREMENT_INEQUALITIES[inequality], count])


if __name__ == "__main__":
    app.run(main)
