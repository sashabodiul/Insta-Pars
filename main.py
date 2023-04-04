from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.common.by import By
import customtkinter as ck
from tkinter import *

class InstagramBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("../chromedriver/chromedriver")
    
    def login(self):
        #get url page
        self.browser.get('https://www.instagram.com/')
        time.sleep(random.randrange(3,5))
        #login to instagram
        try:
            user_input = self.browser.find_element(By.NAME,'username')
            user_input.clear()
            user_input.send_keys(self.username)

            time.sleep(2)

            password_input = self.browser.find_element(By.NAME,'password')
            password_input.clear()
            password_input.send_keys(self.password)

            password_input.send_keys(Keys.ENTER)
            
            time.sleep(10)

        except Exception as e:
            print("[ERROR] - Something went wrong: "+e)

    def close(self):
        #close browser window
        self.browser.close()
        self.browser.quit()

    def enter_links(self,links:list):
        #check links
            try:

                for link in links:
                    if link == 'q':
                        print('[INFO] - List of links completed successfully!')
                links = list(set(links))

                with open('links.txt', 'a') as f:
                    for link in links:
                        f.writelines(link)

            except Exception as e:
                print("[ERROR] - Something went wrong: "+e)

    def search_posts(self):

        browser = self.browser
        with open('links.txt') as f:
            f = f.readlines()
        for link in f:
            browser.get(link)
            time.sleep(3)

            hrefs = browser.find_elements(By.TAG_NAME,'a')
            posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for url in posts_urls[:3]:
                with open('secondlinks.txt', 'a') as f:
                    f.writelines(url+'\n')

    def search_by_likes(self):
        browser = self.browser
        users_list = []
        with open('secondlinks.txt') as f:
            f = f.readlines()
        for link in f:
            browser.get(f'{link}liked_by/')
            time.sleep(2)
            users = browser.find_elements(By.XPATH,'//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"]')
            for user in users:
                users_list.append(user.text)
            users_list = list(set(users_list))
            with open('users.txt', 'a') as f:
                for log in users_list:
                    print(log)
                    f.writelines(log+'\n')


class InstaBotApp(ck.CTk):
    
    def __init__(self):
        super().__init__()
        self.geometry('1080x756')
        self.title('Insta Bot')
        self.resizable(0,0)
        #initialize the links listbox
        self.Playlist = Listbox(self,width=40)
        self.Playlist.pack(side=LEFT, fill=BOTH)
        #initialize login layout
        self.login_label = ck.CTkLabel(self, text='Login')
        self.login_label.pack()
        self.login_entry = ck.CTkEntry(self)
        self.login_entry.pack()
        #initialize password layout
        self.login_password = ck.CTkLabel(self, text='Password')
        self.login_password.pack()
        self.password_entry = ck.CTkEntry(self,show="*")
        self.password_entry.pack()
        #info label
        self.info_label = ck.CTkLabel(self, text='')
        self.info_label.pack()
        #initialize button submit
        self.button_submit = ck.CTkButton(self, text='Submit', command=self.login, cursor='hand2')
        self.button_submit.pack()
        self.empty1_label = ck.CTkLabel(self, text='')
        self.empty1_label.pack()
        #initialize links layout
        self.link_label = ck.CTkLabel(self, text='Insert link')
        self.link_label.pack()
        self.link_entry = ck.CTkEntry(self)
        self.link_entry.pack()
        self.empty2_label = ck.CTkLabel(self, text='')
        self.empty2_label.pack()
        self.button_insert = ck.CTkButton(self, text='Add link', command=self.insert_link, cursor='hand2')
        self.button_insert.pack()
        self.empty3_label = ck.CTkLabel(self, text='')
        self.empty3_label.pack()
        #initialize button following
        self.follow_button = ck.CTkButton(self, text='Start following', command=self.following, cursor='hand2')
        self.follow_button.pack()

    def following(self):
        ...

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        self.login_entry.delete(0,END)
        self.password_entry.delete(0,END)
        try:
            bot = InstagramBot(username,password)
            bot.login()
            bot.enter_links(self.Playlist.get(0,END))
            bot.search_posts()
            bot.search_by_likes()
            self.Playlist.delete(0,END)
            with open('users.txt') as f:
                f = f.readlines()
            for user in f:
                self.Playlist.insert(END,user)
        except Exception as e:
            self.info_label.configure(text=f'[ERROR] - {e}')
        finally:
            bot.close()
    
    def insert_link(self):
        link = self.link_entry.get()
        self.Playlist.insert(END, link)
        self.link_entry.delete(0, END)

def main():
    app = InstaBotApp()
    app.mainloop()

if __name__ == '__main__':
    main()