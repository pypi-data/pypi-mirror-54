# logsensei

![Logo](static/images/logo.png)

Logger for Data Scientist -  [Documentation](https://adityasidharta.com/logsensei/reference/logsensei/)

[![Build Status](https://travis-ci.org/AdityaSidharta/logsensei.svg?branch=master)](https://travis-ci.org/AdityaSidharta/logsensei) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/315315d588c745929c5a3093d2b92850)](https://www.codacy.com/manual/AdityaSidharta/logsensei?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AdityaSidharta/logsensei&amp;utm_campaign=Badge_Grade) 
[![codecov](https://codecov.io/gh/AdityaSidharta/logsensei/branch/master/graph/badge.svg)](https://codecov.io/gh/AdityaSidharta/logsensei) [![Documentation](https://img.shields.io/badge/docs-passing-Green)](https://adityasidharta.com/logsensei/) ![PyPI](https://img.shields.io/pypi/v/logsensei)

## Introduction
This Python Package is build to solve one of the pain points in building Data Science projects: Having an effective logging system. As Data Science Projects often involve data ingestion, data transformation (Be it due to Data Cleaning Process, Feature Engineering, Feature Encoding, etc) and model building, we want to make sure that each steps of the process works as intended. Furthermore, in deploying our data science system, we often automate this data ingestion and data transformation processes. Effective logging will help us monitor our pipeline so that the model that we are about to train will yield consistent, accurate results.

## Installation
```
pip install logsensei
```

## Usage examples

logsensei is very easy and intuitive to use. You can load logsensei by:
```
import logsensei
from logsensei import logger
```

Save the logs into a file by:
```
logger.setup(name="personal_projects", logger_file="./logs", level=logsensei.DEBUG)
```

The setup is done! You can use various logging functions that is provided by the logger. Some of the examples are as follows:

```
array = np.array([1, 2, 3, np.nan, 3, 2])
logger.array(array, 'd_array')
```
```
>>> 2019-10-27 13:10:26 | INFO | __main__:<module>:2 | Array d_array shape : (6,)
>>> 2019-10-27 13:10:26 | INFO | __main__:<module>:2 | Array d_array unique values : {nan, 1.0, 2.0, 3.0}
>>> 2019-10-27 13:10:26 | INFO | __main__:<module>:2 | Array d_array cardinality : 4
>>> 2019-10-27 13:10:26 | INFO | __main__:<module>:2 | Array d_array missing values : 1 (16.67%)
>>> 2019-10-27 13:10:26 | INFO | __main__:<module>:2 | Array d_array info : MEAN=2.2 | STD=0.7483314773547882 | MIN=1.0 | 25TH=2.0 | MEDIAN=2.0 | 75TH=3.0 | MAX=3.0
```

```
logger.classification(target_binary, pred_binary, "Cancer Detection")
```
```
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | Cancer Detection Classification Score
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | ====================
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | Accuracy Score : 0.46
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | Precision Score : 0.5111111111111111
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | Recall Score : 0.41818181818181815
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | F1 Score : 0.4599999999999999
>>> 2019-10-27 13:26:36 | INFO | __main__:<module>:1 | ROC AUC Score : 0.46464646464646464
```

For Full Documentation on the API, please visit [API Documentation](https://adityasidharta.com/logsensei/reference/logsensei/)

## Author

- **Aditya Kelvianto Sidharta**
    - Github: [https://github.com/AdityaSidharta](https://github.com/AdityaSidharta)
    - Personal Website: [https://adityasidharta.com/](https://adityasidharta.com/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
