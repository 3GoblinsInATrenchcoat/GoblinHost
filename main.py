from selenium import webdriver
from time import sleep
import pickle
import random


def start_browser():
    driver = webdriver.Firefox(executable_path='/home/devon-casey/Desktop/GoblinHost/geckodriver')
    driver.get("https://mafia.gg")
    cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    sleep(3)

    # create room
    driver.find_element_by_css_selector(
        '.cell-2-5 > div:nth-child(1) > form:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > '
        'button:nth-child(1) > span:nth-child(1)').click()
    sleep(3)

    # load setup list
    setup_list = []
    with open('Sodium-24.data', 'rb') as filehandle:
        setup_list = pickle.load(filehandle)

    # open and change settings
    open_settings = driver.find_element_by_css_selector(
        'div.game-accordion-pane:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > '
        'button:nth-child(2)')
    open_settings.click()
    setup_field = driver.find_element_by_css_selector('.input-icon-clipboard > input:nth-child(1)')
    setup_field.clear()
    setup_field.send_keys(random.choice(setup_list))
    save = driver.find_element_by_css_selector('.dialog-footer > button:nth-child(3)')
    save.click()
    return driver


def bot_intro(driver):
    new_game_started = False
    current_setup = "Sodium-24"
    current_setup_link = "https://mafiagg.fandom.com/wiki/Sodium-24"
    bot_intro1 = "Hello Everyone! I am GoblinHost, a bot designed to run closed setups. You'll never know what you " \
                 "will get with me! The current setup is: " + current_setup
    bot_intro2 = "You can find out more about the setup by going to: " + current_setup_link
    bot_intro3 = "I will automatically AFK check once the lobby is full. Good luck and have fun!"
    bot_intro4 = 'I currently have no self-moderating functionality. Be nice or report bad behavior to my owner on ' \
                 'Discord! '

    # send intro message
    chat_box = driver.find_element_by_css_selector('.game-chat-bar > form:nth-child(1) > input:nth-child(1)')
    send_chat = driver.find_element_by_css_selector(
        '.game-chat-bar > form:nth-child(1) > button:nth-child(2) > span:nth-child(1)')
    chat_box.send_keys(bot_intro1)
    send_chat.click()
    chat_box.send_keys(bot_intro2)
    send_chat.click()
    chat_box.send_keys(bot_intro3)
    send_chat.click()
    chat_box.send_keys(bot_intro4)
    send_chat.click()

    get_max_players = '12'
    while True:
        player_count_element = driver.find_element_by_css_selector('.game-top-player-count > span:nth-child(2)')
        get_player_count = player_count_element.text
        if get_player_count == get_max_players:
            chat_box.send_keys('Lobby is full! AFK checking...')
            send_chat.click()
            chat_box.send_keys('3')
            send_chat.click()
            sleep(1)
            chat_box.send_keys('2')
            send_chat.click()
            sleep(1)
            chat_box.send_keys('1')
            send_chat.click()
            sleep(1)
            afk_check = driver.find_element_by_css_selector(
                'div.game-accordion-pane:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > span:nth-child(1)')
            afk_check.click()
            sleep(10)
            player_count_element = driver.find_element_by_css_selector('.game-top-player-count > span:nth-child(2)')
            get_player_count = player_count_element.text
            if get_player_count == get_max_players:
                chat_box.send_keys('Maximum amount of players reached!')
                send_chat.click()
                chat_box.send_keys('Starting...')
                send_chat.click()
                sleep(2)
                start_button = driver.find_element_by_css_selector('button.button:nth-child(3)')
                start_button.click()
                break
        else:
            sleep(5)

    result = None
    while result is None:
        try:
            result = driver.find_element_by_css_selector('.button-pulsate > span:nth-child(1)')
            result.click()
            next_game = driver.find_element_by_css_selector('.dialog-footer > button:nth-child(2)')
            next_game.click()
            new_game_started = True
            return new_game_started
        except:
            pass


load_driver = start_browser()
new_game = bot_intro(load_driver)
while True:
    if new_game:
        sleep(5)
        bot_intro(load_driver)
    else:
        pass
