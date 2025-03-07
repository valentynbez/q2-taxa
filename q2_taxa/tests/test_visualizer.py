# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import tempfile
import unittest

import biom
import numpy as np
import pandas as pd
import qiime2

from q2_taxa import barplot


class BarplotTests(unittest.TestCase):

    def setUp(self):
        self.table = biom.Table(np.array([[2.0, 2.0], [1.0, 1.0], [9.0, 8.0],
                                          [0.0, 4.0]]),
                                ['A', 'B', 'C', 'D'],
                                ['feat1', 'feat2']).transpose()
        self.taxonomy = pd.Series(['a; b; c', 'a; b; d'],
                                  index=['feat1', 'feat2'])

    def test_barplot(self):
        metadata = qiime2.Metadata(
            pd.DataFrame({'val1': ['1.0', '2.0', '3.0', '4.0']},
                         index=pd.Index(['A', 'B', 'C', 'D'], name='id')))

        with tempfile.TemporaryDirectory() as output_dir:
            barplot(output_dir, self.table, self.taxonomy, metadata)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue("src='level-1.jsonp?callback=load_data'" in
                            open(index_fp).read())
            csv_lvl3_fp = os.path.join(output_dir, 'level-3.csv')
            self.assertTrue(os.path.exists(csv_lvl3_fp))
            self.assertTrue('val1' in open(csv_lvl3_fp).read())

    def test_barplot_metadata_extra_id(self):
        metadata = qiime2.Metadata(
            pd.DataFrame({'val1': ['1.0', '2.0', '3.0', '4.0', '5.0']},
                         index=pd.Index(['A', 'B', 'C', 'D', 'E'], name='id')))

        with tempfile.TemporaryDirectory() as output_dir:
            barplot(output_dir, self.table, self.taxonomy, metadata)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue("src='level-1.jsonp?callback=load_data'" in
                            open(index_fp).read())
            csv_lvl3_fp = os.path.join(output_dir, 'level-3.csv')
            self.assertTrue(os.path.exists(csv_lvl3_fp))

    def test_barplot_metadata_missing_id(self):
        metadata = qiime2.Metadata(
            pd.DataFrame({'val1': ['1.0', '2.0', '3.0']},
                         index=pd.Index(['A', 'B', 'C'], name='id')))

        with tempfile.TemporaryDirectory() as output_dir:
            with self.assertRaisesRegex(ValueError, 'missing.*D'):
                barplot(output_dir, self.table, self.taxonomy, metadata)

    def test_barplot_no_metadata(self):
        with tempfile.TemporaryDirectory() as output_dir:
            barplot(output_dir, self.table, self.taxonomy)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
            self.assertTrue("src='level-1.jsonp?callback=load_data'" in
                            open(index_fp).read())
            csv_lvl3_fp = os.path.join(output_dir, 'level-3.csv')
            self.assertTrue(os.path.exists(csv_lvl3_fp))
            self.assertTrue('val1' not in open(csv_lvl3_fp).read())
    
    def test_barplot_full_taxonomy_false(self):
        with tempfile.TemporaryDirectory() as output_dir:
            barplot(output_dir, self.table, self.taxonomy, 
                    metadata=None, full_taxonomy=False)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))
