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


def test_signal_normalize(tmp_path):
    sig = np.sin(2*np.pi*np.linspace(0,1,50))
    sig1 = sig * .8
    sig2 = sig * .4

    rms_out1 = 0.700 # Should be very close to full amplitude
    rms_out2 = 0.350 # Should be very close to half amplitude

    with tempfile.TemporaryDirectory() as tmpdirin:
        infile1 = os.path.join(tmpdirin, 'file1.wav')
        infile2 = os.path.join(tmpdirin, 'file2.wav')
        wavwrite(infile1, 50, sig1)
        wavwrite(infile2, 50, sig2)

        with tempfile.TemporaryDirectory() as tmpdirout:
            psylab.signal.normalize(tmpdirin, ext='wav', outdir=tmpdirout, relative=False)

            fs,out1 = wavread(os.path.join(tmpdirout, 'file1.wav'))
            fs,out2 = wavread(os.path.join(tmpdirout, 'file2.wav'))

            #print("sig: {:}".format(np.sqrt(np.mean(np.square(sig)))))
            #print("sig1: {:}".format(np.sqrt(np.mean(np.square(sig1)))))
            #print("sig2: {:}".format(np.sqrt(np.mean(np.square(sig2)))))
            #print("out1: {:}".format(np.sqrt(np.mean(np.square(out1)))))
            #print("out2: {:}".format(np.sqrt(np.mean(np.square(out2)))))

            np.testing.assert_allclose(rms_out1, np.sqrt(np.mean(np.square(out1))), rtol=1e-3)
            np.testing.assert_allclose(rms_out2, np.sqrt(np.mean(np.square(out2))), rtol=1e-3)

