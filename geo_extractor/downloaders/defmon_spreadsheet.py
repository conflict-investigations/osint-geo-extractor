from .base import Downloader

DEFMON_CSV_ENDPOINT = 'https://docs.google.com/spreadsheets/d/1eNjacqBz3nbbebasDw0VtQcX5ZscRP7pRlkSICBt2aU/export?format=csv'  # noqa

class DefmonSpreadsheetDownloader(Downloader):

    def download(self) -> str:
        data = self.request_url(DEFMON_CSV_ENDPOINT)
        return data
