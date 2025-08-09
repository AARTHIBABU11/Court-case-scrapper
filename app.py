from flask import Flask, render_template, request
from scraper_mannual_captcha import scrape_filing_status, get_captcha_image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        section = request.form.get("section")
        from_date = request.form.get("from_date")
        captcha = request.form.get("captcha")

        result = scrape_filing_status(section, from_date, captcha)
        return render_template("index.html", result=result)

    else:
        # On GET, open driver, get captcha image, then quit
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://hcmadras.tn.gov.in/filing_status.php")

        captcha_img_b64 = get_captcha_image(driver)
        driver.quit()

        return render_template("index.html", captcha_image=captcha_img_b64)


if __name__ == "__main__":
    app.run(debug=True)
