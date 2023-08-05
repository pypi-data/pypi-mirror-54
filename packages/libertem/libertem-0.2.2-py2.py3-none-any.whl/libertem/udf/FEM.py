import numpy as np

from libertem.masks import _make_circular_mask
from libertem.udf import UDF


class FEMUDF(UDF):
    '''
    Perform Fluctuation EM :cite:`Gibson1997`

    This UDF calculates the standard deviation within a ring around the zero order diffraction peak.
    '''
    def __init__(self, *args, **kwargs):
        '''
        center: tuple
            (x,y) - coordinates of a center of a ring for a masking region of interest to
            calculate SD

        rad_in: int
            Inner radius of a ring mask

        rad_out: int
            Outer radius of a ring mask
        '''
        super().__init__(*args, **kwargs)

    def get_result_buffers(self):
        return {
            'intensity': self.buffer(
                kind="nav", dtype="float32"
            ),
        }

    def get_task_data(self):
        center = self.params.center
        sig_shape = tuple(self.meta.partition_shape.sig)
        rad_out, rad_in = self.params.rad_out, self.params.rad_in
        mask_out = 1*_make_circular_mask(
            center[1], center[0],
            sig_shape[1], sig_shape[0],
            rad_out
        )
        mask_in = 1*_make_circular_mask(
            center[1], center[0],
            sig_shape[1], sig_shape[0],
            rad_in
        )
        mask = mask_out - mask_in

        kwargs = {
            'mask': mask,
        }
        return kwargs

    def process_frame(self, frame):
        self.results.intensity[:] = np.std(frame[self.task_data.mask == 1])


def run_fem(ctx, dataset, center, rad_in, rad_out, roi=None):
    """
    Return a standard deviation(SD) value for each frame of pixels which belong to ring mask.

    Parameters
    ----------

    ctx: Context
        Context class that contains methods for loading datasets,
        creating jobs on them and running them

    dataset: DataSet
        A dataset with 1- or 2-D scan dimensions and 2-D frame dimensions

    center: tuple
        (x,y) - coordinates of a center of a ring for a masking region of interest to calculate SD

    rad_in: int
        Inner radius of a ring mask

    rad_out: int
        Outer radius of a ring mask

    Returns
    -------

    pass_results: dict
        Returns a standard deviation(SD) value for each frame of pixels which belong to ring mask.
        To return 2-D array use pass_results['intensity'].data

    """
    udf = FEMUDF(center=center, rad_in=rad_in, rad_out=rad_out)
    pass_results = ctx.run_udf(dataset=dataset, udf=udf, roi=roi)
    return pass_results
