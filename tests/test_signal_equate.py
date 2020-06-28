# -*- coding: utf-8 -*-

import os
import tempfile
import numpy as np
import numpy.testing as np_testing
from scipy.io.wavfile import read as wavread, write as wavwrite
import psylab


def test_signal_equate(tmp_path):
    sig1 = np.sin(2*np.pi*np.linspace(0,1,50))
    sig2 = sig1 * .8
    with tempfile.TemporaryDirectory() as tmpdirin:
        infile1 = os.path.join(tmpdirin, 'file1.wav')
        infile2 = os.path.join(tmpdirin, 'file2.wav')
        wavwrite(infile1, 50, sig1)
        wavwrite(infile2, 50, sig2)

        with tempfile.TemporaryDirectory() as tmpdirout:
            psylab.signal.equate(tmpdirin, ext='wav', outdir=tmpdirout, relative=False)

            fs,out1 = wavread(os.path.join(tmpdirout, 'file1.wav'))
            fs,out2 = wavread(os.path.join(tmpdirout, 'file2.wav'))

            np.testing.assert_allclose(sig2, out1)
            np.testing.assert_allclose(sig2, out2)
            np.testing.assert_allclose(np.sqrt(np.mean(np.square(sig1)))*.8, np.sqrt(np.mean(np.square(out2))))

