
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime
import pandas as pd

class FacebookGroupScraper:
    def __init__(self):
        print("\n====FACEBOOK GROUP MEMBER SCRAPER====\n")

    def get_config(self):
        try:
            print("Nhập thông tin đăng nhập")
            self.email = input("Email/Username: ").strip()
            self.password = input("Password: ")
            print("\n Enter ID group facebook:")
            self.group_id = input("Group ID: ").strip()

            print("\n Số lần scroll để load thêm thành viên")
            self.scroll_count = int(input("Số lần scroll (mặc định 5): ") or "5")

        except Exception as e:
            print(f"Lỗi cấu hình : {e}")
            pass

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        except Exception as e:
            print(f"Lỗi khởi tạo trình duyệt: {e}")
            pass

    def login(self):
        try:
            self.driver.get("https://www.facebook.com")

            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys(self.email)

            pass_input = self.driver.find_element(By.ID, "pass")
            pass_input.send_keys(self.password)

            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()

            time.sleep(5)

            pass_input = self.driver.find_element(By.ID, "pass")
            pass_input.send_keys(self.password)

            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            time.sleep(5)
            print("Đăng nhập thành công")


            return True
        except Exception as e:
            print(f"Lỗi đăng nhập: {e}")
            return False

    def get_group_members(self):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(5)

            members = set()

            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                print(f"Scroll lần {i + 1}/{self.scroll_count}")

                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")

                for user in user_elements:  
                    try:
                        href = user.get_attribute("href")
                        if '/user/' in href:
                            user_id = href.split('/user')[1].strip('/')
                            name = user.text
                            members.add((user_id, name))  
                            print(user_id, " - ", name)
                    except Exception as e:  
                        continue

            return list(members)  # Đặt ngoài vòng lặp
        except Exception as e:
            print(f"Lỗi thu thập thành viên: {e}")
            return None

def main():
    scraper = None
    try:
        scraper = FacebookGroupScraper()
        scraper.get_config() 
        scraper.setup_driver()  
        if scraper.login():
            print("Đăng nhập thành công")
            members = scraper.get_group_members()
            if members:
                print(f"\nThu thập được {len(members)} thành viên.")
                # Save the list of members to a CSV file
                df = pd.DataFrame(members, columns=["User ID", "Name"])
                df.to_csv(f"facebook_group_{scraper.group_id}_members.csv", index=False)
                print(f"Thông tin thành viên đã được lưu vào 'facebook_group_{scraper.group_id}_members.csv'")
            else:
                print("Không thu thập được thành viên.")
        else:
            print("Đăng nhập thất bại")
    except Exception as e:
        print(f"Lỗi trong quá trình thực thi: {e}")
    finally:
        if scraper and hasattr(scraper, 'driver'):
            scraper.driver.quit()

if __name__ == "__main__":
    main()
