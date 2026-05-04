import flet as ft
import requests

def main(page: ft.Page):
    # --- Window Configuration ---
    page.title = "Joke Generator"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 50
    
    # Set window dimensions
    page.window.width = 600
    page.window.height = 700

    # --- UI Elements ---
    # The dropdown menu using key/text pairs.
    category_dropdown = ft.Dropdown(
        label="Select a Category",
        options=[
            ft.dropdown.Option(key="Any", text="Surprise Me! (Any)"),
            ft.dropdown.Option(key="Programming", text="Programming"),
            ft.dropdown.Option(key="Misc", text="Miscellaneous"),
            ft.dropdown.Option(key="Pun", text="Classic Puns"),
            ft.dropdown.Option(key="Spooky", text="Spooky"),
            ft.dropdown.Option(key="Christmas", text="Christmas"),
            ft.dropdown.Option(key="Dark", text="Dark Humor"),
            # Custom mixed categories by combining tags with a comma
            ft.dropdown.Option(key="Programming,Pun", text="Coding Puns"), 
            ft.dropdown.Option(key="Misc,Pun", text="Random Puns"), 
        ],
        value="Any", # Default selected value
        width=250,
        border_color="pink400",
    )

    # Text element to display single-part jokes, or the 'setup' of a two-part joke
    setup_text = ft.Text(size=22, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)
    
    # Text element for the punchline. 
    # It starts invisible and fades in when the reveal button is clicked.
    punchline_text = ft.Text(
        size=26, 
        color="pink400", 
        weight=ft.FontWeight.BOLD, 
        text_align=ft.TextAlign.CENTER, 
        opacity=0, 
        animate_opacity=400 # 400 milliseconds fade-in animation
    )

    # Function triggered by the 'Reveal Punchline' button
    def reveal_punchline(e):
        punchline_text.opacity = 1 # Make the punchline visible
        reveal_btn.visible = False # Hide the button itself
        page.update() # Refresh the UI

    # Button to reveal the punchline 
    reveal_btn = ft.ElevatedButton(
        "Reveal Punchline", 
        on_click=reveal_punchline, 
        visible=False, 
        color="white", 
        bgcolor="pink600"
    )

    # --- Main API Logic ---
    # Function triggered by the main 'Get a Joke' button
    def fetch_joke(e):
        # Reset the UI state to a "loading" state
        setup_text.value = "Fetching a joke..."
        punchline_text.opacity = 0
        punchline_text.value = ""
        reveal_btn.visible = False
        page.update()

        # Build the API URL based on the dropdown selection
        cat = category_dropdown.value
        url = f"https://v2.jokeapi.dev/joke/{cat}"
        
        try:
            # Fetch data from the API and convert the JSON response to a Python dictionary
            res = requests.get(url).json()
            
            # Handle the response
            if res.get("error"):
                # Handle API-side errors
                setup_text.value = "Whoops, API error! Try again."
                
            elif res.get("type") == "single":
                # Handle single-part jokes 
                setup_text.value = res.get("joke")
                
            else:
                # Handle two-part jokes
                setup_text.value = res.get("setup")
                punchline_text.value = res.get("delivery")
                reveal_btn.visible = True # Show the reveal button
                
        except Exception:
            # Handle connection errors 
            setup_text.value = "Failed to connect to the internet."
        
        # Refresh the UI to show the final result
        page.update()

    # Main button to trigger the API call
    get_joke_btn = ft.ElevatedButton(
        "Get a Joke!", 
        on_click=fetch_joke, 
        width=250, 
        height=50,
        bgcolor="blue700",
        color="white"
    )

    # --- Layout Structure ---
    # A Card container to give the joke text a nice background box
    joke_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [setup_text, reveal_btn, punchline_text],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            width=500,
            height=300,
            padding=30,
            alignment=ft.Alignment(0, 0), # Centers the content inside the container
            border_radius=15,
        ),
        elevation=10,
        margin=ft.margin.only(top=30)
    )

    # Add all main elements to the Flet window
    page.add(
        ft.Text("Joke API Explorer", size=35, weight=ft.FontWeight.BOLD, color="white"),
        ft.Divider(height=20, color="transparent"),
        category_dropdown,
        get_joke_btn,
        joke_card
    )

ft.app(target=main)