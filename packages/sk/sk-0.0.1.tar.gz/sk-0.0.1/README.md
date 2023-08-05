Utilities for scikit-learn to quickly build and experiment with machine learning models.

## Installation

```sh
pip install sk
```

## Usage

```py
from sk import *

iris = datasets.load_iris()
X, y = iris.data, iris.target

model = SVC(gamma='scale')
model.fit(X, y)
```
