Using extractframes
===================

Running `extract.py`
--------------------

The :program:`extract.py` script extracts frames from a video in a
controllable way.  It is called like this:

    :samp:`extract.py [options] {input_movie} {output_format}`

input_movie
        Some movie file in a format that :command:`ffmpeg` understands.
        Windows `.avi` files and Apple `.mov` files should work fine, among
        many others.

output_format
        A pattern for producing output files.  For example, if you want
        your files to look like :file:`img_99.jpg` and be in the
        :file:`output` directory, then you could say
        :file:`output/img_%5d.jpg`.  The :file:`%05d` in the format is what turns
        the number 99 into the string :file:`99` that becomes part of the
        filename.  Here are some examples when formatting the number 99:

.. csv-table:: Formatting examples
   :header: "Format", "Result", "Comment"
   :widths: 10, 10, 40

   :file:`img_%d.jpg`, :file:`img_99.jpg`, "Commonly used in our projects."
   :file:`img_%05d.jpg`, :file:`img_00099.jpg`, "Adds zeros until exactly 5 digits long---Usually sorts in a better way than above."
   :file:`img_%5d.jpg`, :file:`img_   99.jpg`, "Adds spaces till 5 characters long---usually not what you want."

Options
-------

.. option:: --take <BEGIN-END>
   
   After extracting all the frames from the input, which are numbered
   starting with 0, take only the frames from BEGIN to END inclusive.  They
   are renumbered to start with 0 in the output directory, so if you said
   :samp:`extract.py --take 10-20 infile.avi out%d.jpg`, then you would get
   :file:`out0.jpg` through :file:`out10.jpg` (eleven frames).  This is not
   particularly efficient, see :ref:`this discussion <correct-not-fast>`.
 
.. option:: --take-times <BEGIN-END>
   
   After extracting all the frames from the input, take only the frames
   that fall between BEGIN and END seconds from the start of the video.
   The video is assumed to be at 29.97 frames per second for this
   calculation.  For example, if you said :samp:`extract.py --take-times
   0-15.5 infile.avi out%d.jpg`, then you would get :file:`out0.jpg`
   through :file:`out464.jpg` (465 frames).  If you're counting frames,
   you should know that the American standard frame rate is actually not
   29.97 but :math:`30 * \frac{1000}{1001} \approx 29.970029970` frames per
   second.  This is only important if you have many thousands of
   frames.

.. option:: --stretch-to <FRAMES>, --squish-to <FRAMES>

   Change how many frames there will be in the output, by stretching or
   squishing time---that is, by changing the frame rate.  If your input
   has 100 frames and you say `--stretch-to 200`, then the output will
   have two copies of each frame.  This option is applied *after*
   :option:`--take` or :option:`--take-times`, so :program:`extract.py`
   will *first* take the frames that you select, and *then* stretch or
   squish those frames to fill the output requirement.

.. option:: --keep-numbers

   Normally, the output frames are renumbered so that the first frame in the
   given bounds is frame 0.  :option:`--keep-numbers` overrides this, so that
   the output frames have the same numbers as the bounds you specified
   (although this is not any *faster* than normal: [#f1]_).  So if you say
   :samp:`extract.py --take 10-20 --keep-numbers infile.avi out%d.jpg`, the
   output files will be :file:`out10.jpg` through :file:`out20.jpg`.

   If you use this option with :option:`--stretch-to`, then the first frame
   number will be the same as the first number you specify with
   :option:`--take`, but the last number will be different because there is a
   different number of frames.

 
.. [#f1]
   Under the hood, there is still renumbering happening, because
   :program:`ffmpeg` numbers frames starting with 1 but we start them with 0.
   So, unfortunately, :option:`--keep-numbers` is not any faster than the
   normal mode.


