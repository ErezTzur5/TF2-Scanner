import tkinter as tk
import requests
import multiprocessing
import urllib.request
import os 
import sv_ttk
import threading
import webbrowser
# import sys
import time
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from player_data import Player
from driver import Mydriver
from tf_utils import sorter
from io import BytesIO



text_box = None
root = None
player_info_button = None

# BASE_DIR = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

def filter_before_data(steam_file):
    sorted_list = []
    for steam_id in steam_file:
        player = Player(steam_id)
        player.get_hours()
        if float(player.hours_played['hours']) < 700:
            sorted_list.append(steam_id)
    return sorted_list



def open_link(url):
    webbrowser.open_new(url)

# steam_id_file_raw = sorter(os.path.join("tf.txt"))
# print('steam_id_file_raw:',steam_id_file_raw)

# steam_id_file = filter_before_data(steam_id_file_raw)
# print('steam_id_file(after changes):',steam_id_file)


TRASH_IMG_DIR = os.path.join("docx", "trash_img")
###OS FUNCS####

def clear_directory(directory):
    """
    Deleting all images from the trash folder.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def create_directory_if_not_exists(directory):
    """
    Create directory called imgs if not exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(image_url):
    """
    Downloading images to represent them later.

    """
    image_name = image_url.split("/")[-1]
    image_path = os.path.join(TRASH_IMG_DIR, image_name)
    urllib.request.urlretrieve(image_url, image_path)
    return image_path


def gather_info_batch(batch):
    with multiprocessing.Pool(processes=5) as pool:
        results = pool.map(gather_player_info, batch)
    return results


def gather_player_info(id):
    """
    Calling my Class for players to gather all information about players
    """
    driver = Mydriver().get_driver()
    player = Player(id)
    player.get_name()
    player.get_hours()
    player.get_items()
    driver.close()



    player_info = {
        "Name": player.player_name,
        "Steam_id":player.steam_id,
        "Hours": player.hours_played,
        "Inventory_date":player.inventory_date,
        "Items": player.items
    }

    
    return player_info


def submit_wrapper():
    thread = threading.Thread(target=submit)
    thread.start()

def submit():
    start_time = time.time()
    global player_info_button
    global text_box
    global root

    player_info_button.forget()
    text_box.forget()
    root.update()
    players_info = text_box.get("1.0", "end-1c")
    if players_info:
        messagebox.showinfo("Success", "Player information saved")
        
        # Clear the contents of the TRASH_IMG_DIR directory
        clear_directory(TRASH_IMG_DIR)
        # Get the Steam IDs from the players_info and call the gathering function
        steam_id_file_raw = sorter(players_info)
        steam_id_file = filter_before_data(steam_id_file_raw)

        # Save the gathered information to a separate file (player_data.txt)
        print("Number of Players:", len(steam_id_file))
        with open(os.path.join("player_data.txt"), "w",encoding="utf-8") as data_file:
            gathered_info = []
            for i in range(0,len(steam_id_file),5):
                three_players = steam_id_file[i:i + 5]
                # All player info gather and not sorted
                gathered_info += gather_info_batch(three_players)
                # Sorting list by hours played - the lowest will be on the top of the list 
                sorted_character_list = sorted(gathered_info, key=lambda x: float(x['Hours']['hours']))
                # Filtering the Character list for players that played more than 700 hours
                filtered_character_list = [character for character in sorted_character_list if float(character['Hours']['hours']) <= 700]
                # print('sortedddddddd',filtered_character_list)
                # Packing information
                for player in sorted_character_list:
                    data_file.write(f"Name: {player['Name']}\n")
                    data_file.write(f"Hours: {player['Hours']}\n")
                    data_file.write(f"Inventory_date: {player['Inventory_date']}\n")
                    # data_file.write(f"last time bp was sync: {player['Inventory']}\n")
                    link = f"https://backpack.tf/profiles/{player['Steam_id']}"
                    data_file.write(f"Link: {link}\n")
                    for item in player["Items"]:
                        data_file.write("Items:\n")
                        data_file.write(f"  Name: {item['name']}  Price: {item['price']}  Image: {item['image']}\n")
                    data_file.write("\n")


            
        # Display the "Player Info" button
        text_box.pack()
        player_info_button.pack()
        player_info_button.config(command=lambda: display_player_info(filtered_character_list))
        # text_box.pack()
        # root.update()
    else:
        messagebox.showwarning("Warning", "No player information to save!")
    # Record the end time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed Time:", elapsed_time, "seconds")

