import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

years = [2024, 2025, 2026]


def reference():
    for year in years:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(
            f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
        )
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        html = driver.page_source
        open(f"./reference.{year}.out.html", "w").write(html)
        print(f"finished reference {year}")
        driver.quit()


def espn():
    for year in years:
        request = requests.get(
            f"https://www.espn.com/nba/stats/player/_/season/{year}/seasontype/2?limit=9999",
            headers={
                "User-Agent": "Mozilla/5.0 (platform; rv:gecko-version) Gecko/gecko-trail Firefox/firefox-version"
            },
        )
        open(f"./espn.{year}.out.html", "w").write(str(request.content))
        print(f"finished espn {year}")


if __name__ == "__main__":
    reference()
    espn()
