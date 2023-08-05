# AutoDraft Package
This package contains the necessary modules for running the various scripts within the [AutoDraft](https://github.com/j4th/AutoDraft) project. Namely:
 - `api.py`: Wrapper for the NHL's undocumented (mostly, shout-out to [dword4](https://gitlab.com/dword4/nhlapi)) API.
 - `arima.py`: Module for performing Auto-ARIMA modelling and predictions using [pmdarima](https://www.alkaline-ml.com/pmdarima/).
 - `gluonts.py`: Module for performing DeepAR modelling and predictions; could be extended to any [GluonTS](https://gluon-ts.mxnet.io/) model.
 - `visualization.py`: Module for visualizing model output and performance, largely through leveraging [Bokeh](https://bokeh.pydata.org/en/latest/index.html).