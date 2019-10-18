#!/usr/bin/env python

""" MultiQC module to parse output from fgbio GroupReadsByUmi
"""

from __future__ import print_function
from collections import OrderedDict

import logging

# Initialise the logger
log = logging.getLogger(__name__)

class GroupReadsByUmiMixin():

    def parse_groupreadsbyumi_log(self):
        umi_data = dict()

        for f in self.find_log_files('fgbio/groupreadsbyumi'):
            # add file to data sources
            self.add_data_source(f)
            sample_name = f['s_name']
            family_size = []
            for line in f['f'].splitlines():
                if not line.startswith("family_size"):
                    family_size.append(tuple(line.split("\t")))

            umi_data[sample_name] = { int(s):int(d[1]) for s, d in enumerate(family_size,1)}

        if not umi_data:
            raise UserWarning("No fgbio GroupReadsByUmi logs found")

        #Filter samples
        umi_data = self.ignore_samples(umi_data)

        log.info("Processed {} report(s)".format(len(umi_data)))

        return umi_data
