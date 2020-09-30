"""Creates a fasta file for MHC sequences.

These are to be used as input for a MSA alignment tool such as clustal.
"""
from absl import app
from absl import flags

import tensorflow as tf

from bio_tfds.mhc import mhcflurry

FLAGS = flags.FLAGS

flags.DEFINE_string("outfile", None, "")
flags.mark_flag_as_required("outfile")

flags.DEFINE_list("species", None, "")
flags.DEFINE_list("genes", None, "")
flags.DEFINE_list("exclude_genes", None, "")

flags.DEFINE_string("data_dir", 'None', "")


def get_dataset():
    species = FLAGS.species or None
    genes = FLAGS.genes or None
    exclude_genes = FLAGS.exclude_genes or None

    dsb = mhcflurry.MhcBindingAffinity(
        data_dir=None if FLAGS.data_dir == "None" else FLAGS.data_dir,
        normalize_measurement=True,
        include_inequalities=True,
        species=species,
        genes=genes,
        exclude_genes=exclude_genes,
    )

    return dsb.as_dataset(split="train")


def main(_):
    seen_alleles = set()
    with open(FLAGS.outfile, 'w') as f:
        for x in get_dataset().as_numpy_iterator():
            mhc_allele = tf.compat.as_str(x['mhc_allele'])
            mhc_sequence = tf.compat.as_str(x['mhc_sequence'])
            # The sequence for that allele looks wrong.
            if mhc_allele in seen_alleles or mhc_allele == 'BoLA-2*08:01':
                continue
            seen_alleles.add(mhc_allele)
            f.write(f">{mhc_allele}\n")
            f.write(f"{mhc_sequence}\n")


if __name__ == "__main__":
    app.run(main)