def display_player_info(player_data):
    
    player_info_window = tk.Toplevel(root)
    player_info_window.title("Player Info")
    enlarged_width = 1600
    enlarged_height = 800
    player_info_window.geometry(f"{enlarged_width}x{enlarged_height}")


    canvas = tk.Canvas(player_info_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = ttk.Scrollbar(player_info_window, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
    
    frame = ttk.Frame(canvas)
    
    canvas.create_window((0, 0), window=frame)
    print("Number of Players:", len(player_data))  # Debugging: Check number of players
    for player in player_data:
        player_frame = ttk.Frame(frame,borderwidth=3,relief="solid")
        player_frame.pack(padx=500, pady=40,anchor="center",fill="both", expand=True)
        


        player_name_label = tk.Label(player_frame, text=f"Name: {player['Name']}")
        player_name_label.pack(anchor="center")

        player_hours_label = tk.Label(player_frame, text=f"Hours Played: {player['Hours']['hours']}")
        player_hours_label.pack(anchor="center")
    
        player_inv_date_label = tk.Label(player_frame, text=f"Backpack Date: {player['Inventory_date']}")
        player_inv_date_label.pack(anchor="center")

        link = f"https://backpack.tf/profiles/{player['Steam_id']}"
        link_label = tk.Label(player_frame, text=f"Link: {link}\n")
        link_label.config(fg="#6495ED")
        link_label.bind("<Button-1>", lambda event, url=link: open_link(url))  # Pass the link as an argumen
        link_label.pack(anchor="center")

        items_frame = ttk.Frame(player_frame)
        items_frame.pack(anchor="w")

        for item in player['Items']:
            item_frame = ttk.Frame(items_frame)
            item_frame.pack(padx=50,anchor="w")
            # print((f"  Name: {item['name'][:7]}"))


            image_url = item['image']

            try:
                response = requests.get(image_url, stream=True, timeout=10)
                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    image = image.resize((55, 55), Image.ANTIALIAS)
                    ## BORDER HANDLE ##
                    border_width = 5
                    
                    if item['name'][:7] == 'Strange':
                        background_color = "#8a4620"
                        border_color = "#cf6a32"

                    elif item['name'][:7] == 'Haunted':
                        background_color = "#0cc880"
                        border_color = "#38f3ab"

                    elif item['name'][:7] == 'Unusual':
                        background_color = "#583471"
                        border_color = "#8650ac"

                    elif item['name'][:7] == 'Vintage':
                        background_color = "#2b3b57"
                        border_color = "#476291"
                    else:
                        background_color = "#a88e00"
                        border_color = "gold"

                    bordered_image = ImageOps.expand(image, border=border_width, fill=border_color)
                    bordered_image_with_background = ImageOps.expand(bordered_image, border=border_width, fill=background_color)
                    photo = ImageTk.PhotoImage(bordered_image_with_background)


                    item_image_label = tk.Label(item_frame, image=photo)
                    item_image_label.image = photo
                    item_image_label.pack(side="left")

            except requests.exceptions.RequestException as e:
                print(f"Error retrieving image for URL {image_url}: {e}")
                continue  # Skip to the next item if there's an error

            item_label = tk.Label(item_frame, text=f"{item['name']} ({item['price']})")
            item_label.pack(side="left", padx=5)
            
    canvas.focus_set()
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))



def main():
    multiprocessing.freeze_support()
    global player_info_button
    global text_box
    global root


    root = tk.Tk()
    root.title("Erez Scans")
    # root.iconbitmap('static/icon.png')

    window_width = 1000
    window_height = 615
    root.geometry(f"{window_width}x{window_height}")

    bg_image_path = os.path.join("static", "tf2.png")


    pil_image = Image.open(bg_image_path)
    pil_image = pil_image.resize((window_width, window_height), Image.ANTIALIAS)
    bg_image = ImageTk.PhotoImage(pil_image)

    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[30, 10])

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10)

    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Tab 1")

    text_box = tk.Text(tab1, height=30, width=80)
    text_box.pack()
    
    

    submit_button = tk.Button(
        tab1,
        text="Scan",
        command=submit_wrapper,
        relief=tk.RAISED,  # Raised appearance
        bg="red",  # Background color
        fg="white",  # Text color
        font=("Helvetica", 12, "bold"),  # Font style
        padx=10,  # Horizontal padding
        pady=5,  # Vertical padding
        activebackground="lightgreen",  # Background color when button is pressed
        activeforeground="black",
    )
    submit_button.pack(side="bottom")

    

    player_info_button = tk.Button(tab1, text="Player Info", command=display_player_info,
        relief=tk.RAISED,  # Raised appearance
        bg="blue",  # Background color
        fg="white",  # Text color
        font=("Helvetica", 12, "bold"),  # Font style
        padx=10,  # Horizontal padding
        pady=5,  # Vertical padding
        activebackground="lightgreen",  # Background color when button is pressed
        activeforeground="black",
    )
    player_info_button.pack()
    player_info_button.pack_forget()

    sv_ttk.set_theme("dark")
    root.mainloop()

if __name__ == '__main__':
    main()
    