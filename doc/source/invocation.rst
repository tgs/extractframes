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

.. option:: --stretch-to <FRAMES>, --squish-to <FRAMES>

   Change how many frames there will be in the output, by stretching or
   squishing time---that is, by changing the frame rate.  If your input has
   100 frames and you say `--stretch-to 200`, then the output will have two
   copies of each frame.  This option is applied *after* :option:`--take`,
   so :program:`extract.py` will *first* take the frames that you select, and
   *then* stretch or squish those frames to fill the output requirement.



