from bs4 import BeautifulSoup
import requests

def transformEmbedURL(original_url):
    id = original_url.split('/')[-1]
    return "www.youtube.com/watch?v=" + id

def create_link(text, url):
    return "[" + text + "](" + url + ")"

def scrape_videos(soup, file):
    f = open(file, "w")
    days = soup.find_all(class_="schedule-item")

    for day in days:
        title_tags = day.find_all('h2')
        number = title_tags[0].string
        title = title_tags[1].string

        content = day.find_all(class_="section")[0]
        details = content.find_all("details")

        f.write("## " + (number if number else " ") + "\t" + title + "\n")

        for detail in details:
            vid_title = detail.summary.string
            src = detail.iframe["src"]
            f.write("* " + create_link(vid_title, transformEmbedURL(src)))
            f.write("\n")

        f.write("\n")

    f.close()

def download_pdf(url, file):
    response = requests.get(url)
    pdf = open(file, 'wb')
    pdf.write(response.content)
    pdf.close()

    return 0; 

def scrape_assignments(soup, base_url, base_filepath):
    days = soup.find_all(class_="schedule-item")

    for day in days:
        number = day.h2.string 
        number = number if number else ""
        number = "0" + number if len(number) < 2 else number
        assignments = day.find_all(class_="section")[1]
        links = [a["href"] for a in assignments.find_all('a')]

        for link in links:
            filename = base_filepath + number + '-' + link.split('/')[-1]
            url = base_url + link
            download_pdf(url, filename)

def main():
    website_url = "https://www.eecs.umich.edu/courses/eecs201/fa2022/schedule"
    base_url = "https://www.eecs.umich.edu/"
    base_filepath = "assignments/"
    vid_filename = "eecs201.md"

    page = requests.get(website_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_videos(soup, vid_filename)
    scrape_assignments(soup, base_url, base_filepath)

main()