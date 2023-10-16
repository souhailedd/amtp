import scrapy
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware

class AmtspySpider(scrapy.Spider):
    name = "amtspy"
    allowed_domains = ["www.amtcomposites.co.za"]

    # Define the base URL with placeholders for the page number
    base_url = "https://www.amtcomposites.co.za/shop/page/{}"

    def __init__(self):
        self.data = []  # Create an empty list to store scraped data


    def start_requests(self):
        # Iterate through the range of pages (from 1 to 30)
        for page_number in range(1, 2):
            page_url = self.base_url.format(page_number)
            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse(self, response):
        product_page_url = response.css('.astra-shop-summary-wrap a.ast-loop-product__link::attr(href)').extract()

        #for product_page_url in product_page_urls:
        product_page_url = response.urljoin(product_page_url[0])
        yield scrapy.Request(url=product_page_url, callback=self.parse_page)
        


    def parse_page(self, response):
        product_name = response.css('.elementor-widget-container h1.product_title::text').get()
        product_price = response.css('.woocommerce-Price-amount bdi::text').get()
        product_availability = response.css('.stock::text').get()

        item = {
            'Product Name': product_name.strip() if product_name else None,
            'Price': product_price.strip() if product_price else None,
            'Availability': product_availability.strip() if product_availability else None
        }

        self.data.append(item)  # Append the scraped data to the list

    def closed(self, reason):
        if self.data:
            # Create a DataFrame with all the scraped data
            df = pd.DataFrame(self.data)

            # Get the current date and time
            current_datetime = datetime.now()
            date_string = current_datetime.strftime("%Y-%m-%d_%H-%M")  # Format as "YYYY-MM-DD_HH-MM"

            # Create the file name with the date and export the DataFrame to an Excel file
            file_name = f"scraped_data_{date_string}.xlsx"
            df.to_excel(file_name, index=False)

            # Email settings
            sender_email = "skylarroyal333@gmail.com"  # Your Gmail email address
            sender_password = "ppzc brxa dbqh jkhd"  # Your Gmail password
            recipient_email = "souhail.ouchfil@gmail.com"  # Recipient's email address
            subject = "Scraped Data"
            message = "Please find the scraped data attached."

            # Create the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            # Attach the scraped data file
            with open(file_name, "rb") as file:
                part = MIMEApplication(file.read(), Name=file_name)
                part["Content-Disposition"] = f'attachment; filename="{file_name}"'
                msg.attach(part)

            # Send the email
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.quit()
                print("Email sent successfully.")
            except Exception as e:
                print(f"Email could not be sent: {e}")
