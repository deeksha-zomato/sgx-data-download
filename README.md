# sgx-data-download

Please install selenium, chromedriver_py, logging, schedule for running the project and change the data in config.json accordingly.

<h4>script.py</h4>

-contains two functions:-

1) download_data: It takes download_date as argument and downloads all the four types of file in the a directory with name `default_download_directory+download_date` if the download_date is present in drop-down.
2) set_date: It takes download_date as argument and checks if the download_date is present in drop-down.

<h4>main.go</h4>

- should be called by user for downloading data of specific input date. The date should be passed as command line argument like `python main.py '28 Jul 2021' `. 
Note: The date format should be `"%d %b %Y"` this only.

<h4>scheduler.python</h4>

- should be run as a background process using command `nohup python scheduler.py & ` for automatic data download everyday. It downloads data for previous day and is triggered at 6:00 pm everyday from Tuesday to Saturday.
  
<h4>Future Work</h4>

- Currently the data can be downloaded only for the dates that are present in drop-down. We can download data for every day with the links:-
1) https://links.sgx.com/1.0.0/derivatives-historical/4951/TickData_structure.dat

2) https://links.sgx.com/1.0.0/derivatives-historical/4951/TC.txt

3) https://links.sgx.com/1.0.0/derivatives-historical/4951/TC_structure.dat

4) https://links.sgx.com/1.0.0/derivatives-historical/4951/WEBPXTICK_DT.zip

SGX hits these links with get method and the data gets downloaded. It increases the index if the data is published for next day. We can map date to index and download data for any given date.
