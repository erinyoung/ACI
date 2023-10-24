#!/usr/bin/env python3
"""ACI"""

import argparse
import concurrent.futures
import itertools
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pysam
from src.lib.amplicon_depth import aci_depth