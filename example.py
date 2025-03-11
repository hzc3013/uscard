import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys

def incremental_scroll(driver, max_iterations=20, scroll_step=300):
    """
    Scrolls down the page in small increments (scroll_step px).
    - Does up to max_iterations.
    - After each scroll, waits 2-4 seconds randomly.
    - Stops early if there's no change in page height (meaning we've reached the bottom).
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_iterations):
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(random.uniform(2, 4))  # Wait a bit so new content can load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height <= last_height:
            # No more new content; we've likely reached the bottom
            break
        last_height = new_height

def login_and_visit_uscardforum(username, password):
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_argument("--headless")  # Uncomment if you want headless
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        # 1. Go to the login page
        driver.get("https://www.uscardforum.com/login")
        time.sleep(random.uniform(1, 2))

        # Close cookie consent if present
        try:
            cookie_btn = driver.find_element(By.CSS_SELECTOR, "a.cc-btn.cc-dismiss")
            cookie_btn.click()
            time.sleep(random.uniform(3, 5))
        except:
            pass

        # 2. Fill username
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login-account-name"))
        )
        username_field.send_keys(username)

        # 3. Fill password
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login-account-password"))
        )
        password_field.send_keys(password)

        # Submit by pressing Enter on the password field
        password_field.send_keys(Keys.ENTER)

        # 4. Wait for login to complete
        time.sleep(random.uniform(2, 4))

        # 5. Navigate to the "new" page (or whichever page you want)
        driver.get("https://www.uscardforum.com/new")
        time.sleep(random.uniform(3, 5))

        # 6. Grab the post links
        posts = driver.find_elements(By.CSS_SELECTOR, "a.title.raw-link")
        num_found = len(posts)
        print(f"Found {num_found} posts on the page.")

        # If no posts are found, exit with an error message
        if num_found == 0:
            print("ERROR: No posts found on the page! Exiting.")
            sys.exit(1)

        # Pick a random number of posts between 3 and 7
        num_posts_to_visit = min(num_found, random.randint(3, 7))
        print(f"Will visit {num_posts_to_visit} random posts.")

        # Shuffle so we pick random ones
        random.shuffle(posts)

        for i in range(num_posts_to_visit):
            post_link = posts[i]
            post_title = post_link.text
            post_url = post_link.get_attribute("href")
            print(f"Visiting post #{i+1}: {post_title} ({post_url})")

            # 7. Open the post
            post_link.click()
            time.sleep(random.uniform(2, 4))

            # 8. Randomly scroll 5 to 10 times
            #    Each time, we call incremental_scroll with smaller max_iterations
            #    so it won't scroll too far in one go.
            scroll_loops = random.randint(5, 10)
            for _ in range(scroll_loops):
                incremental_scroll(driver, max_iterations=1, scroll_step=300)
                # This means each loop calls incremental_scroll once.
                # If you want each call to do more steps, set max_iterations=2 or 3, etc.

            # 9. Capture text from the post
            post_content = driver.find_element(By.CSS_SELECTOR, "div.post-stream").text

            # 10. Write to a text file with current date/time
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("posts_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{current_timestamp}] === Post #{i+1}: {post_title} ===\n")
                f.write(post_content)
                f.write("\n\n")

            # 11. Go back to the list
            driver.back()
            time.sleep(random.uniform(2, 4))

            # 12. Re-fetch the post elements in case the page reloaded
            posts = driver.find_elements(By.CSS_SELECTOR, "a.title.raw-link")

        print("Done visiting posts. Check 'posts_log.txt' for the results.")

    finally:
        driver.quit()

if __name__ == "__main__":
    USERNAME = "hzc3008"
    PASSWORD = "200812hzc"
    login_and_visit_uscardforum(USERNAME, PASSWORD)
