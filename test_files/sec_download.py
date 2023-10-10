from sec_edgar_downloader import Downloader

dl = Downloader("Personal", "vishwas.g217@gmail.com", "data/")
dl.get("10-K", "AAPL", download_details=False, after="2020-01-01")

