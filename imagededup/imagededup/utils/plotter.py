import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib import figure
from pathlib import Path, PosixPath
from typing import Dict, Union, List

import numpy as np
from PIL import Image


def _formatter(val: Union[int, np.float32]):
    """
    For printing floats only upto 3rd precision. Ints are unchanged.
    """
    if isinstance(val, np.float32):
        return f'{val:.3f}'
    else:
        return val


def _plot_images(
    image_dir: PosixPath,
    orig: str,
    image_list: List,
    scores: bool = False,
    outfile: str = None,
) -> None:
    """
    Plotting function for plot_duplicates() defined below.

    Args:
        image_dir: image directory where all files in duplicate_map are present.
        orig: filename for which duplicates are to be plotted.
        image_list: List of duplicate filenames, could also be with scores (filename, score).
        scores: Whether only filenames are present in the image_list or scores as well.
        outfile:  Name of the file to save the plot.
    """
    n_ims = len(image_list)
    ncols = 4  # fixed for a consistent layout
    nrows = int(np.ceil(n_ims / ncols)) + 1

    plt.rcParams["figure.figsize"] = (40, 56)

    '''
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(Image.open(image_dir / orig))
    ax2.imshow(Image.open(image_dir / orig))

    '''

    gs = gridspec.GridSpec(nrows=nrows, ncols=ncols)
    ax = plt.subplot(gs[0, 0])
    ax.imshow(Image.open(image_dir / orig))
    ax.set_title('Original Image: {}'.format(orig))
    ax.axis('off')

    for i in range(0, n_ims):

        ax = plt.subplot(gs[0, i+1])
        if scores:
            ax.imshow(Image.open(image_dir / image_list[i][0]))
            val = _formatter(image_list[i][1])
            title = ' '.join([image_list[i][0], f'({val})'])
        else:
            ax.imshow(Image.open(image_dir / image_list[i]))
            title = image_list[i]

        ax.set_title(title)
        ax.axis('off')

    if outfile:
        plt.savefig(outfile)


def _validate_args(
    image_dir: Union[PosixPath, str], duplicate_map: Dict, filename: str
) -> PosixPath:
    """Argument validator for plot_duplicates() defined below.
    Return PosixPath to the image directory"""

    image_dir = Path(image_dir)
    assert (
        image_dir.is_dir()
    ), 'Provided image directory does not exist! Please provide the image directory where all files are present!'

    if not isinstance(duplicate_map, dict):
        raise ValueError('Please provide a valid Duplicate map!')
    if filename not in duplicate_map.keys():
        raise ValueError(
            'Please provide a valid filename present as a key in the duplicate_map!'
        )
    return image_dir


def plot_duplicates(
    image_dir: Union[PosixPath, str],
    duplicate_map: Dict,
    filename: str,
    outfile: str = None,
) -> None:
    """
    Given filename for an image, plot duplicates along with the original image using the duplicate map obtained using
    find_duplicates method.

    Args:
        image_dir: image directory where all files in duplicate_map are present.
        duplicate_map: mapping of filename to found duplicates (could be with or without scores).
        filename: Name of the file for which duplicates are to be plotted, must be a key in the duplicate_map.
        dictionary.
        outfile: Optional, name of the file to save the plot. Default is None.

    Example:
    ```
        from imagededup.utils import plot_duplicates
        plot_duplicates(image_dir='path/to/image/directory',
                        duplicate_map=duplicate_map,
                        filename='path/to/image.jpg')
    ```
    """
    # validate args
    image_dir = _validate_args(image_dir=image_dir, duplicate_map=duplicate_map, filename=filename)

    retrieved = duplicate_map[filename]
    assert len(retrieved) != 0, 'Provided filename has no duplicates!'

    # plot
    if isinstance(retrieved[0], tuple):
        _plot_images(
            image_dir=image_dir,
            orig=filename,
            image_list=retrieved,
            scores=True,
            outfile=outfile,
        )
    else:
        _plot_images(
            image_dir=image_dir,
            orig=filename,
            image_list=retrieved,
            scores=False,
            outfile=outfile,
        )
