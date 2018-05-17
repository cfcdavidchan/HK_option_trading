# Hong Kong Stock Option Trading

This project is aiming at designing a option trading strategy for trading Hong Kong stock option, build on Python, and based on the date provided by [HKEX](http://www.hkex.com.hk/)

![](/example.png?raw=true)
# Contents
  - [Installation](https://github.com/cfcdavidchan/HK_option_trading#installation)
  - [exe file extraction](https://github.com/cfcdavidchan/HK_option_trading#exe_file_extraction_(Windows_Only))


### Installation
* ##### Language
 - Python 3.5 or above
* ##### Prerequisites
 - [pandas](https://pandas.pydata.org/)
 - [QuantLib](http://www.quantlib.org/)

* ##### Conda Virtual Environment create
  `conda create -n stock_option python=3.5 numpy cython pystan -c conda-forge`

* ##### QuantLib Installation (Ubuntu)
  Reference: https://www.quantlib.org/install/windows-python.shtml

  All the supporting files and library can be found in `/Quantlib/`

  1. Boost Installation

    `sudo apt-get install libboost-all-dev`

  2. QuantLib Installation
    1.  unzip the QuantLib

        `tar xzf QuantLib-1.12.tar.gz`

    2.  configure QuantLib by executing

        `cd QuantLib-1.12`

        `./configure`

    3.  setup the build

        `make`

    4.  builds the library and Install

        `sudo make install`

  3. QuantLib-Python Installation

        1.  unzip the QuantLib-Python

            `tar xzf QuantLib-SWIG-1.12.tar.gz`

        2.  configure QuantLibPython by executing

            `cd QuantLib-SWIG-1.12`

            `./configure`

        3.  setup the build

            `make -C Python`

        4.  builds the library and Install

            `sudo make -C Python install`
* ##### QuantLib Installation (Ubuntu)
All the supporting files and library can be found in `/Quantlib/`

  1. Boost Installation

    `sudo apt-get install libboost-all-dev`

  2. QuantLib Installation
    1.  unzip the QuantLib

        `tar xzf QuantLib-1.12.tar.gz`

    2.  configure QuantLib by executing

        `cd QuantLib-1.12`

        `./configure`

    3.  setup the build

        `make`

    4.  builds the library and Install

        `sudo make install`


* ##### QuantLib Installation (Windows)

    1.  Install QuantLib directly by `pip`

        `pip install QuantLib-Python`

### exe file extraction (Windows Only)
  1. Install [pyinstaller](https://www.pyinstaller.org/) by pip

        `pip install pyinstaller`
  2. Run pyinstaller in the directroy containing application.py and the exe will be created inside `/dist/`

        `pyinstaler --onefile --windowed application.py`

### Usage
  The script will automatically create `/csv_tmp/` and `csv_stock` and update the `option_code.json` when running it.

  `/csv_tmp/` - storage the entire csv file,including all the stock option data.

  `/csv_stock/` - storage specified stock only, separating in call table and put table.

  `option_code.json` - a python dictionary, using 5 digital stock code as key and HKATS code and underlying stock name as value.

  Update button - Update the `option_code.json`

  Clean button - Clean up both the `/csv_tmp/` and `/csv_stock/`

  Full/Stock list - Full mean download all the data. Stock means downloads the spcified stock data only

  `+` button - Adding stock

  Download button - Download the data after inputing all the information


  There are two different date counting for downloading the data. One is by date, another is by period.

  In by date method, end date and start date is required and **the tpye in format must follow, dd mm yyyy** . The downloaded data will be within the specified date range in this method. On the other hand, end date and period is requried in bt period method. This method will download the data by rolling the end date backward according to the specified period.

  Note: The applcation will use last trading day (current date not counted) as the updated date, which is shown in End Date column when the application runs. Therefore, End date or Start Date column can never be greater than the updated date, shown initally.

  If the specified date, both End Date and Start Date, the application will find the nearest trading data by roll backward the date. For example, if 01 05 2018 (labor holiday) is specified, the application will roll back to 04 30 2018. Kindly note that the rolling back date will not be noticed in the windows but will do it in the back-end.
