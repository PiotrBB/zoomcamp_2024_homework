from concurrent.futures import ThreadPoolExecutor
import requests

file_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{month}.parquet'
urls = [file_url.format(month=str(m).zfill(2)) for m in range(1, 13)]

def download_file(url):
    response = requests.get(url)
    if "content-disposition" in response.headers:
        content_disposition = response.headers["content-disposition"]
        filename = content_disposition.split("filename=")[1]
    else:
        filename = url.split("/")[-1]
    with open(f'data/{filename}', mode="wb") as file:
        file.write(response.content)
    print(f"Downloaded file {filename}")
    
if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, urls)
