from selenium import webdriver

# Initialize the webdriver (e.g., ChromeDriver)
driver = webdriver.Chrome()
link = "https://backpack.tf/profiles/76561198342547469"
# Open tabs for the first 5 players
player_urls = [link] * 5
for url in player_urls:
    driver.execute_script(f"window.open('{url}')")

# Switch to each tab and perform operations
for index, handle in enumerate(driver.window_handles):
    driver.switch_to.window(handle)
    # Perform operations for the current player in the current tab

# Collect information and keep tabs open

# Switch back to the main/original tab
main_handle = driver.window_handles[0]
driver.switch_to.window(main_handle)

# Run next 5 players on existing tabs
next_player_urls = [link] * 5
for index, url in enumerate(next_player_urls):
    driver.switch_to.window(driver.window_handles[index])
    # Perform operations for the next player in the existing tab

# Close the webdriver when done
while (True):
    pass
driver.quit()
