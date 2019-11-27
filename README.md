# dupre
Duplicates Remover

Dupre provides an easy-to-use streamlit UI for imagededup package that simplifies the task of finding **exact** and **near duplicates** in an image collection. 

Imagededup package provides a bunch of hashing algorithms that are particularly good at finding exact duplicates. It also provides a convolutional neural networks which are adept at finding near duplicates. An evaluation
framework is also provided to judge the quality of deduplication for a given dataset.

Detailed documentation of the package can be found at: [https://idealo.github.io/imagededup/](https://idealo.github.io/imagededup/)

Dupre is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. It is distributed under the Apache 2.0 license.

## Installation
* Install streamlit from PyPI (recommended):

```
pip install streamlit
```

> **Note**: imagededup comes with TensorFlow CPU-only support by default. If you have GPUs, you should rather
> install the TensorFlow version with GPU support especially when you use CNN to find duplicates. It's way faster. See the
> [TensorFlow guide](https://www.tensorflow.org/install/gpu) for more details on how to install it.

* Install imagededup from the GitHub source:

```bash
git clone https://github.com/amolnaik/dupre.git
cd imagededup
pip install "cython>=0.29"
python setup.py install
```  

## Quick Start

In order to find duplicates in an image directory start by:

```
cd streamlit_test
streamlit run deduper.py
```

## © Copyright
See [LICENSE](LICENSE) for details.
